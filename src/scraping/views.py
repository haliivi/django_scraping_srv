from django.contrib.admindocs.views import ModelDetailView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
__all__ = [
    'home_view',
    'list_view',
    'v_detail',
    'VDetail',
    'VList',
    'VCreate',
    'VUpdate',
    'VDelete',
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
    qs = Vacancy.objects.filter(**filter_).select_related('city', 'language')
    paginator = Paginator(qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, 'scraping/list.html', context)


def v_detail(request, pk):
    # object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})


class VDetail(DetailView):
    template_name = 'scraping/detail.html'
    model = Vacancy
    context_object_name = 'object'


class VList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        get = self.request.GET
        context['city'] = get.get('city')
        context['language'] = get.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        filter_ = {
            'city__slug': city,
            'language__slug': language,
        }
        filter_ = {key: value for key, value in filter_.items() if value}
        return Vacancy.objects.filter(**filter_).select_related('city', 'language')


class VCreate(CreateView):
    model = Vacancy
    # fields = '__all__'
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')
    form_class = VForm


class VUpdate(UpdateView):
    model = Vacancy
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')
    form_class = VForm


class VDelete(DeleteView):
    model = Vacancy
    template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
