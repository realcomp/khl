# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from ..models import Player


class ViewsTestCase(TestCase):
    PLAYER_DATA = {
        'ru_fio': 'Иванов Иван',
        'en_fio': 'Ivanov Ivan',
        'khl_id': 666,
        'line': 1,
        'birth_date': datetime.date(year=2000, month=12, day=31),
        'weight': '80',
        'height': '180',
        'grip': 'left',
        'number': '666',
    }

    def setUp(self):
        self.player = Player.objects.create(**self.PLAYER_DATA)
        self.client = Client()

    def assertEqualPlayer(self, context, obj):
        self.assertEqual(context['pk'], obj.pk)
        # TODO: set language
        self.assertEqual(context['fio'], obj.ru_fio)
        self.assertEqual(context['line'], obj.line)
        self.assertEqual(context['line_display'], obj.get_line_display())
        self.assertEqual(context['birth_date'], '31 December 2000')
        # self.assertEqual(context['age'], (13, 11))
        self.assertEqual(context['weight'], obj.weight)
        self.assertEqual(context['height'], obj.height)
        self.assertEqual(context['grip'], obj.grip)
        self.assertEqual(context['number'], obj.number)
        self.assertEqual(
            context['khl_url'],
            'http://www.khl.ru/players/%s/' % obj.khl_id)
        self.assertEqual(context['birth_date_short'], '31.12.2000')

    def test_players_search(self):
        response = self.client.get(
            reverse('hockeyapp:players-search'))
        self.assertEqual(response.status_code, 200)

    def test_players_search_api(self):
        response = self.client.get(
            reverse('hockeyapp:players-search-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqualPlayer(response.data['results'][0], self.player)

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
