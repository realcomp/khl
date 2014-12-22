#coding: utf-8
import base.tests

from . import parsers
from .models import Match, Player, Arena, Club


class HockeyAppTest(base.tests.BaseTest):
    blank = ''
    player_id = 4202
    match_id = 43

    def base_test(self):
        ''' base hockeapp test '''
        self._check_parsers()
        self._create_club()
        self._create_player()
        self._create_match()

    def _check_parsers(self):
        ''' test parsers fucntionality'''
        # test player parser
        self.player_data = parsers.player.GetPlayerInfo(
                                            ).get_page(self.player_id)
        self.assertIsNotNone(self.player_data)
        # test match parser
        self.match_data = parsers.match.HockeyMatchParser(html=True
                                            ).get_page(self.match_id)
        self.assertIsNotNone(self.match_data)
        # test clubs parser
        self.clublink = parsers.club.GetAllClubURLs().get_page()[0][:-1]
        self.assertIsNotNone(self.clublink)
        self.clubinfo = parsers.club.ClubInfo().get_page(self.clublink)
        self.assertIsNotNone(self.clubinfo)

    def _create_club(self):
        '''
            test create club and its arena
        '''
        self.assertEqual(Club.objects.count(), 0)
        #get club
        club = Club.objects.create_or_update_club(self.clublink, 
                                                data=self.clubinfo)
        self.assertEqual(Club.objects.count(), 1)
        #check fields
        for field in ('ru_title', 'html_body', 'url', 'site', 'contacts'):
            self.assertNotEqual(getattr(club, field), self.blank)
        for field in ('proccesed_time', 'coach_id', 'arena_id', 'logo_id'):
            self.assertIsNotNone(getattr(club, field))
        #check arena fields
        for field in ('ru_title', 'site', 'contacts', 'tickets_url'):
            self.assertNotEqual(getattr(club.arena, field), self.blank)
        self.assertIsNotNone(getattr(club.arena, 'photo_id'))

    def _create_player(self):
        ''' test create player '''
        self.assertEqual(Player.objects.count(), 0)
        #get player from khl site
        khlid = self.player_id
        player = Player.objects.get_or_create_player(
            khl_id=khlid,
            data=self.player_data
        )
        self.assertEqual(Player.objects.filter(khl_id=khlid).count(), 1)
        #check fields
        self.assertEqual(player.khl_id, khlid)
        self.assertNotEqual(player.ru_fio, self.blank)
        self.assertIsNotNone(player.line)
        self.assertNotEqual(player.birth_date, self.blank)
        self.assertNotEqual(player.height, self.blank)
        self.assertNotEqual(player.weight, self.blank)
        self.assertIsNotNone(player.photo)
        #update
        player = Player.objects.get_or_create_player(khl_id=khlid)
        self.assertEqual(Player.objects.filter(khl_id=khlid).count(), 1)
        self.assertNotEqual(player.ru_fio, self.blank)

    def _create_match(self):
        '''
            test create match
        '''
        self.assertEqual(Match.objects.count(), 0)
        #get first match
        khlid = self.match_id
        match = Match.objects.get_or_create_match(**self.match_data)
        self.assertEqual(Match.objects.count(), 1)
        #check fields
        self.assertEqual(match.khl_id, khlid)
        for field in ('ru_title', 'html_body', 'url', 'spectators', 'count',
        'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id'):
            self.assertIsNotNone(getattr(match, field))
        #check relations
        self.assertEqual(match.matchgoalhistory_set.count(), 12)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 21)
        self.assertEqual(match.judges.count(), 1)
        self.assertEqual(match.line_judges.count(), 2)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 22)