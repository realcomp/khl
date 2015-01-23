#coding: utf-8
import base.tests

from .. import parsers
from ..models import Match, Player, Club


class HockeyAppTest(base.tests.BaseTest):
    blank = ''
    player_id = 3582
    mhl_match_id = 44367
    khl_match_id = 42100
    vhl_match_id = 43031

    def base_test(self):
        ''' base hockeapp test '''
        self._check_parsers()
        #creates
        self._create_club()
        self._create_player()
        self._create_mhl_match()
        self._create_khl_match()
        self._create_vhl_match()
        #updates
        self._update_mhl_match()
        self._update_khl_match()
        self._update_vhl_match()

    def _check_parsers(self):
        ''' test parsers fucntionality'''
        # test player parser
        self.player_data = parsers.player.GetPlayerInfo(
                                            ).get_page(self.player_id)
        self.assertIsNotNone(self.player_data)
        # test mhl match parser
        self.mhl_match_data = parsers.match.HockeyMHLMatchParser(html=True
                                                ).get_page(self.mhl_match_id)
        self.assertIsNotNone(self.mhl_match_data)
        # test khl match parser
        self.khl_match_data = parsers.match.HockeyKHLMatchParser(html=True
                                                ).get_page(self.khl_match_id)
        self.assertIsNotNone(self.khl_match_data)
        # test vhl match parser
        self.vhl_match_data = parsers.match.HockeyVHLMatchParser(html=True
                                                ).get_page(self.vhl_match_id)
        self.assertIsNotNone(self.khl_match_data)
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
        for field in ('ru_fio', 'html_body', 'url', 'line', 'birth_date',
            'height', 'weight', 'contract_type', 'contract_to', 'number',
            'grip', 'birth_date', 'citizenship', 'wiki_page',
        ):
            self.assertNotEqual(getattr(player, field), self.blank)
        for field in ('proccesed_time', 'photo_id', 'citizenship_id',):
            self.assertIsNotNone(getattr(player, field))
        self.assertEqual(player.khl_id, khlid)
        #update
        player = Player.objects.get_or_create_player(khl_id=khlid)
        self.assertEqual(Player.objects.filter(khl_id=khlid).count(), 1)
        self.assertNotEqual(player.ru_fio, self.blank)

    def _create_mhl_match(self):
        '''
            test create mhl match
        '''
        self.assertEqual(Match.objects.count(), 0)
        #get first match
        match = Match.objects.get_or_create_match(**self.mhl_match_data)
        self.assertEqual(Match.objects.count(), 1)
        #check fields
        self.assertEqual(match.khl_id, self.mhl_match_id)
        for field in ('ru_title', 'html_body', 'url', 'count', 'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id', 'spectators'):
            self.assertIsNotNone(getattr(match, field))
        self._check_mhl_relations(match)

    def _update_mhl_match(self):
        '''
            test update mhl match
        '''
        #get and update match
        match = Match.objects.get(khl_id=self.mhl_match_id)
        parser = parsers.match.HockeyMHLMatchParser
        match = parser().update_model_object(match)
        #check fields
        for field in ('ru_title', 'html_body', 'url', 'spectators', 'count',
        'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id'):
            self.assertIsNotNone(getattr(match, field))
        self._check_mhl_relations(match)

    def _check_mhl_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 7)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 16)
        self.assertEqual(match.clubplayermatch_set.count(), 44)
        self.assertEqual(match.judges.count(), 1)
        self.assertEqual(match.line_judges.count(), 1)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 22)

    def _create_khl_match(self):
        '''
            test create khl match
        '''
        self.assertEqual(Match.objects.count(), 1)
        #get first match
        match = Match.objects.get_or_create_match(**self.khl_match_data)
        self.assertEqual(Match.objects.count(), 2)
        #check fields
        self.assertEqual(match.khl_id, self.khl_match_id)
        for field in ('ru_title', 'html_body', 'url', 'count', 'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id', 'spectators'):
            self.assertIsNotNone(getattr(match, field))
        self._check_khl_relations(match)

    def _update_khl_match(self):
        '''
            test update khl match
        '''
        #get and update match
        match = Match.objects.get(khl_id=self.khl_match_id)
        parser = parsers.match.HockeyKHLMatchParser
        match = parser().update_model_object(match)
        #check fields
        for field in ('ru_title', 'html_body', 'url', 'spectators', 'count',
        'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id'):
            self.assertIsNotNone(getattr(match, field))
        self._check_khl_relations(match)

    def _check_khl_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 8)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 9)
        self.assertEqual(match.clubplayermatch_set.count(), 41)
        self.assertEqual(match.judges.count(), 2)
        self.assertEqual(match.line_judges.count(), 2)
        self.assertEqual(match.home_players.count(), 21)
        self.assertEqual(match.guest_players.count(), 20)

    def _create_vhl_match(self):
        '''
            test create vhl match
        '''
        self.assertEqual(Match.objects.count(), 2)
        #get first match
        match = Match.objects.get_or_create_match(**self.vhl_match_data)
        self.assertEqual(Match.objects.count(), 3)
        #check fields
        self.assertEqual(match.khl_id, self.vhl_match_id)
        for field in ('ru_title', 'html_body', 'url', 'count', 'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id', 'spectators'):
            self.assertIsNotNone(getattr(match, field))
        self._check_vhl_relations(match)


    def _update_vhl_match(self):
        '''
            test update vhl match
        '''
        #get and update match
        match = Match.objects.get(khl_id=self.vhl_match_id)
        parser = parsers.match.HockeyVHLMatchParser
        match = parser().update_model_object(match)
        #check fields
        for field in ('ru_title', 'html_body', 'url', 'spectators', 'count',
        'detail_count'):
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in ('proccesed_time', 'home_coach_id', 'home_team_id',
        'guest_team_id', 'guest_coach_id'):
            self.assertIsNotNone(getattr(match, field))
        self._check_vhl_relations(match)


    def _check_vhl_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 4)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 12)
        self.assertEqual(match.clubplayermatch_set.count(), 44)
        self.assertEqual(match.judges.count(), 2)
        self.assertEqual(match.line_judges.count(), 2)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 22)