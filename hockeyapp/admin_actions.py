# -*- coding: utf-8 -*-
import itertools

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


def get_recalc_counters_actions():
    '''
    admin actions generator
    '''
    fields = (
        'seasons_total', 'matches_total', 'bullet_matches_total',
        'shots_received_total', 'saves_total', 'loose_goals_total',
        'saves_p_average', 'sf_average', 'zero_goals_matches_total',
        'matches_win_total', 'matches_lose_total', 'gamingtime_total',
    ) + tuple(itertools.chain(*map(
        lambda x: ('%s_total' % x, '%s_average' % x),
        ('goals', 'assists', 'points', 'plus_minus', 'penalty_time'))))

    def get_action(field):
        def action(modeladmin, request, queryset):
            from .tasks import player_recalc_counters
            from .tasks import player_recalc_counters_index
            pks = queryset.values_list('pk', flat=True)
            player_recalc_counters.delay(pks, [field])
            player_recalc_counters_index.delay(field)
        # make function unique for django
        action.__name__ = str('action_%s' % field)
        action.short_description = _('Recalculate counters for "%s"') % field
        return action

    for field in fields:
        yield get_action(field)

    def action_all(modeladmin, request, queryset):
        from .tasks import periodic_player_recalc_counters
        from .tasks import periodic_player_recalc_counters_index
        periodic_player_recalc_counters.delay()
        periodic_player_recalc_counters_index.delay()
    action_all.short_description = _('Recalculate all counters')
    yield action_all

    def reset_last_match_date(modeladmin, request, queryset):
        queryset.update(last_match_date=None)
    reset_last_match_date.short_description = _('Reset "last_match_date"')
    yield reset_last_match_date


def import_names(modeladmin, request, queryset):
    from .models import Name, Player, Coach

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
    from .models import Name, Player, Coach

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


def regenerate_timeline(modeladmin, request, queryset):
    queryset.model.objects.all().delete()
    # generate_timeline(modeladmin, request, queryset)
regenerate_timeline.short_description = _('Re-generate timeline events')


def generate_timeline(modeladmin, request, queryset):
    from . import tasks
    from .models import Player

    pks = Player.objects.values_list('pk', flat=True)
    for i in range(0, len(pks), 1000):  # 1000 players per task
        tasks.player_generate_timeline.delay(pks[i:i + 1000])
    # tasks.player_generate_timeline.delay([1830, 2210])  # dev mode
    # tasks.player_generate_timeline.delay(pks[0:100])  # dev mode
generate_timeline.short_description = _('Generate new timeline events')


def calculate_similarity(modeladmin, request, queryset):
    from .models import RelatedPlayer
    RelatedPlayer.calc(queryset, queryset)
calculate_similarity.short_description = _(
    'Calculate similarity between selected')


def calculate_similarity_everyone(modeladmin, request, queryset):
    # from .models import RelatedPlayer
    # RelatedPlayer.calc(queryset, queryset.model.objects.all())
    from . import tasks
    for pk in queryset.values_list('pk', flat=True):
        tasks.relatedplayer_calc_player.delay(pk)
calculate_similarity.short_description = _(
    'Calculate similarity between selected and everyone')
