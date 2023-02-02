import os, sys

from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_srv.settings'
import django
django.setup()
from scraping.parsers import *
from scraping.models import *
from django.db import DatabaseError

User = get_user_model()

parsers = (
    (work, 'https://www.work.ua/ru/jobs-python/'),
    (djinni, 'https://djinni.co/jobs/?location=kyiv&region=UKR'),
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_li = set((q['city_id'], q['language_id']) for q in qs)
    return settings_li


city = City.objects.filter(slug='kaluga').first()
language = Language.objects.filter(slug='php').first()

jobs, errors = [], []

for fun, url in parsers:
    j, e = fun(url)
    jobs += j
    errors += e
    # with open('work.text', 'w', encoding='utf8') as f:
    #     f.write(str(jobs))

for job in jobs:
    try:
        Vacancy(**job, city=city, language=language).save()
    except DatabaseError as e:
        pass

Error(data=errors).save() if errors else None
