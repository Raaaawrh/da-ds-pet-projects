from typing import Dict, Any

from bs4 import BeautifulSoup
from datetime import datetime
from utils.parse_utils import *

from .team import TeamInMatch

class Match:
    def __init__(self, id: int, soup: BeautifulSoup) -> None:
        self.id: int = id

        self.stage: str = None
        self.step: str = None
        self.gender: str = None
        self.no: str = None
        self.parse_stage_step_gender_no(soup)

        self.country: str = None
        self.city: str = None
        self.parse_country_city(soup)

        self.season: int = None
        self.date_and_time: datetime = None
        self.parse_season_date_and_time(soup)

        self.referee_1_name: str = None
        self.referee_1_nation: str = None
        self.referee_2_name: str = None
        self.referee_2_nation: str = None
        self.parse_referees(soup)

        self.teamA: TeamInMatch = TeamInMatch(self.id, 'A', soup)
        self.teamB: TeamInMatch = TeamInMatch(self.id, 'B', soup)

    def parse_stage_step_gender_no(self, soup: BeautifulSoup):
        # Stage, Step, Gender, No
        tmp_stage = None
        tmp_step = None
        tmp_gender = None
        tmp_no = None

        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'vbw-mu--match' in tag.get('class') and
                        'vbw-mu-finished' in tag.get('class')) if soup else None
        tmp = tmp.find('div',
                       attrs={'class': 'vbw-mu__info--details'}) if tmp else None
        tmp = tmp.get_text() if tmp else None
        tmp = tmp.replace('#', '-').split('-') if tmp else None
        tmp = [s.strip() for s in tmp] if tmp else None

        if tmp and 'Women' in tmp:
            self.gender = 'Women'
        elif tmp and 'Men' in tmp:
            self.gender = 'Men'

        if tmp and len(tmp) >= 3:
            self.stage = tmp[0]
            if len(tmp) == 4:
                self.step = tmp[1]
            self.no = text_to_int(tmp[-1])

    def parse_country_city(self, soup: BeautifulSoup) -> None:
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'vbw-mu--match' in tag.get('class') and
                        'vbw-mu-finished' in tag.get('class')) if soup else None
        # Country
        tmp_country = tmp.find('div',
                               attrs={'class': 'vbw-mu__info--country'}) if tmp else None
        self.country = tmp_country.get_text().strip() if tmp_country else None

        # City
        tmp_city = tmp.find('div',
                            attrs={'class': 'vbw-mu__info--city'}) if tmp else None
        self.city = tmp_city.get_text().strip() if tmp_city else None

    def parse_season_date_and_time(self, soup: BeautifulSoup) -> None:
        tmp = soup.find(lambda tag:
                        tag.name == 'div' and
                        tag.get('class') and
                        'vbw-mu--match' in tag.get('class') and
                        'vbw-mu-finished' in tag.get('class')) if soup else None

        # Season
        tmp_season = tmp.find('div',
                              attrs={'class': 'vbw-mu__info--season'}) if tmp else None
        self.season = text_to_int(tmp_season.get_text()) if tmp_season else None

        # Date And Time
        tmp_date_and_time = tmp.find(lambda tag:
                                     tag.name == 'div' and
                                     tag.get('class') and
                                     'vbw-mu__time-wrapper' in tag.get('class') and
                                     tag.get('data-utc-datetime')) if tmp else None
        tmp_date_and_time = tmp_date_and_time.get('data-utc-datetime').strip() if tmp_date_and_time else None
        self.date_and_time = datetime.strptime(tmp_date_and_time, '%Y-%m-%dT%XZ') if tmp_date_and_time else None

    def parse_referees(self, soup: BeautifulSoup) -> None:
        tmp_referees = soup.find('div',
                                 attrs={'class': 'vbw-referees__wrapper'}) if soup else None
        # Referee 1
        if tmp_referees:
            tmp_referee_1 = tmp_referees.find(lambda tag:
                                              tag.name == 'span' and
                                              tag.get('class') and
                                              'vbw-referees__referee' in tag.get('class') and
                                              'vbw-referees__referee--first' in tag.get('class'))
            tmp_referee_1 = tmp_referee_1.get_text() if tmp_referee_1 else None
            tmp_referee_1 = [s for s in tmp_referee_1.split(
                '(')] if tmp_referee_1 else None
            tmp_referee_1_name = text_to_name(
                tmp_referee_1[0]) if tmp_referee_1 and len(tmp_referee_1) == 2 else None
            if len(tmp_referee_1) > 1:
                tmp_referee_1_nation = text_to_name(
                    tmp_referee_1[1]) if tmp_referee_1 and len(tmp_referee_1) == 2 else None

            self.referee_1_name = tmp_referee_1_name
            self.referee_1_nation = tmp_referee_1_nation

        # Referee 2
            tmp_referee_2 = tmp_referees.find(lambda tag:
                                              tag.name == 'span' and
                                              tag.get('class') and
                                              'vbw-referees__referee' in tag.get('class') and
                                              'vbw-referees__referee--second' in tag.get('class')) if tmp_referees else None
            tmp_referee_2 = tmp_referee_2.get_text() if tmp_referee_2 else None
            tmp_referee_2 = [s.strip(')').strip() for s in tmp_referee_2.split(
                '(')] if tmp_referee_2 else None

            tmp_referee_2_name = text_to_name(
                tmp_referee_2[0]) if tmp_referee_2 and len(tmp_referee_2) == 2 else None

            if len(tmp_referee_2) > 1:
                tmp_referee_2_nation = text_to_name(
                    tmp_referee_2[1]) if tmp_referee_2 and len(tmp_referee_2) == 2 else None

            self.referee_2_name = tmp_referee_2_name
            self.referee_2_nation = tmp_referee_2_nation
        else:
            self.referee_1_name = None
            self.referee_1_nation = None
            self.referee_2_name = None
            self.referee_2_nation = None

    def get_dict(self) -> Dict[str, Any]:
        result = {}

        result['id'] = self.id
        result['stage'] = self.stage
        result['step'] = self.step
        result['gender'] = self.gender
        result['no'] = self.no
        result['country'] = self.country
        result['city'] = self.city
        result['date_and_time'] = self.date_and_time
        result['referee_1_name'] = self.referee_1_name
        result['referee_1_nation'] = self.referee_1_nation
        result['referee_2_name'] = self.referee_2_name
        result['referee_2_nation'] = self.referee_2_nation

        return result
