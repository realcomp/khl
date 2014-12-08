from django.contrib import admin

from base.admin import BaseAdmin

from .models import Player, Coach, Judge, Team, Match


for model in (Player, Coach, Judge, Team, Match):
    admin.site.register(model, BaseAdmin)