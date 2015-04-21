from django.core.urlresolvers import reverse


class ClubsMixin(object):
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
