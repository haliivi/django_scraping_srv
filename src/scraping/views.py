from django.core.paginator import Paginator
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
    context = {'city': city, 'language': language, 'form': form}
    filter_ = {
        'city__slug': city,
        'language__slug': language,
    }
    filter_ = {key: value for key, value in filter_.items() if value}
    qs = Vacancy.objects.filter(**filter_)
    paginator = Paginator(qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
