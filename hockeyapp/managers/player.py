#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

import requests

from PIL import Image
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import F, Q, Avg, Sum

import filer

from addresses.models import Country


class PlayerQuerySet(models.QuerySet):
    b''' Менеджер игрока '''
    def get_or_create_player(self, khl_id, fio='', update=False, data=None):
        b''' получаем игрока по id со стороннего ресурса '''
        _player = self.filter(khl_id=khl_id).last()
        if not _player or update:
            if data:
                #clear data ####################################################
                for k,v in data.items(): 
                    if not v: 
                        data.pop(k, None)
                ################################################################
                data.pop('club', None)
                _ava = data.pop('ava_url', None)
                if _ava:
                    # создаем фото игрока, если нет в бд
                    data['photo'] = self._create_photo(khl_id, _ava)
                _citizenship = data.pop('citizenship', None)
                if _citizenship:
                    _func = Country.objects.get_or_create
                    data['citizenship'], _crt = _func(ru_title = _citizenship)
                if not data.get('fio') and fio:
                    data['fio'] = fio
            else:
                data = dict(khl_id=khl_id,)
                if fio:
                    data['fio']=fio
            if update and _player:
                self.filter(khl_id=_player.khl_id).update(**data)
            else:
                _player = self.create(**data)
        return _player

    def _create_photo(self, khl_id, ava_url):
        b'''создаем в БД фото игрока через django-filer
            в папке players
            В асинхронном режиме не рекомендуется использовать get_or_create
        '''
        response = requests.get(ava_url)
        if response.status_code == 200:
            _buffer = StringIO(response.content)
            img = Image.open(_buffer)
            img_name = '{}.{}'.format(khl_id,img.format)
            _folder_objects = filer.models.Folder.objects
            folder = _folder_objects.filter(name='Player photo').last()
            if not folder:
                folder = _folder_objects.create(name='Player photo')
            _file_objects = filer.models.Image.objects
            data = dict(folder=folder,
                        name=img_name,
                        is_public=True
            )
            _file = _file_objects.filter(**data).last()
            if not _file:
                _file = _file_objects.create(**data)
            _file.file.save(img_name,
                            InMemoryUploadedFile(_buffer, "image", img_name, 
                            None, _buffer.tell(), None)
            )
            _file.save()
            return _file

    def ranged_filter(self, filter_, range_):
        i = 0
        start = 0
        end = 0
        count = self.count()
        found = False
        for obj in self:
            if filter_(obj):
                found = True
                break
            i += 1
        if not found:
            return self.none()
        start = i - range_
        end = i + range_
        if i - range_ < 0:
            start = 0
            end = i + range_
            end -= i - range_
        elif i + range_ > count - 1:
            end = count - 1
            start = i - range_
            start += (count - 1) - (i + range_)
        return self[start:end + 1]

    def recalc_counters(self, fields, update_last_match_date=False):
        q_rated_matches = (
            Q(clubplayermatch__match__challenge_type__isnull=False) &
            Q(clubplayermatch__match__challenge_type__gt=0))
        q_home_matches = (
            Q(clubplayermatch__match__home_team=F('club')))
        q_guest_matches = (
            Q(clubplayermatch__match__guest_team=F('club')))
        x_home_win = {
            'where': [
                "hockeyapp_match.count ~ '^[0-9]:[0-9]' and "
                "cast(split_part(left(hockeyapp_match.count, 3), ':', 1) as integer) > "
                "cast(split_part(left(hockeyapp_match.count, 3), ':', 2) as integer)"
            ],
        }
        x_guest_win = {
            'where': [
                "hockeyapp_match.count ~ '^[0-9]:[0-9]' and "
                "cast(split_part(left(hockeyapp_match.count, 3), ':', 1) as integer) < "
                "cast(split_part(left(hockeyapp_match.count, 3), ':', 2) as integer)"
            ],
        }

        for player in self:
            clubplayers = player.clubplayer_set.filter(q_rated_matches)

            q_not_parsed_yet = Q(
                clubplayermatch__created__gt=player.last_match_date)

            if (not player.last_match_date or
                    clubplayers.filter(q_not_parsed_yet).exists() or
                    not clubplayers.exists()):
                for field in fields:
                    value = None
                    if field in (
                            'goals_total', 'assists_total', 'points_total',
                            'plus_minus_total', 'penalty_time_total',
                            'saves_total', 'loose_goals_total', 'gamingtime_total'):
                        value = clubplayers.aggregate(**{
                            field: Sum('clubplayermatch__%s' % field.replace('_total', ''))
                        }).get(field, 0) or 0
                    elif field in (
                            'goals_average', 'assists_average', 'points_average',
                            'plus_minus_average', 'penalty_time_average',
                            'saves_p_average', 'sf_average'):
                        if clubplayers.count() >= 10:
                            value = clubplayers.aggregate(**{
                                field: Avg('clubplayermatch__%s' % field.replace('_average', ''))
                            }).get(field, 0) or 0
                        else:
                            value = 0
                    elif field == 'seasons_total':
                        value = len(set(clubplayers.values_list('season')))
                    elif field == 'matches_total':
                        value = clubplayers.count()
                    elif field == 'matches_win_total':
                        value = (
                            clubplayers.filter(q_home_matches)
                            .extra(**x_home_win).count() +
                            clubplayers.filter(q_guest_matches)
                            .extra(**x_guest_win).count())
                    elif field == 'matches_lose_total':
                        value = (
                            clubplayers.filter(q_home_matches)
                            .extra(**x_guest_win).count() +
                            clubplayers.filter(q_guest_matches)
                            .extra(**x_home_win).count())
                    elif field == 'bullet_matches_total':
                        value = (
                            clubplayers
                            .filter(clubplayermatch__bullet_goals__gt=0).count())
                    elif field == 'zero_goals_matches_total':
                        value = (
                            clubplayers
                            .filter(clubplayermatch__loose_goals=0).count())
                    elif field == 'shots_received_total':
                        value = (player.saves_total or 0) + (player.loose_goals_total or 0)

                    setattr(player, field, value)

                if update_last_match_date:
                    last_cp = clubplayers.order_by('clubplayermatch__created').last()
                    if last_cp:
                        last_cpm = last_cp.clubplayermatch_set.order_by('created').last()
                        if last_cpm:
                            player.last_match_date = last_cpm.created
                            fields = list(fields) + ['last_match_date']

                player.save(update_fields=list(fields) + ['last_match_date'])

    def recalc_counters_index(self, field):
        rating_index = 0
        rating_value = None

        def less(a, b):
            ''' a < b '''
            if type(a) == float and type(b) == float:
                return round(a, 3) < round(b, 3)
            else:
                return a < b

        for player in self.order_by('-%s' % field, '-pk'):
            if (less(getattr(player, field), rating_value) or
                    rating_value is None):
                rating_index += 1
                rating_value = getattr(player, field)
            setattr(player, '%s_index' % field, rating_index)
            player.save(update_fields=('%s_index' % field,))


class ClubPlayerQuerySet(models.QuerySet):
    def by_season(self, season):
        qs = self.filter(season=season)
        # if season.is_last:
        #     end_date = min(datetime.datetime.now().date(), season.end_date)
        #     qs = qs.filter(end_date__gte=end_date)
        return qs

    def by_leagues(self, leagues):
        return self.filter(league__in=leagues)
