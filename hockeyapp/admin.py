from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base.admin import BaseAdmin, BaseMixin, NoActionMixin

from .models import Player, Coach, Judge, Club, Match
from .models import MatchGoalHistory, MatchPenaltyHistory, ClubPlayer


class GoalEntryInline(NoActionMixin, BaseMixin, admin.TabularInline):
    model = MatchGoalHistory
    extra=0
    readonly_fields = (  'parity', 'time', 'period', 'assist',
                'home_five_numbers', 'guest_five_numbers')
    fields = ('scorer',)+readonly_fields


class PenaltyEntryInline(NoActionMixin, BaseMixin, admin.TabularInline):
    model = MatchPenaltyHistory
    extra=0
    readonly_fields = 'ptype', 'time', 'duration'
    fields = ('player',)+readonly_fields


class MatchAdmin(NoActionMixin, BaseAdmin):
    suit_form_tabs = (
                ('general', _('General')),
                ('hometeam', _('Home team')),
                ('guestteam', _('Guest team')),
                ('servinfo', _('Service Info')),
    )
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('ru_title', 'en_title', 'date', 'count', 'detail_count',
                        'judges', 'line_judges')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-hometeam',),
            'fields': ('home_team', 'home_coach', 'home_players'),
        }), 
        (None, {
            'classes': ('suit-tab suit-tab-guestteam',),
            'fields': ('guest_team', 'guest_coach', 'guest_players'),
        }),      
        (None, {
            'classes': ('suit-tab suit-tab-servinfo',),
            'fields': ('khl_id', 'url', 'html_body',)
        }),
    )

    inlines = (GoalEntryInline, PenaltyEntryInline)
    list_display = 'khl_id', 'ru_title', 'url', 'spectators', 'date', 'count'
    readonly_fields = 'home_players', 'guest_players', 'judges', 'line_judges'

    def get_list_filter(self, request):
        if self.list_filter:
            return self.list_filter
        if self.list_display:
            return self.list_display   
        return self.get_fields(request)
        
    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
admin.site.register(Match, MatchAdmin)

for model in (Player, Coach, Judge, MatchGoalHistory, MatchPenaltyHistory,
Club, ClubPlayer):
    admin.site.register(model, BaseAdmin)