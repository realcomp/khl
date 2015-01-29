#coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from suit.widgets import SuitDateWidget

from base.admin import LinkedSelect2, select2_options

from .models import Club, LeagueClub


class ClubleaguesAddForm(forms.ModelForm):
    clubs = forms.ModelMultipleChoiceField(
                queryset=Club.objects.all().order_by('ru_title'),
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


PARSERS = (
            (1, _('MHL parser')),
            (2, _('KHL parser')),
            (3, _('VHL parser')),
            (4, _('MHL-2 parser')),
)

class MatchParserForm(forms.Form):
    parser_id = forms.ChoiceField(label=_('Parser'), choices=PARSERS)
    from_id = forms.IntegerField(_('From match khl id'), min_value=43)
    to_id = forms.IntegerField(_('To match khl id'), min_value=43, required=False)
    count = forms.IntegerField(_('Count matches'), min_value=1, required=False)
    update = forms.BooleanField(label=_('Update from db cache'), required=False)