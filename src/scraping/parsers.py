import requests
from bs4 import BeautifulSoup as bs
from random import randint
__all__ = [
    'work',
    'djinni',
]

headers = [
    {
        'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'UserAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'UserAgent': 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'UserAgent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
]


def work(url_):
    jobs_ = []
    errors_ = []
    domain = 'https://www.work.ua'
    resp = requests.get(url=url_, headers=headers[randint(0, 5)])

    status_code = resp.status_code

    if status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            divs = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in divs:
                title = div.find('h2')
                href = title.a['href']
                description = div.p.text
                company = logo['alt'] if (logo := div.find('img')) else 'No company'
                jobs_.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': description,
                    'company': company,
                })
        else:
            errors_.append({
                'url': url_,
                'title': 'Div does not exists.',
            })
    else:
        errors_.append({
            'url': url_,
            'title': 'Page do not response',
        })
    return jobs_, errors_


def djinni(url_):
    jobs_ = []
    errors_ = []
    domain = 'https://djinni.co'
    resp = requests.get(url=url_, headers=headers[randint(0, 5)])

    status_code = resp.status_code

    if status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            lis = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in lis:
                title = li.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                content = li.find('div', attrs={'class': 'list-jobs__description'})
                description = content.text
                company = company.text if (company := li.find('div', attrs={'class': 'list-jobs__details__info'})) else 'No company'
                jobs_.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': description,
                    'company': company,
                })
        else:
            errors_.append({
                'url': url_,
                'title': 'Div does not exists.',
            })
    else:
        errors_.append({
            'url': url_,
            'title': 'Page do not response.',
        })
    return jobs_, errors_


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/?location=kyiv&region=UKR'
    jobs, errors = djinni(url)
    with open('work.text', 'w', encoding='utf8') as f:
        f.write(str(jobs))
