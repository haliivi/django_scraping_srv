from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', list_view, name='list'),
]
