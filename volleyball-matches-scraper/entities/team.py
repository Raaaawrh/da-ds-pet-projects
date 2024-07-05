from typing import Dict, List, Optional, Any

from bs4 import BeautifulSoup
from utils.parse_utils import *

from .player_statistics import PlayerStatistics
from .team_in_match_statistics import TeamInMatchStatistics


class Team:
    def __init__(self, match_id, set_no, team_letter: str, soup: BeautifulSoup) -> None:
        self.match_id: int = match_id
        self.set_no: int = set_no
        self.team_letter: str = team_letter

        self.name: int = None
        self.abbr: int = None
        self.score: int = None
        self.parse_name_abbr_score(soup)

        self.player_ids: List[Optional[int]] = []
        
        self.player_statistics: List[PlayerStatistics] = []
        self.parse_player_statistics(soup)

    def parse_name_abbr_score(self, soup: BeautifulSoup):
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'vbw-mu--match' in tag.get('class') and
                        'vbw-mu-finished' in tag.get('class')) if soup else None
        tmp = tmp.find(lambda tag:
                       tag.name == 'a' and
                       tag.get('class') and
                       'vbw-mu-finished' in tag.get('class') and
                       'vbw-mu__data' in tag.get('class')) if tmp else None

        tmp_name_abbr = tmp.find(lambda tag:
                                 tag.name == 'div' and
                                 tag.get('class') and
                                 'vbw-mu__team' in tag.get('class') and
                                 f'vbw-mu__team--{"home" if self.team_letter == "A" else "away"}' in tag.get('class')) if tmp else None
        # Name
        tmp_name = tmp_name_abbr.find(lambda tag:
                                      tag.name == 'div' and
                                      tag.get('class') and
                                      'vbw-mu__team__name' in tag.get('class') and
                                      'vbw-mu__team__name--abbr' not in tag.get('class')) if tmp_name_abbr else None
        self.name = tmp_name.get_text().strip() if tmp_name else None

        # Abbr
        tmp_abbr = tmp_name_abbr.find(lambda tag:
                                      tag.name == 'div' and
                                      tag.get('class') and
                                      'vbw-mu__team__name' in tag.get('class') and
                                      'vbw-mu__team__name--abbr' in tag.get('class')) if tmp_name_abbr else None
        self.abbr = tmp_abbr.get_text().strip() if tmp_abbr else None

        # Score
        tmp_score = tmp.find('div',
                             attrs={'class': 'vbw-mu__score--container'}) if tmp else None
        tmp_score = tmp_score.find('div',
                                   attrs={'class': f'vbw-mu__score--{"home" if self.team_letter=="A" else "away"}'}) if tmp_score else None
        self.score = text_to_int(tmp_score.get_text()) if tmp_score else None

    def parse_player_ids(self, soup):
        tmp_statistics = ['scoring', 'attack', 'block',
                          'serve', 'reception', 'dig', 'set']
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'tabs-nav' in tag.get('class') and
                        'vbw-match-stats-player--sets' in tag.get('class') and
                        '-addcontent' not in tag.get('class')) if soup else None

        for statistic in tmp_statistics:

            tmp_table = tmp.find(lambda tag:
                                 tag.name == 'table' and
                                 tag.get('class') and
                                 'vbw-o-table' in tag.get('class') and
                                 'vbw-match-player-statistic-table' in tag.get('class') and
                                 f'vbw-stats-{statistic}' in tag.get('class') and
                                 f'vbw-set-{"all" if self.set_no == 0 else str(self.set_no)}' in tag.get('class')) if tmp else None

            tmp_table = tmp_table.find('tbody',
                                       attrs={'class': 'vbw-o-table__body'}) if tmp_table else None

            tmp_table = tmp_table.find_all(lambda tag:
                                           tag.name == 'tr' and
                                           tag.get('class') and
                                           'vbw-o-table__row' in tag.get('class') and
                                           tag.get('data-player-no')) if tmp_table else []

            for tmp_row in tmp_table:
                tmp_player_id = tmp_row.find(lambda tag:
                                             tag.name == 'td' and
                                             tag.get('class') and
                                             'vbw-o-table__cell' in tag.get('class') and
                                             'playername' in tag.get('class')) if tmp_row else None

                tmp_player_id = tmp_player_id.find(lambda tag:
                                                   tag.name == 'a' and
                                                   tag.get('class') and
                                                   'vbw-mu__player' in tag.get('class') and
                                                   tag.get('href')) if tmp_player_id else None

                tmp_player_id = text_to_int(tmp_player_id.get('href').strip('/').split('/')[-1].strip('/'))

                self.player_ids.append()
                if tmp_player_id not in self.player_statistics:
                    self.player_statistics = []
                
                self.player_statistics[tmp_player_id].append(tmp_row)


    def parse_player_statistics(self, soup):
        self.player_statistics = [PlayerStatistics(
            self.match_id, self.set_no, self.name, id, soup) for id in self.player_ids]


class TeamInMatch(Team):
    def __init__(self, match_id, team_letter, soup) -> None:
        super().__init__(match_id, 0, team_letter, soup)
        self.statistics: TeamInMatchStatistics = TeamInMatchStatistics(
            match_id, self.name, team_letter, soup)


class TeamInSet(Team):
    def __init__(self, match_id, set_no, team_letter, soup) -> None:
        super().__init__(match_id, set_no, team_letter, soup)
