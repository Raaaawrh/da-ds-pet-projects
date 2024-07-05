from datetime import datetime, date


from bs4 import BeautifulSoup
from utils.parse_utils import *


class Player:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.name: int = None
        self.position: str = None
        self.nationality: str = None
        self.birth_date: datetime.date = None
        self.height: int = None

    def parse(self, soup_player_page: BeautifulSoup) -> None:
        tmp = soup_player_page.find(lambda tag:
                                    tag.name == 'div' and
                                    tag.get('class') and
                                    'vbw-player-bio-wrap' in tag.get('class') and
                                    '--section-wrap' in tag.get('class')) if soup_player_page else None
        if tmp is None:
            return

        # Name
        tmp_name = tmp.find('span', attrs={'class': 'vbw-player-name'})
        tmp_name = tmp_name.get_text().strip() if tmp_name else None
        self.name = tmp_name

        # Position
        tmp_position = tmp.find(lambda tag:
                                tag.name == 'div' and
                                tag.get('class') and
                                'vbw-player-bio-col' in tag.get('class') and
                                'position' in tag.get_text().lower())
        tmp_position = tmp_position.find(lambda tag:
                                         tag.name == 'div' and
                                         tag.get('class') and
                                         'vbw-player-bio-text' in tag.get('class') and
                                         '--desktop' in tag.get('class')) if tmp_position else None
        tmp_position = tmp_position.get_text().strip() if tmp_position else None
        tmp_position = tmp_position if tmp_position and tmp_position != '-' else None
        self.position = tmp_position

        # Nationality

        tmp_nationality = tmp.find(lambda tag:
                                   tag.name == 'div' and
                                   tag.get('class') and
                                   'vbw-player-bio-col' in tag.get('class') and
                                   'nationality' in tag.get_text().lower())
        tmp_nationality = tmp_nationality.find(lambda tag:
                                               tag.name == 'div' and
                                               tag.get('class') and
                                               'vbw-player-bio-text' in tag.get('class') and
                                               '--desktop' in tag.get('class')) if tmp_nationality else None
        tmp_nationality = tmp_nationality.get_text().strip() if tmp_nationality else None
        tmp_nationality = tmp_nationality if tmp_nationality and tmp_nationality != '-' else None
        self.nationality = tmp_nationality

        # Birth Date
        tmp_birth_date = tmp.find(lambda tag:
                                  tag.name == 'div' and
                                  tag.get('class') and
                                  'vbw-player-bio-col' in tag.get('class') and
                                  'birth date' in tag.get_text().lower())
        tmp_birth_date = tmp_birth_date.find('div',
                                             attrs={'class': 'vbw-player-bio-text'}) if tmp_birth_date else None
        
        tmp_birth_date = tmp_birth_date.get_text().strip() if tmp_birth_date else None
        tmp_birth_date = tmp_birth_date if tmp_birth_date and tmp_birth_date != '-' else None
        self.birth_date = datetime.strptime(
            tmp_birth_date, '%d/%m/%Y').date() if tmp_birth_date else None

        # Height
        tmp_height = tmp.find(lambda tag:
                              tag.name == 'div' and
                              tag.get('class') and
                              'vbw-player-bio-col' in tag.get('class') and
                              'height' in tag.get_text().lower())
        tmp_height = tmp_height.find('div',
                                     attrs={'class': 'vbw-player-bio-text'}) if tmp_height else None
        tmp_height = tmp_height.get_text() if tmp_height else None
        self.height = text_to_int(tmp_height)
