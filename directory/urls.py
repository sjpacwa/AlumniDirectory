# urls.py
# Contains all of the redirects for website URLs for the Django framework.

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
    path('office/approve_deny_new/', views.approve_deny_new, name='approve_deny_new'),
    path('office/approve_deny_edit/', views.approve_deny_edit, name='approve_deny_edit'),
    path('<int:business_id>/admin_delete/', views.admin_delete, name='admin_delete'),
    path('<int:business_id>/delete/', views.delete, name='delete')
]   

