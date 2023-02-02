from django.shortcuts import render
from .models import *
from .forms import *
__all__ = [
    'home_view',
    'list_view',
]


def home_view(request):
    form = FindForm()
    get = request.GET
    city = get.get('city')
    language = get.get('language')
    filter_ = {
        'city__slug': city,
        'language__slug': language,
    }
    filter_ = {key: value for key, value in filter_.items() if value}
    qs = Vacancy.objects.filter(**filter_)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})


def list_view(request):
    form = FindForm()
    get = request.GET
    city = get.get('city')
    language = get.get('language')
    filter_ = {
        'city__slug': city,
        'language__slug': language,
    }
    filter_ = {key: value for key, value in filter_.items() if value}
    qs = Vacancy.objects.filter(**filter_)
    return render(request, 'scraping/list.html', {'object_list': qs, 'form': form})
