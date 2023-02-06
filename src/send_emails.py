import os
import sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

# Run Django
project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_srv.settings'
django.setup()

from scraping.models import *
from scraping_srv.settings import EMAIL_HOST_USER

EMAIL_ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий {today}'
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению а сегодня по Вашим предпочтениям данных нет.</h2>'

User = get_user_model()
users = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for user in users:
    users_dict.setdefault((user['city'], user['language']), [])
    users_dict[(user['city'], user['language'])].append(user['email'])
if users_dict:
    params = {
        'city_id__in': [],
        'language_id__in': [],
    }
    for city, language in users_dict.keys():
        params['city_id__in'].append(city)
        params['language_id__in'].append(language)
    vacancies = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies_dict = {}
    # for vacancy in vacancies:
    #     vacancies_dict.setdefault((vacancy['city_id'], vacancy['language_id']), [])
    #     vacancies_dict[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)
    # for keys, emails in users_dict.items():
    #     rows = vacancies_dict.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<div><a href="{row["url"]}">{row["title"]}</a></div>'
    #         html += f'<p>{row["description"]}</p>'
    #         html += f'<p>{row["company"]}</p><br /><hr>'
    #     html_ = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(html_, "text/html")
    #         msg.send()

subject = ''
text_content = ''
to = EMAIL_ADMIN_USER
html_ = ''

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        html_ += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p>'
    subject += 'Ошибки скрапинга'
    text_content = 'Ошибки скрапинга'

    data = error.data.get('user_data')
    if data:
        html_ += '<hr />'
        html_ += '<h2>Пожелания пользователей</h2>'
    for i in data:
        html_ += f'<p>Город: {i["city"]}, Специальность: {i["language"]}, E-mail: {i["email"]}</p>'
    subject += 'Пожелания пользователей'
    text_content = 'Пожелания пользователей'


qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        urls_err = f'<p>Для города: {keys[0]} и ЯП: {keys[1]} отсутствует url.</p>'

if urls_err:
    subject += 'Ошибки скрапинга'
    html_ += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_, "text/html")
    msg.send()
