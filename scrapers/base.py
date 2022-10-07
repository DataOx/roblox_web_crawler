import time

from utils.logger import Logger


class BaseScraper:
    name: str

    def __init__(self):
        assert self.name
        self.logger = Logger(self.__class__.__name__)

    def start_scraping(self):
        pass

    @staticmethod
    def sleep(delay: float):
        time.sleep(abs(delay))
