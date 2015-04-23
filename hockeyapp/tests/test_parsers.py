#coding: utf-8
import base.tests

from .. import parsers
from ..models import Match, Player, Club


class HockeyAppParserTest(base.tests.BaseTest):
    blank = ''
    khl_player_id = 3582
    mhl_player_id = 22698
    mhl2_player_id = 18395
    vhl_player_id = 13228
    mhl_match_id = 44367
    mhl2_match_id = 45340
    khl_match_id = 42100
    vhl_match_id = 43031

    nbf = ( 'ru_title', 'html_body', 'url', 'count', 'detail_count', 'title')
    nnf = ( 'date', 'proccesed_time', 'home_coach_id', 'home_team_id',
            'guest_team_id', 'guest_coach_id', 'spectators',
            'home_score', 'guest_score', 'overtime_win', 'bullet_win')

    def test_parsers(self):
        ''' test hockeyapp parsers '''
        self._check_parsers()
        # creates
        self._create_club()
        self._create_players()
        #self._create_schedulers()
        #creates matches
        self._create_mhl_match()
        self._create_mhl2_match()
        self._create_khl_match()
        self._create_vhl_match()
        #updates
        self._update_mhl_match()
        self._update_mhl2_match()
        self._update_khl_match()
        self._update_vhl_match()

    def _check_parsers(self):
        ''' test parsers fucntionality'''
        # test khl player parser
        self.khl_player_data = parsers.player.KHLPlayerInfo(
                                            ).get_page(self.khl_player_id)
        self.assertIsNotNone(self.khl_player_data)
        # test mhl player parser
        self.mhl_player_data = parsers.player.MHLPlayerInfo(
                                            ).get_page(self.mhl_player_id)
        self.assertIsNotNone(self.mhl_player_data)
        # test mhl2 player parser
        self.mhl2_player_data = parsers.player.MHL2PlayerInfo(
                                            ).get_page(self.mhl2_player_id)
        self.assertIsNotNone(self.mhl2_player_data)
        # test vhl player parser
        self.vhl_player_data = parsers.player.VHLPlayerInfo(
                                            ).get_page(self.vhl_player_id)
        self.assertIsNotNone(self.vhl_player_data)
        # test mhl match parser
        self.mhl_match_data = parsers.match.HockeyMHLMatchParser(html=True,
                    absolute_url='http://mhl.khl.ru/report/272/?idgame=44367'
            ).get_page(self.mhl_match_id)
        self.assertIsNotNone(self.mhl_match_data)
        # test mhl2 match parser
        self.mhl2_match_data = parsers.match.HockeyMHL2MatchParser(html=True,
                    absolute_url='http://mhl2.khl.ru/report/274/?idgame=45340'
            ).get_page(self.mhl2_match_id)
        self.assertIsNotNone(self.mhl2_match_data)
        # test khl match parser
        self.khl_match_data = parsers.match.HockeyKHLMatchParser(html=True,
                    absolute_url='http://www.khl.ru/game/266/42100/protocol/'
            ).get_page(self.khl_match_id)
        self.assertIsNotNone(self.khl_match_data)
        # test vhl match parser
        self.vhl_match_data = parsers.match.HockeyVHLMatchParser(html=True,
                    absolute_url='http://www.vhlru.ru/report/269/?idgame=43031'
            ).get_page(self.vhl_match_id)
        self.assertIsNotNone(self.vhl_match_data)
        # test clubs parser
        self.clublink = parsers.club.KHLClubURLs().get_page()[0][:-1]
        self.assertIsNotNone(self.clublink)
        self.clubinfo = parsers.club.KHLClubInfo().get_page(self.clublink)
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
        for field in ('ru_title', 'html_body', 'url', 'site', 'contacts',
        'title'):
            self.assertNotEqual(getattr(club, field), self.blank)
        for field in ('proccesed_time', 'coach_id', 'logo_id',):# 'arena_id',):
            self.assertIsNotNone(getattr(club, field))
        self.assertEqual(club.ru_title, club.title)
        #check arena fields
        #for field in ('ru_title', 'site', 'contacts', 'tickets_url'):
            #self.assertNotEqual(getattr(club.arena, field), self.blank)
        #self.assertIsNotNone(getattr(club.arena, 'photo_id'))

    def _create_players(self):
        ''' test create players '''
        # create khl player
        self.assertEqual(Player.objects.count(), 0)
        id = self.khl_player_id
        player = Player.objects.get_or_create_player(
            khl_id=id,
            data=self.khl_player_data
        )
        self.assertEqual(Player.objects.filter(khl_id=id).count(), 1)
        #check fields
        for field in ('ru_fio', 'html_body', 'url', 'line', 'birth_date',
            'height', 'weight', 'contract_type', 'contract_to', 'number',
            'grip', 'citizenship', 'wiki_page', 'fio',
        ):
            self.assertNotEqual(getattr(player, field), self.blank)
        for field in ('proccesed_time', 'photo_id', 'citizenship_id',):
            self.assertIsNotNone(getattr(player, field))
        self.assertEqual(player.khl_id, id)
        self.assertEqual(player.ru_fio, player.fio)

        for id, data in (
            (self.mhl_player_id, self.mhl_player_data),
            (self.mhl2_player_id, self.mhl2_player_data),
            (self.vhl_player_id, self.vhl_player_data),
        ):
            player = Player.objects.get_or_create_player(khl_id=id,data=data)
            #check fields
            for field in ('ru_fio', 'html_body', 'url', 'line', 'birth_date',
                'height', 'weight', 'citizenship', 'fio',
            ):
                self.assertNotEqual(getattr(player, field), self.blank)
            for field in ('proccesed_time', 'photo_id', 'citizenship_id',):
                self.assertIsNotNone(getattr(player, field))
            self.assertEqual(player.khl_id, id)
            self.assertEqual(player.ru_fio, player.fio)

    def _create_schedulers(self):
        ''' test schedulers cretes '''
        _parsers = (#(parsers.schedule.KHLScheduleParser, 266),
                    #(parsers.schedule.VHLScheduleParser, 269),
                    #(parsers.schedule.MHLScheduleParser, 272),
                    #(parsers.schedule.MHL2ScheduleParser, 274),
        )
        for _parser, id in _parsers:
            _parser().put_data_in_db_from_page(id)

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
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
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
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
        self._check_mhl_relations(match)

    def _check_mhl_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 7)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 16)
        self.assertEqual(match.clubplayermatch_set.count(), 44)
        self.assertEqual(match.judges.count(), 1)
        self.assertEqual(match.line_judges.count(), 1)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 22)

    def _create_mhl2_match(self):
        '''
            test create mhl2 match
        '''
        self.assertEqual(Match.objects.count(), 1)
        #get first match
        match = Match.objects.get_or_create_match(**self.mhl2_match_data)
        self.assertEqual(Match.objects.count(), 2)
        #check fields
        self.assertEqual(match.khl_id, self.mhl2_match_id)
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
        self._check_mhl2_relations(match)

    def _update_mhl2_match(self):
        '''
            test update mhl2 match
        '''
        #get and update match
        match = Match.objects.get(khl_id=self.mhl2_match_id)
        parser = parsers.match.HockeyMHL2MatchParser
        match = parser().update_model_object(match)
        #check fields
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
        self._check_mhl2_relations(match)

    def _check_mhl2_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 3)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 8)
        self.assertEqual(match.clubplayermatch_set.count(), 42)
        self.assertEqual(match.judges.count(), 1)
        self.assertEqual(match.line_judges.count(), 2)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 20)

    def _create_khl_match(self):
        '''
            test create khl match
        '''
        self.assertEqual(Match.objects.count(), 2)
        #get first match
        match = Match.objects.get_or_create_match(**self.khl_match_data)
        self.assertEqual(Match.objects.count(), 3)
        #check fields
        self.assertEqual(match.khl_id, self.khl_match_id)
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
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
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
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
        self.assertEqual(Match.objects.count(), 3)
        #get first match
        match = Match.objects.get_or_create_match(**self.vhl_match_data)
        self.assertEqual(Match.objects.count(), 4)
        #check fields
        self.assertEqual(match.khl_id, self.vhl_match_id)
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
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
        for field in self.nbf:
            self.assertNotEqual(getattr(match, field), self.blank)
        for field in self.nnf:
            self.assertIsNotNone(getattr(match, field))
        self.assertEqual(match.ru_title, match.title)
        self._check_vhl_relations(match)


    def _check_vhl_relations(self, match):
        self.assertEqual(match.matchgoalhistory_set.count(), 4)
        self.assertEqual(match.matchpenaltyhistory_set.count(), 12)
        self.assertEqual(match.clubplayermatch_set.count(), 44)
        self.assertEqual(match.judges.count(), 2)
        self.assertEqual(match.line_judges.count(), 2)
        self.assertEqual(match.home_players.count(), 22)
        self.assertEqual(match.guest_players.count(), 22)