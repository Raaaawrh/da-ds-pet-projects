from typing import Set, List

from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By

import time



class Scraper:
    def __init__(self, url: str, reviews_num: int, scroll_down_pause: float = 1.0) -> None:
        self.url: str = url
        self.reviews_num: int = reviews_num
        self.scroll_down_pause: float = scroll_down_pause

        self.driver: Firefox = None
        self.reviews: List = []
        self.reviews_id: Set = set()

    def __setup_driver(self) -> None:
        options = Options()
        options.headless = True
        service = Service(GeckoDriverManager().install())
        self.driver: Firefox = webdriver.Firefox(
            service=service, options=options)

    def __parse_reviews(self):
        review_boxes = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.apphub_Card.modalContentLink')
        for review_box in review_boxes[-20:]:
            try:
                review_id = review_box.get_attribute('data-modal-content-url')
                if not review_id: continue

                review_id = '/'.join(review_id.strip('/').split('/')[-3:])

                review_date = review_box.find_element(
                    By.CSS_SELECTOR, 'div.date_posted').text
                revies_play_time = review_box.find_element(
                    By.CSS_SELECTOR, 'div.hours').text

                review_text = review_box.find_element(
                    By.CSS_SELECTOR, 'div.apphub_CardTextContent').text
                review_text = review_text.replace(review_date, '').strip()

                review_recommendation = review_box.find_element(
                    By.CSS_SELECTOR, 'div.title').text
                review = (review_date, revies_play_time,
                          review_text, review_recommendation)
                if review not in self.reviews and len(self.reviews) < self.reviews_num:
                    self.reviews.append(review)

            except Exception as e:
                print(f'Exception occured: {e}')
                continue
        

    def __scroll_down(self):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(self.scroll_down_pause)

    def scrape_reviews(self):
        self.__setup_driver()
        self.driver.get(self.url)

        reviews = []
        done = False

        while len(self.reviews) < self.reviews_num and not done:
            self.__scroll_down()
            self.__parse_reviews()

        self.driver.quit()


if __name__ == '__scraper__':
    test = Scraper('https://steamcommunity.com/app/1172470/reviews/', 20)
    test.scrape_reviews()
    print(*test.reviews)