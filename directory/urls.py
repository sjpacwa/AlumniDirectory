from django.contrib import admin
from django.urls import path

from . import views

app_name = 'directory'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('search/', views.search, name='search'),
    path('<int:business_id>/detail/', views.detail, name='detail'),
    path('<int:business_id>/edit/', views.edit, name='edit'),
    path('office/login/', views.log_in, name='login'),
    path('office/statistics/', views.statistics, name='statistics'),
    path('office/approve/', views.approve, name='approve'),
    path('office/logout/', views.log_out, name='logout'),
    path('office/approve_deny/', views.approve_deny, name='approve_deny')
]

