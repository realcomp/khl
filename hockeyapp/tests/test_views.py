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
    fixtures = 'countries', 'leagues'

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
        'weight': 80,
        'height': 180,
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

    def assertEqualPlayer(self, data, obj):
        self.assertEqual(data['pk'], obj.pk)
        # TODO: set language
        self.assertEqual(data['name'], obj.ru_name)
        self.assertEqual(data['lastname'], obj.ru_lastname)
        # self.assertEqual(data['line'], obj.line)
        self.assertEqual(data['line_display'], obj.get_line_display())
        # self.assertEqual(data['birth_date'], '31 December 2000')
        delta = relativedelta.relativedelta(
            timezone.now().date(), obj.birth_date)
        self.assertEqual(data['age'], (delta.years, delta.months))
        self.assertEqual(data['weight'], obj.weight)
        self.assertEqual(data['height'], obj.height)
        self.assertEqual(data['grip'], obj.grip)
        # self.assertEqual(data['number'], obj.number)
        # self.assertEqual(
        #     data['khl_url'], 'http://www.khl.ru/players/%s/' % obj.khl_id)
        self.assertEqual(data['birth_date_short'], '31.12.2000')

    def assertEqualClub(self, context, obj):
        self.assertEqual(context['pk'], obj.pk)

    def test_players_search(self):
        response = self.client.get(
            reverse('hockeyapp:players:search'))
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
            reverse('hockeyapp:players:card', kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_api(self):
        response = self.client.get(
            reverse('hockeyapp:player-card-api', kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.data, self.player)

    def test_player_card_indicators(self):
        response = self.client.get(
            reverse('hockeyapp:players:indicators',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_coaches(self):
        response = self.client.get(
            reverse('hockeyapp:players:coaches',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_partners(self):
        response = self.client.get(
            reverse('hockeyapp:players:partners',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_photos(self):
        response = self.client.get(
            reverse('hockeyapp:players:photos',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_communication(self):
        response = self.client.get(
            reverse('hockeyapp:players:communication',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_player_card_news(self):
        response = self.client.get(
            reverse('hockeyapp:players:news',
                    kwargs={'pk': self.player.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.context_data, self.player)

    def test_club_list(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:list'))
        self.assertEqual(response.status_code, 200)

    def test_club(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:details', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_calendar(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:calendar', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_stats(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:stats', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_home(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:home', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_photos(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:photos', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_club_fanzone(self):
        response = self.client.get(
            reverse('hockeyapp:clubs:fanzone', kwargs={'pk': self.club.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqualClub(response.context_data, self.club)

    def test_country_list_api(self):
        response = self.client.get(
            reverse('hockeyapp:country-list-api') + '?s=Россия')
        self.assertEqual(response.data[0]['pk'], 1)
        self.assertEqual(response.data[0]['title'], 'Россия')
        self.assertEqual(response.status_code, 200)

    def test_country_league_list_api(self):
        response = self.client.get(
            reverse('hockeyapp:country-league-list-api'))
        self.assertEqual(response.status_code, 200)

    def test_league_list_api(self):
        response = self.client.get(
            reverse('hockeyapp:league-list-api'))
        self.assertEqual(response.status_code, 200)

    def test_player_numbers_api(self):
        response = self.client.get(
            reverse('hockeyapp:player-numbers-api'))
        self.assertEqual(response.status_code, 200)
