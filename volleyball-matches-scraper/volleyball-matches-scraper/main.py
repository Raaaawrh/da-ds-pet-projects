from os import environ
from utils import DatabaseManager, UserAgentManager, Scraper

from entities import Match
import logging

from typing import List
from tqdm.auto import tqdm

import asyncio

import logging
logging.getLogger('stem').setLevel(logging.CRITICAL)

import os.path

# Get environment variables
try:
    match_id_min: int = int(environ['MATCH_ID_MIN'])
    match_id_max: int = int(environ['MATCH_ID_MAX'])
except ValueError as e:
    print(f'Wrong MATCH_ID limits. Fallback to default 15000...16000. \n{e}')

db_name = str(environ['DB_NAME'])

match_id_min=15000
match_id_max=16000

if match_id_min > match_id_max:
    print('Passed Match ID minimal is greater than Match ID maximum. Automatically exchanged.')
    match_id_min, match_id_max = match_id_max, match_id_min

# Create Database and User Agent managers
db_path = os.path.abspath(f'data/{db_name}')
db_manager = DatabaseManager(db_path)
user_agent_manager = UserAgentManager(logger_level=logging.INFO)

match_ids = list(range(match_id_min, match_id_max+1))


async def main(match_ids: List[str]):
    page = None

    async with Scraper(domain='https://en.volleyballworld.com/',
                       uam=user_agent_manager,
                       min_delay=2,
                       max_delay=5,
                       logger_level=logging.INFO) as scraper:
        for match_id in tqdm(match_ids):
            while True:
                try:
                    page = (await scraper.get_page(f'volleyball/competitions/volleyball-nations-league/schedule/{match_id}'))[0]
                    break
                except:
                    print(
                        f'Exception occured fetching match #{match_id}. Retrying.')
            match_obj = Match(match_id, page)
            match_info = match_obj.get_match_info()
            teams_in_match_info = match_obj.get_team_in_match_info()
            teams_in_set_info = match_obj.get_team_in_set_info()
            players_statistics = match_obj.get_players_results_info()

            db_manager.insert(match_info=match_info,
                              teams_in_match_info=teams_in_match_info,
                              teams_in_set_info=teams_in_set_info,
                              players_statistics=players_statistics)

if __name__ == '__main__':
    asyncio.run(main(match_ids=match_ids))
