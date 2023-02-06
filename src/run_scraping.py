import asyncio
import os
import sys
import time
import datetime as dt
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
    (work, 'work'),
    (djinni, 'djinni'),
)

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_li = set((q['city_id'], q['language_id']) for q in qs)
    return settings_li


def get_urls(settings_):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in settings_:
        if pair in url_dict:
            tmp = {
                'city': pair[0],
                'language': pair[1],
                'url_data': url_dict[pair]
            }
            urls.append(tmp)
    return urls


async def main(args):
    fun, url, city, language = args
    job, err = await loop.run_in_executor(None, fun, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kaluga').first()
# language = Language.objects.filter(slug='php').first()





start = time.time()

loop = asyncio.new_event_loop()
tmp_task = [
    (fun, data['url_data'][key], data['city'], data['language'])
    for data in url_list
    for fun, key in parsers
]
tasks = asyncio.wait([loop.create_task(main(args)) for args in tmp_task])
loop.run_until_complete(tasks)
loop.close()

print(time.time() - start)

for job in jobs:
    try:
        Vacancy(**job).save()
    except DatabaseError as e:
        print(e)
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        Error(data=f'errors:{errors}').save()
