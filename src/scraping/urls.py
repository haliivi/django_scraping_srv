from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    # path('list/', list_view, name='list'),
    path('create/', VCreate.as_view(), name='create'),
    path('update/<int:pk>', VUpdate.as_view(), name='update'),
    path('delete/<int:pk>', VDelete.as_view(), name='delete'),
    path('list/', VList.as_view(), name='list'),
    # path('list/detail/<int:pk>/', v_detail, name='detail')
    path('list/detail/<int:pk>/', VDetail.as_view(), name='detail')
]
