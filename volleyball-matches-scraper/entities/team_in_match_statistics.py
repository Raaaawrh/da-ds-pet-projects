from bs4 import BeautifulSoup

from utils.parse_utils import *


class TeamInMatchStatistics:
    def __init__(self, match_id, team_name, team_letter: str, soup: BeautifulSoup) -> None:
        self.match_id: int = match_id
        self.team_name: str = team_name
        self.__team_letter: str = team_letter

        self.attack: int = None
        self.block: int = None
        self.serve: int = None
        self.opponent_error: int = None
        self.total: int = None

        self.dig: int = None
        self.reception: int = None
        self.set: int = None

        self.parse_statistics(soup)

    def parse_statistics(self, soup) -> None:
        tmp_table = soup.find(lambda tag:
                              tag.name == 'table' and
                              tag.get('class') and
                              'vbw-o-table' in tag.get('class') and
                              'vbw-match-team-statistics' in tag.get('class') and
                              'vbw-match-team-statistics-table' in tag.get('class')) if soup else None
        if tmp_table is None:
            return
        # Attack
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'attack' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.attack = text_to_int(tmp.get_text()) if tmp else None

        # Block
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'block' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.block = text_to_int(tmp.get_text()) if tmp else None

        # Serve
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'serve' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.serve = text_to_int(tmp.get_text()) if tmp else None

        # Opponent errors
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'opponent-error' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.opponent_error = text_to_int(tmp.get_text()) if tmp else None

        # Total
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'total' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.total = text_to_int(tmp.get_text()) if tmp else None

        # Dig
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'dig' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.dig = text_to_int(tmp.get_text()) if tmp else None

        # Reception
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'reception' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.reception = text_to_int(tmp.get_text()) if tmp else None

        # Set
        tmp = tmp_table.find(lambda tag:
                             tag.name == 'tr' and
                             tag.get('class') and
                             'vbw-o-table__row' in tag.get('class') and
                             'set' in tag.get('class'))
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'stats-score' in tag.get('class') and
                       f'-td-team{self.__team_letter}' in tag.get('class')) if tmp else None
        tmp = tmp.find('span') if tmp else None
        self.set = text_to_int(tmp.get_text()) if tmp else None

