from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base.admin import BaseAdmin, BaseMixin, NoActionMixin, NoFilterAdmin
from base.admin import DynamicDisplayFilterMixin

from .models import Player, Coach, Judge, Club, Match, CoachClub, AddressClub
from .models import MatchGoalHistory, MatchPenaltyHistory, ClubPlayer, Arena
from .models import LogoClubHistory, ClubPlayerMatch


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


class MatchAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseAdmin):
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
admin.site.register(Match, MatchAdmin)


class PlayerAdmin(DynamicDisplayFilterMixin, BaseAdmin):
    list_display = ('khl_id', 'ru_fio', 'line', 'birth_date', 'weight',
                    'height', 'url',)
admin.site.register(Player, PlayerAdmin)


class CoachClubInline(NoActionMixin, BaseMixin, admin.TabularInline):
    model = CoachClub
    extra=0

class AddressClubInline(BaseMixin, admin.TabularInline):
    model = AddressClub
    extra=0


class ClubAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseAdmin):
    inlines = (CoachClubInline, AddressClubInline)
    list_display = 'ru_title', 'site', 'url', 'arena', 'coach', 'address'
admin.site.register(Club, ClubAdmin)


for model in (Coach, Judge, Arena, AddressClub, ClubPlayer, CoachClub):
    admin.site.register(model, BaseAdmin)

admin.site.register(LogoClubHistory, NoFilterAdmin)


class HasMatchObjAdmin(NoFilterAdmin):
    readonly_fields = 'match',

for model in (MatchGoalHistory, MatchPenaltyHistory, ClubPlayerMatch):
    admin.site.register(model, HasMatchObjAdmin)