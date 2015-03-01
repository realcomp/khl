# coding: utf-8
from __future__ import unicode_literals

import itertools

from django import forms
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_select2 import Select2MultipleWidget
from daterange_filter.filter import DateRangeFilter
from relatives.utils import object_link

from base.admin import AutocompleteFieldFilter, SimpleRangeFilter
from base.admin import BaseAdmin, NoActionMixin, NoFilterAdmin, BaseListAdmin
from base.admin import DynamicDisplayFilterMixin, TabularInlineReadOnly

from .forms import TimelineForm
from .models import Player, Coach, Judge, Club, Match, CoachClub, AddressClub
from .models import MatchGoalHistory, MatchPenaltyHistory, ClubPlayer, Arena
from .models import LogoClubHistory, ClubPlayerMatch, AdvancedPlayerStats
from .models import League, LeagueClub, PlayerCitizenship, ArenaPhotos
from .models import AddressClubPhotos, Name, Schedule, ClubTitleAlias
from .models import PlayerCoachJudge, ClubSocial, PlayerSocial, CoachSocial
from .models import JudgeSocial, ArenaInstaPhoto, Timeline


class GoalEntryInline(TabularInlineReadOnly):
    model = MatchGoalHistory
    readonly_fields = ( object_link, 'scorer', 'parity', 'time', 'period',
                        'assist', 'home_five_numbers', 'guest_five_numbers')
    fields = readonly_fields


class PenaltyEntryInline(TabularInlineReadOnly):
    model = MatchPenaltyHistory
    readonly_fields = object_link, 'player', 'ptype', 'time', 'duration'
    fields = readonly_fields


class MatchAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseListAdmin):
    suit_form_tabs = (
                ('general', _('General')),
                ('hometeam', _('Home team')),
                ('guestteam', _('Guest team')),
                ('servinfo', _('Service Info')),
    )
    list_filter = ( 'ru_title', 'home_team', 'guest_team', 'league',
                    ('date', DateRangeFilter),
    )
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('ru_title', 'en_title', 'date', 'count', 'detail_count',
                        'spectators', 'judges', 'line_judges', 'challenge_type',
                        'title',
                    )
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
            'fields': ( 'khl_id', 'url', 'html_body', 'is_championship',
                        'is_playoff')
        }),
    )

    inlines = (GoalEntryInline, PenaltyEntryInline)
    list_display = ('khl_id', 'ru_title', 'home_team', 'count',  'guest_team',
                    'date','spectators',)
    linked_readonly_fields = (      'home_team', 'guest_team', 'home_coach', 
                                    'guest_coach')
    linked_m2m_readonly_fields = (  'home_players', 'guest_players', 'judges',
                                    'line_judges',)
    readonly_fields = ('title',) + linked_readonly_fields + linked_m2m_readonly_fields

    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
admin.site.register(Match, MatchAdmin)


class ClubPlayerInline(TabularInlineReadOnly):
    model = ClubPlayer
    readonly_fields = ( object_link, 'club', 'number', 'line', 'start_date',
                        'end_date', 'season', 'league')

class PlayerCitizenshipInline(TabularInlineReadOnly):
    model = PlayerCitizenship
    readonly_fields = ( object_link, 'start_date', 'end_date',)

class PlayerSocialsInline(admin.TabularInline):
    model = PlayerSocial
    fields = ('url', 'stype')


def recalc_counters(modeladmin, request, queryset):
    from .tasks import player_recalc_counters
    pks = queryset.values_list('pk', flat=True)
    for i in range(0, len(pks), 1000):  # 1000 players per task
        player_recalc_counters.delay(pks[i:i + 1000])
recalc_counters.short_description = _('Recalculate counters')


class PlayerAdmin(DynamicDisplayFilterMixin, BaseListAdmin):
    actions = recalc_counters,
    inlines = (ClubPlayerInline, PlayerCitizenshipInline,)# PlayerSocialsInline)
    list_display = ('khl_id', 'ru_fio', 'line', 'birth_date', 'weight',
                    'height', 'url', 'ru_name', 'ru_lastname',
    )
    list_filter = ( ('khl_id', AutocompleteFieldFilter), 
                    ('ru_fio', AutocompleteFieldFilter),
                    'line', 
                    ('weight', SimpleRangeFilter),
                    ('height', SimpleRangeFilter),
                    ('birth_date', DateRangeFilter),
    )
    readonly_fields = ('fio',)
admin.site.register(Player, PlayerAdmin)


class CoachClubInline(TabularInlineReadOnly):
    model = CoachClub
    readonly_fields = ( object_link, 'coach', 'club', 'head',
                        'start_date', 'end_date', 'season')
    fields = readonly_fields

class AddressClubInline(TabularInlineReadOnly):
    model = AddressClub
    readonly_fields = ( object_link, 'club', 'start_date', 'end_date', 'season')
    fields = readonly_fields

class LeagueClubInline(TabularInlineReadOnly):
    model = LeagueClub
    readonly_fields = ( object_link, 'club', 'start_date', 'end_date', 'season')
    fields = readonly_fields

class ClubTitleAliasInline(TabularInlineReadOnly):
    model = ClubTitleAlias
    readonly_fields = ( object_link, 'club', 'alias')
    fields = readonly_fields

class ClubSocialsInline(admin.TabularInline):
    model = ClubSocial
    fields = ('url', 'stype')

class ClubAdmin(NoActionMixin, DynamicDisplayFilterMixin, BaseListAdmin):
    inlines = ( CoachClubInline, AddressClubInline, LeagueClubInline,
                ClubTitleAliasInline,)# ClubSocialsInline)
    list_display = ('ru_title', 'address', 'coach','league', 'site', 'arena',)
    linked_m2m_readonly_fields = ('players', 'coaches')
    readonly_fields = linked_m2m_readonly_fields
    list_editable = 'league',
    select_related = (  'league', 'address', 'coach', 'arena', 'farm_club',
                        'junior_club',
    )
    fields = (  'ru_title', 'en_title', 'title', 'address', 'coach', 'coaches',
                'opening_dt', 'closing_dt', 'logo', 'arena', 'league',
                'farm_club', 'junior_club', 'site', 'email', 'phone',
                'players', 'style', 'rgb',
                'vk', 'ok', 'fb', 'gl', 'tw', 'im', 'pp', 'ut')
    readonly_fields = ('title',)
admin.site.register(Club, ClubAdmin)


class ScheduleAdmin(BaseAdmin):
    linked_readonly_fields = ('match', 'home_team', 'guest_team')
    readonly_fields = linked_readonly_fields
    list_filter = ( 'league', 'home_team', 'guest_team', 'season',
                    'challenge_type', ('date', DateRangeFilter)
    )
    list_display = ('khl_id', 'league', 'home_team', 'guest_team',
                    'season', 'date',)
admin.site.register(Schedule, ScheduleAdmin)

for _model in (League, LeagueClub, CoachClub, ClubTitleAlias):
    admin.site.register(_model, BaseListAdmin)
for _model in (LogoClubHistory, PlayerCoachJudge,):
    admin.site.register(_model, NoFilterAdmin)

class ArenaPhotosInline(admin.TabularInline):
    model = ArenaPhotos
    extra=0

class ArenaInstaPhotoInline(admin.TabularInline):
    model = ArenaInstaPhoto
    extra=0

class ArenaForm(forms.ModelForm):
    club_set = forms.ModelMultipleChoiceField(label=_('Clubs'),
                queryset=Club.objects.all().order_by('ru_title'),
                widget=Select2MultipleWidget(select2_options = {'width': 'resolve', 'dropdownAutoWidth': True,}),
    )
    class Meta:
        model = Arena

class ArenaAdmin(DynamicDisplayFilterMixin, BaseListAdmin):
    inlines = (ArenaPhotosInline,)
    list_filter = ('ru_title', 'address',
                    ('capacity', SimpleRangeFilter),
    )
    list_display = ('ru_title', 'address', 'capacity', 'coords')
    readonly_fields = ('title',)
    fields = (  'title', 'ru_title', 'en_title', 'capacity', 'coords', 'site',
                'address', 'contacts', 'tickets_url', 'photo', 'club_set'
            )
    def save_model(self, request, obj, form, change):
        obj.club_set = form.cleaned_data['club_set']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['club_set'] = forms.ModelMultipleChoiceField(
                        label=_('Clubs'),
                        queryset=Club.objects.all().order_by('ru_title'),
                        initial = obj.club_set.all(),
                        widget=Select2MultipleWidget(select2_options = {'width': 'resolve', 'dropdownAutoWidth': True,}),
            )
        return super(ArenaAdmin, self).get_form(request, obj)
admin.site.register(Arena, ArenaAdmin)


class AddressClubPhotosInline(admin.TabularInline):
    model = AddressClubPhotos
    extra=0

class AddressClubAdmin(DynamicDisplayFilterMixin, BaseListAdmin):
    inlines = (AddressClubPhotosInline,)
    list_filter = ('club', 'address', 'season',)
    list_display = list_filter+('postaddress', 'email')
admin.site.register(AddressClub, AddressClubAdmin)


class JudgeMatchesInline(TabularInlineReadOnly):
    model = Match.judges.through
    verbose_name=Judge._meta.verbose_name_plural
    readonly_fields = ('match',)
    linked_readonly_fields = ('match',)
    fields = linked_readonly_fields

class LineJudgeMatchesInline(TabularInlineReadOnly):
    model = Match.line_judges.through
    verbose_name=_('Line judges')
    readonly_fields = ('match',)
    linked_readonly_fields = ('match',)
    fields = linked_readonly_fields

class JudgeSocialsInline(admin.TabularInline):
    model = JudgeSocial
    fields = ('url', 'stype')

class JudgeAdmin(BaseListAdmin):
    inlines = (JudgeMatchesInline,LineJudgeMatchesInline,)# JudgeSocialsInline)
    readonly_fields = ('fio',)
admin.site.register(Judge, JudgeAdmin)


class CoachSocialsInline(admin.TabularInline):
    model = CoachSocial
    fields = ('url', 'stype')

class CoachAdmin(BaseListAdmin):
    inlines = (CoachClubInline,CoachSocialsInline)
    readonly_fields = ('fio',)
admin.site.register(Coach, CoachAdmin)

class ClubPlayerMatchInline(TabularInlineReadOnly):
    model = ClubPlayerMatch
    readonly_fields = ( object_link, 'clubplayer', 'goals', 'assists', 'points',
                        'faceoff',  'gamingtime', 'loose_goals', 'penalty_time',
                        'pis', 'plus_minus', 'saves', 'saves_p', 'sf', 'shots',
                        'win_goals', 'winfaceoff', 'winfaceoff_p'
                    )
    fields = readonly_fields

class ClubPlayerAdmin(DynamicDisplayFilterMixin, BaseListAdmin):
    inlines = (ClubPlayerMatchInline, )
    linked_readonly_fields = ('player',)
    readonly_fields = linked_readonly_fields
    list_filter = ('club', 'line', 'number', 'season', 'league')
    list_display = ('id', 'player')+list_filter
admin.site.register(ClubPlayer, ClubPlayerAdmin)


class MatchGoalHistoryAdmin(NoFilterAdmin):
    linked_readonly_fields = 'match', 'scorer',
    linked_m2m_readonly_fields = 'assist',
    readonly_fields = linked_readonly_fields + linked_m2m_readonly_fields
admin.site.register(MatchGoalHistory, MatchGoalHistoryAdmin)


class MatchPenaltyHistoryAdmin(NoFilterAdmin):
    linked_readonly_fields = 'match', 'player',
    readonly_fields = linked_readonly_fields
admin.site.register(MatchPenaltyHistory, MatchPenaltyHistoryAdmin)


class ClubPlayerMatchAdmin(NoFilterAdmin):
    linked_readonly_fields = ('match', 'clubplayer', 'adv_stats')
    readonly_fields = linked_readonly_fields
    list_display = linked_readonly_fields

    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        return ('id',)+self.get_fields(request)
admin.site.register(ClubPlayerMatch, ClubPlayerMatchAdmin)


admin.site.register(AdvancedPlayerStats)


def import_names(modeladmin, request, queryset):
    def update_or_create_name(**kwargs):
        name, created = Name.objects.get_or_create(
            ru_name=kwargs['ru_name'], en_name=kwargs['en_name'])
        if not name.type:
            name.type = kwargs['type']
            name.save()
        return name

    q_named = Q(ru_name__isnull=False) & Q(en_name__isnull=False)
    players = Player.objects.filter(q_named)
    coaches = Coach.objects.filter(q_named)
    for type, field in (
            (0, 'name'),
            (1, 'lastname')):
        for ru_name, en_name in itertools.chain(
                players.values_list('ru_%s' % field, 'en_%s' % field),
                coaches.values_list('ru_%s' % field, 'en_%s' % field)):
            update_or_create_name(ru_name=ru_name, en_name=en_name, type=type)
import_names.short_description = _('Import Names')


def export_names(modeladmin, request, queryset):
    def swap_names(obj):
        ''' swaps first and last names '''
        obj.ru_lastname, obj.ru_name = obj.ru_name, obj.ru_lastname
        obj.en_lastname, obj.en_name = obj.en_name, obj.en_lastname

    for model in (Player, Coach):
        for type, field in (
                (0, 'ru_lastname'),  # first names
                (1, 'ru_name')):  # last names
            names = queryset.filter(type=type)
            for obj in model.objects.filter(**{
                    '%s__in' % field: names.values_list('ru_name')}):
                swap_names(obj)
                obj.save()
export_names.short_description = _('Export Names')


class NameAdmin(admin.ModelAdmin):
    actions = import_names, export_names
    list_display = 'type', 'ru_name', 'en_name'
    list_filter = 'type',
    search_fields = 'ru_name', 'en_name'
admin.site.register(Name, NameAdmin)


def generate_timeline(modeladmin, request, queryset):
    from . import tasks
    pks = Player.objects.values_list('pk', flat=True)
    for i in range(0, len(pks), 1000):  # 1000 players per task
        tasks.player_generate_timeline.delay(pks[i:i + 1000])
    # tasks.player_generate_timeline.delay([1830, 2210])  # dev mode
    # tasks.player_generate_timeline.delay(pks[0:100])  # dev mode
generate_timeline.short_description = _('Generate new timeline events')


def regenerate_timeline(modeladmin, request, queryset):
    Timeline.objects.all().delete()
    # generate_timeline(modeladmin, request, queryset)
regenerate_timeline.short_description = _('Re-generate timeline events')


class TimelineAdmin(admin.ModelAdmin):
    actions = generate_timeline, regenerate_timeline,
    form = TimelineForm
    list_display = (
        'player', 'start_date', 'end_date', 'ru_headline', 'en_headline',
        'type')
    list_filter = 'type',
    search_fields = 'ru_headline', 'en_headline', 'ru_text', 'en_text', 'tag'
admin.site.register(Timeline, TimelineAdmin)
