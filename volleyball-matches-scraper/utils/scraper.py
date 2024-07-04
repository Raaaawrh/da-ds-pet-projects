from .user_agent_manager import UserAgentManager

import logging
from typing import Optional, Coroutine, Any, Dict

import random
import asyncio

from playwright.async_api import async_playwright
from playwright.async_api import Playwright, Browser, BrowserContext, Page, ProxySettings

from bs4 import BeautifulSoup


class Scraper:
    def __init__(self,
                 domain: str,
                 uam: Optional[UserAgentManager] = None,
                 min_delay: float = 2,
                 max_delay: float = 10,
                 bs4_parser: str = 'html.parser',
                 logger_level: int = logging.INFO) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logger_level)

        self.domain: str = domain.rstrip('/')
        self.min_delay: float = min_delay
        self.max_delay: float = max_delay

        self.uam: UserAgentManager = uam if uam else UserAgentManager()

        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None

        self.bs4_parser: str = bs4_parser

    async def __aenter__(self) -> 'Scraper':
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.firefox.launch(headless=True)
        except Exception as e:
            self.logger.error(
                f'Failed to initialize Playwright or launch browser: {e}.')
            if self.playwright:
                await self.playwright.stop()
            self.playwright = None
            self.browser = None
            raise
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        self.browser = None
        self.playwright = None

    async def get_page(self,
                       path: str,
                       min_delay: Optional[float] = None,
                       max_delay: Optional[float] = None):
        assert self.browser is not None, 'Browser is not initialized. Check your playwright installation.'
        min_delay = min_delay if min_delay else self.min_delay
        max_delay = max_delay if max_delay else self.max_delay

        url = f'{self.domain}/{path.strip("/")}'
        user_agent: str = self.uam.get_random_user_agent()
        proxy: Dict[str, str] = {'server': self.uam.get_proxy()}
        delay = random.uniform(min_delay, max_delay)

        self.logger.info(f'Waiting for {delay:.2f} seconds...')
        await asyncio.sleep(delay)
        self.logger.info(f'Fetching {url}...')

        content = None

        try:
            self.logger.debug(f'Applying user-agent: {user_agent}.')
            context: BrowserContext = await self.browser.new_context(user_agent=user_agent, proxy=proxy)
            page = await context.new_page()

            await page.goto(url=url, wait_until='networkidle', timeout=120_000)
            content = await page.content()
            await context.close()
            await page.close()
            self.logger.info(f'OK', extra={'color': 'green'})

        except Exception as e:
            self.logger.error(f'Error occured fetching {url} -- {e}.')

        result = BeautifulSoup(content, self.bs4_parser)
        return result, content
