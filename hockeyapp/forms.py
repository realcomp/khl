#coding: utf-8
from __future__ import unicode_literals

from django import forms

from django_select2.widgets import Select2MultipleWidget
from suit.widgets import SuitDateWidget

from base.admin import LinkedSelect2, select2_options

from .models import Club, LeagueClub


class ClubleaguesAddForm(forms.ModelForm):
    clubs = forms.ModelMultipleChoiceField(
                queryset=Club.objects.filter(league__isnull=True),
                widget=Select2MultipleWidget(select2_options=select2_options),
    )
    class Meta:
        model = LeagueClub
        fields = 'league', 'start_date', 'end_date'
        widgets = {
            'clubs': Select2MultipleWidget(select2_options=select2_options),
            'league': LinkedSelect2(select2_options=select2_options),
            'start_date': SuitDateWidget,
            'end_date': SuitDateWidget,
        }