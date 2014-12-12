# -*- coding: utf-8 -*-
 
import re
import sys
import lxml.html
import traceback
from grab import Grab
from grab.error import DataNotFound
from grab.spider import Spider, Task
from grab.tools.http import quote


class KHLSpider(Spider):
    def task_generator(self):
        # XXX
        # for char in u'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ':
        for char in u'А':
            url = u'http://www.khl.ru/players/?letter=' + quote('%s' % char)
            yield Task('players_list', url=url)

    def task_players_list(self, grab, task):
        for player_link in grab.doc.select('//td/div/a'):
            player_link = player_link.attr('href')
            assert player_link.startswith('/players') # catch this error
            # TODO: check the player in the database
            yield Task('store_player', url=u'http://www.khl.ru' + player_link)
            # XXX
            break

    def task_store_player(self, grab, task):
        data = {
            u'ru_name': None,
            u'en_name': None,
            u'Клуб': None,
            u'Вид контракта': None,
            u'Контракт до': None,
            u'Номер': None,
            u'Амплуа': None,
            u'Рост': None,
            u'Вес': None,
            u'Дата рождения': None,
            u'Возраст': None,
            u'Клубы по сезонам': None,
        }
        infotable = grab.doc.select('//div[@class="borderdiv"]/table/tbody/tr')

        avatar_div_style = infotable[0].select('td/div')[0].attr('style')
        avatar_link = re.search('url\((.*?)\)', avatar_div_style).group(1)
        avatar_url = u'http://www.khl.ru' + avatar_link

        name_div = infotable.select('td/div/h2')
        data['ru_name'] = name_div.select('br/preceding-sibling::node()').text()
        data['en_name'] = name_div.select('br/following-sibling::node()').text()

        for li in infotable.select('td/ul/li'):
            key, value = li.text.split(u':', 1)
            # TODO: Maybe store undecoded keys in datamix column ?
            assert key in data # catch this error
            data[key] = value

        # sote data
        yield Task('download_image', url=avatar_url, db_object='XXX', db_object_key='XXX')

    def task_download_image(self, grab, task):
        raise


class Grabber():
    def __init__(self, url):
        self.url = url
        self.grabber = Grab()
        self.grabber.go(url)
 
    ###### ОБЩАЯ ИНФОРМАЦИЯ О МАТЧЕ ######
    def _main_info(self):
        # Номер матча
        def _game_number():
            return int(re.findall(r'\d+', self.grabber.css_text('div.games_title > p').split('.')[0])[0])
 
        # Дата матча
        def _game_date():
            raw_date = self.grabber.css_text('div.games_title > p').split('.')[1].split(',')
            return raw_date[0] + raw_date[1]
 
        # Время проведения матча (часто бывает указано)
        def _game_time():
            raw_time = [i for i in self.grabber.css_text('div.games_title > p').split(',') if i]
            if len(raw_time) == 4:
                return raw_time[-1].lstrip()
 
        # Количество зрителей
        def _game_attendance():
            try:
                attendance = int(re.findall(r'\d+', self.grabber.css_text('div.games_title > p.games_title_more'))[0])
            except IndexError:
                return None
            return attendance
 
        # Первая команда Название
        def _first_team_name():
            return self.grabber.css_text('table.matches_protocol_main > tr.first_row > td:first-child').split('(')[0].rstrip()
 
        # Первая команда Регион
        def _first_team_region():
            try:
                region = self.grabber.css_text('table.matches_protocol_main > tr.first_row > td:first-child').split('(')[1].replace(')','')
            except IndexError:
                return None
            return region
 
        # Вторая команда Название
        def _second_team_name():
            return self.grabber.css_text('table.matches_protocol_main > tr.first_row > td:last-child').split('(')[0].rstrip()
 
        # Вторая команда Регион
        def _second_team_region():
            try:
                region = self.grabber.css_text('table.matches_protocol_main > tr.first_row > td:last-child').split('(')[1].replace(')','')
            except IndexError:
                return None
            return region
 
        # Тренер первой команды - Имя
        def _first_team_coach_name():
            try:
                name = self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.first_column').split(':')[1].strip()
            except IndexError:
                return None
            return name
 
        # Тренер второй команды - Имя
        def _second_team_coach_name():
            try:
                name = self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.right_column').split(':')[1].strip()
            except IndexError:
                return None
            return name
 
        # Счет общий
        def _game_score():
            return self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.main_column > p.count')
 
        # Счет по периодам
        def _period_scores():
            return self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.main_column > div.detail_count')
 
        # Главный судья (может быть два) - Имена
        def _chief_referee():
            try:
                referee = self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.main_column > p:nth_child(3)').split(':')[-1].strip()
            except DataNotFound:
                return None
            return referee
 
        # Линейные судьи (точно два) - Имена
        def _linesmen():
            try:
                linesmen = self.grabber.css_text('table.matches_protocol_main > tr.second_row > td.main_column > p:nth_child(4)').split(':')[-1].strip()
            except DataNotFound:
                return None
            return linesmen
 
        return {
            'game_number': _game_number(),
            'game_date': _game_date(),
            'game_time': _game_time(),
            'game_attendance': _game_attendance(),
            'first_team_name': _first_team_name(),
            'first_team_region': _first_team_region(),
            'second_team_name': _second_team_name(),
            'second_team_region': _second_team_region(),
            'first_team_coach_name': _first_team_coach_name(),
            'second_team_coach_name': _second_team_coach_name(),
            'game_score': _game_score(),
            'period_scores': _period_scores(),
            'chief_referee': _chief_referee(),
            'linesmen': _linesmen()
        }
 
    ###### ИГРОКИ ######
    def _players(self):
        def _first_team_players():
            type_dict = {
                '1': 'goalkeeper',
                '2': 'defender',
                '3': 'offender'
            }
            html = self.grabber.request().body
            players = []
            doc = lxml.html.document_fromstring(html)
            player_types = doc.cssselect('div.matches_player_statistic > table')
            counter = 0
            for player_type in player_types:
                counter += 1
                for tr in player_type.cssselect('tr'):
                    if 'class' in tr.attrib.keys() and tr.attrib['class'] == 'header':
                        continue
                    game_number = tr.cssselect('td.empty_bg')[0].text_content()
                    raw_link = tr.cssselect('td.empty_bg')[1]
                    link = raw_link.cssselect('a')[0].attrib['href'].split('/')[-2]
                    players.append({
                        'name': link,
                        'game_number': game_number,
                        'type': type_dict[str(counter)]
                    })
            self.first_team_players = players
            return players
 
        def _second_team_players():
            type_dict = {
                '1': 'goalkeeper',
                '2': 'defender',
                '3': 'offender'
            }
            html = self.grabber.request().body
            players = []
            doc = lxml.html.document_fromstring(html)
            player_types = doc.cssselect('div.matches_player_statistic > dl:last-of-type > table.matches_penalty')
            counter = 0
            for player_type in player_types:
                counter += 1
                for tr in player_type.cssselect('tr'):
                    if 'class' in tr.attrib.keys() and tr.attrib['class'] == 'header':
                        continue
                    game_number = tr.cssselect('td.empty_bg')[0].text_content()
                    raw_link = tr.cssselect('td.empty_bg')[1]
                    link = raw_link.cssselect('a')[0].attrib['href'].split('/')[-2]
                    players.append({
                        'name': link,
                        'game_number': game_number,
                        'type': type_dict[str(counter)]
                    })
            self.second_team_players = players
            return players
 
        return {
            'first_team_players': _first_team_players(),
            'seond_team_players': _second_team_players()
        }
 
    ###### ЗАБРОШЕННЫЕ ШАЙБЫ ######
    def _goals(self):
        def _find_player(number, all_players):
            for player in all_players:
                if number == player['game_number']:
                    return player['name']
 
        def _process_players(active_players_numbers, all_players):
            result = []
            for item in active_players_numbers:
                result.append(_find_player(item, all_players))
            return result
 
        def _define_looser_team(first_team_score, second_team_score, score):
            if score[0] > first_team_score:
                looser_team = 'second'
                first_team_score += 1
            else:
                looser_team = 'first'
                second_team_score += 1
            return looser_team, first_team_score, second_team_score
 
        def _define_looser_goalkeeper(looser_team,
                                      first_team_active_players_numbers,
                                      second_team_active_players_numbers,
                                      first_team_players,
                                      second_team_players):
            if looser_team == 'first':
                try:
                    id = _find_player(first_team_active_players_numbers[0], first_team_players)
                except IndexError:
                    return None
                return id
            else:
                try:
                    id = _find_player(second_team_active_players_numbers[0], second_team_players)
                except IndexError:
                    return None
                return id
 
        parity_dict = {
            u'рав.': u'равенство',
            u'бол.': u'большинство',
            u'мен.': u'меньшинство',
            u'бул.': u'буллит',
            u'': None,
        }
        html = self.grabber.request().body
        goals = []
        doc = lxml.html.document_fromstring(html)
        raw_goals = doc.cssselect('div.second_content > div.inner_content > table.matches_goals > tr')
        first_team_score = 0
        second_team_score = 0
        for item in raw_goals:
            if 'class' in item.attrib.keys() and item.attrib['class'] == 'header':
                    continue
            period = item.cssselect('td:nth-child(2)')[0].text_content().strip()
            parity = parity_dict[item.cssselect('td:nth-child(5)')[0].text_content().strip()]
            time = item.cssselect('td:nth-child(3)')[0].text_content().strip()
            scorer = item.cssselect('td:nth-child(6) > a')[0].attrib['href'].split('/')[-2]
            assistants = [
                item.cssselect('td:nth-child({position}) > a'.format(position=i))[0].attrib['href'].split('/')[-2] for i in (7, 8) if
                item.cssselect('td:nth-child({position}) > a'.format(position=i))
            ]
            _first_team_active_players_numbers = [i for i in item.cssselect('td:nth-child(9)')[0].text_content().split(',') if i]
            _second_team_active_players_numbers = [i for i in item.cssselect('td:nth-child(10)')[0].text_content().split(',') if i]
            first_team_active_players = _process_players(_first_team_active_players_numbers, self.first_team_players)
            second_team_active_players = _process_players(_second_team_active_players_numbers, self.second_team_players)
            _score = [int(i) for i in item.cssselect('td:nth-child(4)')[0].text_content().split(':')]
            _looser_team, first_team_score, second_team_score = _define_looser_team(first_team_score, second_team_score, _score)
 
            looser_goalkeeper = _define_looser_goalkeeper(_looser_team,
                                                          _first_team_active_players_numbers,
                                                          _second_team_active_players_numbers,
                                                          self.first_team_players,
                                                          self.second_team_players)
            goals.append({
                'period': period,
                'parity': parity,
                'time': time,
                'scorer': scorer,
                'assistants': assistants,
                'first_team_active_players': first_team_active_players,
                'second_team_active_players': second_team_active_players,
                'looser_goalkeeper': looser_goalkeeper
            })
        return goals
 
    ###### ШТРАФ ######
    def _penalties(self):
        def _extract_penalties(raw_penalties):
            def _define_period(penalty_time):
                minutes = int(penalty_time.split(':')[0])
                if 0 <= minutes <= 19:
                    return 1
                elif 20 <= minutes <= 39:
                    return 2
                elif 40 <= minutes <= 59:
                    return 3
                else:
                    return 4
 
            penalties = []
            for item in raw_penalties:
                penalty_time = item[0].text_content()
                if not penalty_time:
                    continue
                period = _define_period(penalty_time)
 
                try:
                    player = item[1].cssselect('a')[0].attrib['href'].split('/')[-2]
                except IndexError:
                    player = None
 
                penalty_duration = item[2].text_content()
                penalty_type = item[3].text_content().strip()
                penalties.append({
                    'penalty_time': penalty_time,
                    'period': period,
                    'player': player,
                    'penalty_duration': penalty_duration,
                    'penalty_type': penalty_type
                })
            return penalties
 
        html = self.grabber.request().body
        doc = lxml.html.document_fromstring(html)
        rows = doc.cssselect('div.second_content > div.inner_content > table.matches_penalty > tr')
        raw_penalties = []
        for row in rows:
            if 'class' in row.attrib.keys():
                continue
            tds = row.cssselect('td')
            raw_penalties.append(tds[:4])
            raw_penalties.append(tds[5:])
        return _extract_penalties(raw_penalties)
 
    def run(self):
        id = self.url.split('=')[-1]
        data = None
        exception = None
 
        try:
            data = {
                'main_info': self._main_info(),
                'players': self._players(),
                'goals': self._goals(),
                'penalties': self._penalties()
            }
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exception = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
 
        return {
            'id': id,
            'data': data,
            'exception': exception
        }
