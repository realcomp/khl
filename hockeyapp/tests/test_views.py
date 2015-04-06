# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from base.models import Season

from ..models import Arena, Club, Player, League


class ViewsTestCase(TestCase):
    PLAYER_DATA = {
        'ru_fio': 'Иванов Иван',
        'ru_name': 'Иван',
        'ru_lastname': 'Иванов',
        'en_fio': 'Ivanov Ivan',
        'en_name': 'Ivan',
        'en_lastname': 'Ivanov',
        'khl_id': 666,
        'line': 1,
        'birth_date': datetime.date(year=2000, month=12, day=31),
        'weight': '80',
        'height': '180',
        'grip': 'left',
        'number': '666',
    }
    CLUB_DATA = {
        'ru_title': 'СКА',
        'en_title': 'SKA',
        'site': 'https://google.com/',
        'contacts': '+7 999-999-99-99',
    }

    def setUp(self):
        League.objects.create(en_title='KHL')

        Season.objects.create(
            start_date=datetime.date(year=2000, month=12, day=31),
            end_date=datetime.date(year=2001, month=12, day=31))

        self.player = Player.objects.create(**self.PLAYER_DATA)

        self.club = Club.objects.create(**self.CLUB_DATA)
        self.club.arena = Arena.objects.create(
            contacts='+7 999-999-99-99')
        self.club.save()

        self.player.last_club = self.club
        self.player.save()

        self.client = Client()

    def assertEqualPlayer(self, context, obj):
        self.assertEqual(context['pk'], obj.pk)
        # TODO: set language
        # self.assertEqual(context['fio'], obj.ru_fio)
        self.assertEqual(context['name'], obj.ru_name)
        self.assertEqual(context['lastname'], obj.ru_lastname)
        # self.assertEqual(context['line'], obj.line)
        self.assertEqual(context['line_display'], obj.get_line_display())
        self.assertEqual(context['birth_date'], '31 December 2000')
        delta = relativedelta.relativedelta(
            timezone.now().date(), obj.birth_date)
        self.assertEqual(context['age'], (delta.years, delta.months))
        self.assertEqual(context['weight'], obj.weight)
        self.assertEqual(context['height'], obj.height)
        self.assertEqual(context['grip'], obj.grip)
        self.assertEqual(context['number'], obj.number)
        self.assertEqual(
            context['khl_url'],
            'http://www.khl.ru/players/%s/' % obj.khl_id)
        self.assertEqual(context['birth_date_short'], '31.12.2000')

    def assertEqualClub(self, context, obj):
        self.assertEqual(context['pk'], obj.pk)

    def test_players_search(self):
        response = self.client.get(
            reverse('hockeyapp:players-search'))
        self.assertEqual(response.status_code, 200)

    def test_players_search_api(self):
        response = self.client.get(
            reverse('hockeyapp:players-search-api'))
        self.assertEqual(response.status_code, 200)
        # self.assertEqualPlayer(response.data['results'][0], self.player)

    def test_player_names_search_api(self):
        response = self.client.get(
            reverse('hockeyapp:player-names-search-api') +
            b'?s=%s' % self.PLAYER_DATA['ru_lastname'][:2].lower())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]['lastname'], self.PLAYER_DATA['ru_lastname'])

    def test_club_titles_search_api(self):
        response = self.client.get(
            reverse('hockeyapp:club-titles-search-api') +
            b'?s=%s' % self.CLUB_DATA['ru_title'][:2].lower())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]['title'], self.CLUB_DATA['ru_title'])

    def test_player_card(self):
        response = self.client.get(
            reverse('hockeyapp:player-card', kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_indicators(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-indicators',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_coaches(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-coaches',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_partners(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-partners',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_photos(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-photos',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_communication(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-communication',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_news(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-news',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_club_list(self):
        response = self.client.get(
            reverse('hockeyapp:club-list'))
        self.assertEqual(response.status_code, 200)

    def test_club(self):
        response = self.client.get(
            reverse('hockeyapp:club', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_calendar(self):
        response = self.client.get(
            reverse('hockeyapp:club-calendar', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_stats(self):
        response = self.client.get(
            reverse('hockeyapp:club-stats', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_home(self):
        response = self.client.get(
            reverse('hockeyapp:club-home', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_photos(self):
        response = self.client.get(
            reverse('hockeyapp:club-photos', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_fanzone(self):
        response = self.client.get(
            reverse('hockeyapp:club-fanzone', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)
