from utils import DatabaseManager, UserAgentManager, Scraper

from entities import Match
import logging

from typing import List
from tqdm.auto import tqdm

import asyncio

db_manager = DatabaseManager('../data/volleyball_world.sqlite')
user_agent_manager = UserAgentManager(
    password='password', logger_level=logging.INFO)

match_ids = list(range(1000, 1020+1))

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
                    page = await scraper.get_page(f'volleyball/competitions/volleyball-nations-league/schedule/{match_id}')
                    break
                except:
                    print (f'Exception occured fetching match #{match_id}. Retrying.')
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
