from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('search/', views.search, name='search'),
    path('<int:business_id>/detail/', views.detail, name='detail'),
    path('office/login/', views.login, name='login'),
    path('office/statistics/', views.statistics, name='statistics'),
    path('office/approve/', views.approve, name='approve'),
]

