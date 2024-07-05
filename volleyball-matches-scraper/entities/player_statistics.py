from typing import List, Optional

from bs4 import BeautifulSoup
from utils.parse_utils import *


class Statistics:
    _statistics = ['scoring', 'attack', 'block',
                   'serve', 'reception', 'dig', 'set']
    _features = []

    def __init__(self, match_id: int, set_no: int, player_id: int, team_name: str, team_letter: str) -> None:
        self.match_id: int = match_id
        self.set_no: int = set_no
        self.player_id: int = player_id
        self.team_name: str = team_name
        self.team_letter: str = team_letter

    def parse(self, soup: BeautifulSoup) -> None:
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'tabs-nav' in tag.get('class') and
                        'vbw-match-stats-player--sets' in tag.get('class')) if soup else None
        tmp = soup.find(lambda tag:
                        tag.name == 'table' and
                        tag.get('class') and
                        'vbw-o-table' in tag.get('class') and
                        'vbw-match-player-statistic-table' in tag.get('class') and
                        'vbw-stats-scoring' in tag.get('class') and
                        'vbw-set-all' in tag.get('class')) if tmp else None

        

        statistics = self.__class__.parse_features(soup_row)

        for attr, statistic in zip(vars(self), statistics):
            value = None
            if attr == 'efficiency_percentage':
                value = text_to_float(statistic)
            else:
                value = text_to_int(statistic)
            setattr(self, attr, value)

    @classmethod
    def parse_features(cls, soup_row: BeautifulSoup) -> List[Optional[str]]:
        result = []
        for feature in cls._features:
            tmp = soup_row.find(lambda tag:
                                tag.name == 'td' and
                                tag.get('class') and
                                'vbw-o-table__cell' in tag.get('class') and
                                feature in tag.get('class'))
            result.append(tmp.get_text().strip() if tmp else None)

        return result


class ScoringStatistics(Statistics):
    _features = ['total-abs', 'attacks', 'blocks',
                 'serves', 'errors', 'efficiency-percentage']

    def __init__(self, set_no: int,  player_id: int) -> None:
        super().__init__()

        self.total_abs: int = None
        self.attacks: int = None
        self.blocks: int = None
        self.serves: int = None
        self.errors: int = None
        self.efficiency_percentage: float = None


class AttackStatistics(Statistics):
    _features = ['point', 'errors', 'attempts',
                 'total', 'efficiency-percentage']

    def __init__(self) -> None:
        super().__init__()

        self.points: int = None
        self.errors: int = None
        self.attempts: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class BlockStatistics(Statistics):
    _features = ['point', 'errors', 'touches',
                 'total', 'efficiency-percentage']

    def __init__(self) -> None:
        super().__init__()

        self.points: int = None
        self.errors: int = None
        self.touches: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class ServeStatistics(Statistics):
    _features = ['point', 'errors', 'attempts',
                 'total', 'efficiency-percentage']

    def __init__(self) -> None:
        super().__init__()

        self.points: int = None
        self.errors: int = None
        self.attempts: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class ReceptionStatistics(Statistics):
    _features = ['successful', 'errors', 'attempts',
                 'total', 'efficiency-percentage']

    def __init__(self) -> None:
        super().__init__()

        self.successful: int = None
        self.errors: int = None
        self.attempts: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class DigStatistics(Statistics):
    _features = ['digs', 'errors', 'attempts', 'total']

    def __init__(self) -> None:
        super().__init__()

        self.digs: int = None
        self.errors: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class SetStatistics(Statistics):
    _features = ['successful', 'errors', 'attempts',
                 'total', 'efficiency-percentage']

    def __init__(self) -> None:
        super().__init__()

        self.points: int = None
        self.errors: int = None
        self.attempts: int = None
        self.total: int = None
        self.efficiency_percentage: float = None


class PlayerStatistics:
    def __init__(self, match_id: int, set_no: int, team_name: str, player_id, soup: BeautifulSoup) -> None:
        self.match_id: int = match_id
        self.set_no: int = set_no
        self.team_name: str = team_name
        self.player_id: int = player_id

        self.shirtnumber: int = None
        self.parse_shirtnumber(soup)

        self.scoring: ScoringStatistics = ScoringStatistics()
        self.attack: AttackStatistics = AttackStatistics()
        self.block: BlockStatistics = BlockStatistics()
        self.serve: ServeStatistics = ServeStatistics()
        self.reception: ReceptionStatistics = ReceptionStatistics()
        self.dig: DigStatistics = DigStatistics()
        self.set: SetStatistics = SetStatistics()

    def parse_shirtnumber(self, soup: BeautifulSoup):
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'tabs-nav' in tag.get('class') and
                        'vbw-match-stats-player--sets' in tag.get('class')) if soup else None
        tmp = tmp.find(lambda tag:
                       tag.name == 'table' and
                       tag.get('class') and
                       'vbw-o-table' in tag.get('class') and
                       'vbw-match-player-statistic-table' in tag.get('class') and
                       'vbw-stats-scoring' in tag.get('class') and
                       'vbw-set-all' in tag.get('class')) if tmp else None
        tmp = tmp.find('tbody',
                       attrs={'class': 'vbw-o-table__body'}) if tmp else None
        tmp = tmp.find(lambda tag:
                       tag.name == 'tr' and
                       tag.get('class') and
                       'vbw-o-table__row' in tag.get('class') and
                       'vbw-o-table__row--scoring' in tag.get('class') and
                       f'vbw-stats-player-{self.player_id}') if tmp else None
        tmp = tmp.find(lambda tag:
                       tag.name == 'td' and
                       tag.get('class') and
                       'vbw-o-table__cell' in tag.get('class') and
                       'shirtnumber' in tag.get('class')) if tmp else None
        self.shirtnumber = text_to_int(tmp.get_text()) if tmp else None

    def get_dict(self):
        result = {}
        result['player_id'] = self.player_id
        result['match_id'] = self.match_id
        result['set_no'] = self.set_no
        result['shirtnumber'] = self.shirtnumber
        for stat_category in ['scoring', 'attack', 'block', 'serve', 'reception', 'dig', 'set']:
            for stat in getattr(self, stat_category):
                result[f'{stat_category}_{stat}'] = getattr(
                    self, stat_category)[stat]
