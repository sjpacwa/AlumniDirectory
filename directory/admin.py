# admin.py
# Used to register database models with the Django framework.

from django.contrib import admin

from .models import Business, Alumni

admin.site.register(Business)
admin.site.register(Alumni)
