from django.core.urlresolvers import reverse


class PlayersMixin(object):
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
