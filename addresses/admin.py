from django.contrib import admin

from base.admin import BaseAdmin

from .models import Address, City, Country, District


for model in (Address, City, Country, District):
    admin.site.register(model, BaseAdmin)