#coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from suit.widgets import SuitDateWidget

from base.admin import LinkedSelect2, select2_options

from .models import Club, LeagueClub


class ClubleaguesAddForm(forms.ModelForm):
    clubs = forms.ModelMultipleChoiceField(
                queryset=Club.objects.filter(league__isnull=True),
                widget=FilteredSelectMultiple(
                                    verbose_name=Club._meta.verbose_name_plural,
                                    is_stacked=False,
                                    attrs={'style': 'height:400px;'}
                ),
    )
    class Meta:
        model = LeagueClub
        fields = 'league', 'season'
        widgets = {
            'league': LinkedSelect2(select2_options=select2_options),
            'start_date': SuitDateWidget,
            'end_date': SuitDateWidget,
        }