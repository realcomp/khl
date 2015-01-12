from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from daterange_filter.filter import DateRangeFilter
from relatives.utils import object_link

from base.admin import BaseAdmin, NoActionMixin, NoFilterAdmin
from base.admin import DynamicDisplayFilterMixin, TabularInlineReadOnly
from base.admin import Select2MultipleWidget, select2_options

from .models import Player, Coach, Judge, Club, Match, CoachClub, AddressClub
from .models import MatchGoalHistory, MatchPenaltyHistory, ClubPlayer, Arena
from .models import LogoClubHistory, ClubPlayerMatch, AdvancedPlayerStats
from .models import League, LeagueClub, PlayerCitizenship


class GoalEntryInline(TabularInlineReadOnly):
    model = MatchGoalHistory
    readonly_fields = ( object_link, 'scorer', 'parity', 'time', 'period',
                        'assist', 'home_five_numbers', 'guest_five_numbers')
    fields = readonly_fields


class PenaltyEntryInline(TabularInlineReadOnly):
    model = MatchPenaltyHistory
    readonly_fields = object_link, 'player', 'ptype', 'time', 'duration'
    fields = readonly_fields


class MatchAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseAdmin):
    suit_form_tabs = (
                ('general', _('General')),
                ('hometeam', _('Home team')),
                ('guestteam', _('Guest team')),
                ('servinfo', _('Service Info')),
    )
    list_filter = ( ('date', DateRangeFilter),
                    'ru_title', 'home_team', 'guest_team', 'league',               
    )
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('ru_title', 'en_title', 'date', 'count', 'detail_count',
                        'spectators', 'judges', 'line_judges')
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
    list_display = ('khl_id', 'ru_title', 'home_team', 'count',  'guest_team',
                    'date','spectators',)
    linked_readonly_fields = (      'home_team', 'guest_team', 'home_coach', 
                                    'guest_coach')
    linked_m2m_readonly_fields = (  'home_players', 'guest_players', 'judges',
                                    'line_judges',)
    readonly_fields = linked_readonly_fields + linked_m2m_readonly_fields

    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
admin.site.register(Match, MatchAdmin)


class ClubPlayerInline(TabularInlineReadOnly):
    model = ClubPlayer
    readonly_fields = ( object_link, 'club', 'number', 'line', 'start_date',
                        'end_date',)

class PlayerCitizenshipInline(TabularInlineReadOnly):
    model = PlayerCitizenship
    readonly_fields = ( object_link, 'start_date', 'end_date',)

class PlayerAdmin(DynamicDisplayFilterMixin, BaseAdmin):
    inlines = (ClubPlayerInline, PlayerCitizenshipInline)
    list_display = ('khl_id', 'ru_fio', 'line', 'birth_date', 'weight',
                    'height', 'url',
    )
    list_filter = ( ('birth_date', DateRangeFilter),
                    'khl_id', 'ru_fio', 'line', 'weight', 'height',
    )
admin.site.register(Player, PlayerAdmin)


class CoachClubInline(TabularInlineReadOnly):
    model = CoachClub
    readonly_fields = ( object_link, 'coach', 'club', 'head',
                        'start_date', 'end_date')
    fields = readonly_fields

class AddressClubInline(TabularInlineReadOnly):
    model = AddressClub
    readonly_fields = ( object_link, 'club', 'start_date', 'end_date')
    fields = readonly_fields

class LeagueClubInline(TabularInlineReadOnly):
    model = LeagueClub
    readonly_fields = ( object_link, 'club', 'start_date', 'end_date')
    fields = readonly_fields

class ClubAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseAdmin):
    inlines = (CoachClubInline, AddressClubInline, LeagueClubInline)
    list_display = ('ru_title', 'site', 'url', 'arena', 'coach', 'address',
                    'league',
    )
    linked_m2m_readonly_fields = ('players',)
    readonly_fields = linked_m2m_readonly_fields
    list_editable = 'league',
    select_related = (  'league', 'address', 'coach', 'arena', 'farm_club',
                        'junior_club',
    )
admin.site.register(Club, ClubAdmin)


for model in (Arena, Judge, League, AddressClub, LeagueClub, CoachClub,):
    admin.site.register(model, BaseAdmin)

admin.site.register(LogoClubHistory, NoFilterAdmin)

class CoachAdmin(BaseAdmin):
    inlines = (CoachClubInline,)
admin.site.register(Coach, CoachAdmin)

class ClubPlayerMatchInline(TabularInlineReadOnly):
    model = ClubPlayerMatch
    readonly_fields = ( object_link, 'bullet_goals', 'clubplayer', 'es_goals',
                        'ev_goals', 'faceoff',  'gamingtime', 'loose_goals',
                        'overtime_goals', 'penalty_time', 'pis', 'plus_minus',
                        'pp_goals', 'saves', 'saves_p', 'sf', 'shots',
                        'win_goals', 'winfaceoff', 'winfaceoff_p'
                    )
    fields = readonly_fields

class ClubPlayerAdmin(BaseAdmin):
    inlines = (ClubPlayerMatchInline, )
    linked_readonly_fields = ('player',)
    readonly_fields = linked_readonly_fields
admin.site.register(ClubPlayer, ClubPlayerAdmin)


class HasMatchObjAdmin(NoFilterAdmin):
    readonly_fields = 'match',

for model in (MatchGoalHistory, MatchPenaltyHistory):
    admin.site.register(model, HasMatchObjAdmin)


class ClubPlayerMatchAdmin(NoFilterAdmin):
    linked_readonly_fields = ('match', 'clubplayer', 'adv_stats')
    readonly_fields = linked_readonly_fields
admin.site.register(ClubPlayerMatch, ClubPlayerMatchAdmin)

admin.site.register(AdvancedPlayerStats)