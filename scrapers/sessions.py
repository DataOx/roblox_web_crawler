from datetime import datetime
from typing import Dict

from scrapers.base import BaseScraper
from requests import Session
from requests.adapters import HTTPAdapter


class ScraperSession(BaseScraper):
    def __init__(self, proxy: Dict[str, str] = None, max_retries: int = 3):
        super().__init__()
        self.session = Session()
        self.set_retries(max_retries=max_retries)
        self.sets_proxies(proxy)
        self.start_scraping_time: datetime
        self.end_scraping_time: datetime
        self.scraped_count = 0
        self.close = self.__exit__

    def success_scraped(self) -> None:
        self.scraped_count += 1

    def set_retries(self, max_retries: int):
        self.session.mount("https://", HTTPAdapter(max_retries=max_retries))
        self.session.mount("http://", HTTPAdapter(max_retries=max_retries))

    def sets_proxies(self, proxy: Dict[str, str] = None) -> None:
        if proxy is None:
            return

        self.session.proxies = proxy

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.logger.info('Success Scraped Count: ' + str(self.scraped_count))
        self.session.close()
