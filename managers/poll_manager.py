import time
from random import randint
from typing import Dict, Union

from dao.connections import db
from dao.models import BaseModel
from managers.exceptions import NotSupportedScraper
from scrapers.base import BaseScraper
from scrapers.items import RobloxItem
from utils.items import UrlsData
from utils.logger import Logger
from scrapers.roblox import RobloxScraper
from dao.models import ExtractProduct
from dao.operations import create_extract_product
from google_services.spreadsheet_writer import write_data_on_sheet


class PoolModuleManager:
    SCRAPERS = ('roblox',)
    PROXY: Dict[str, str] = None
    spreadsheet_saving_delay: float = 0.01

    def __init__(self, spreadsheet_id: str = None, saving_db: bool = True):
        self.spreadsheet_id = spreadsheet_id
        self._sheet_name: str = ''
        self.logger = Logger(self.__class__.__name__)
        self.saving_db = saving_db

    def run_roblox_scraping(self, urls_data: UrlsData, requests_delay: float = 0.25) -> None:
        """
        start scraping roblox, then save items to database and write to spreadsheet
        :param urls_data: UrlsData obj
        :param requests_delay: timeout before next request (in seconds)
                time.sleep(abs(requests_delay))
        """
        self._sheet_name = urls_data.sheet_name
        if requests_delay <= 0:
            requests_delay = 0.02
        if self._sheet_name and self.spreadsheet_id:
            self.logger.info('Sheet: {0} SpreadSheet: {1}'.format(self._sheet_name, self.spreadsheet_id))
        with RobloxScraper(urls_data, proxy=self.PROXY) as roblox_scraper:
            for roblox_item in roblox_scraper.start_scraping(requests_delay=requests_delay):
                scraped_data = roblox_item.dict()
                if self.saving_db:
                    self.save_to_db(roblox_scraper, **scraped_data)
                if self.spreadsheet_id and roblox_item.row_index > 1 and self._sheet_name:
                    self.extract_product_to_spreadsheet(roblox_item)
                    sheet_saving_delay = self.spreadsheet_saving_delay + randint(0, 1000) / 1000.0
                    self.logger.debug('saved to spreadsheet. ')
                    time.sleep(sheet_saving_delay)

    def save_to_db(self, scraper: BaseScraper, **scraper_data) -> BaseModel:
        if scraper.name not in self.SCRAPERS:
            raise NotSupportedScraper(
                'This scraper %s not supported with this managers for saving to db' % scraper.name)
        if not scraper_data:
            raise ValueError('Empty scraped_data for saving to db')
        if scraper.name == 'roblox':
            obj = create_extract_product(**scraper_data)
            self.logger.info('Saved to model ExtractProduct ID: ' + str(obj.id))
            return obj
        raise ValueError('Not added script for saving to db for scrapper ' + scraper.name)

    def extract_product_to_spreadsheet(self, item: Union[RobloxItem, ExtractProduct]):
        # saving data to spreadsheet
        if isinstance(item, RobloxItem):
            data = [[str(item.created_at), item.message, item.name, item.favorites, item.visits,
                     str(item.created.date()), str(item.updated.date()), item.badges_total]]
        else:
            with db:
                product = ExtractProduct.get_or_none(id=item)
                data = [[str(product.created_at), product.message, product.name, product.favorites, product.visits,
                         str(product.created.date()), str(product.updated.date()), product.badges_total]
                        ] if product else []
        if not data:
            self.logger.debug(
                f'Not found data for saving to spreadsheet ID: {self.spreadsheet_id} SHEET: {self._sheet_name}')
            return
        result = write_data_on_sheet(spreadsheet_id=self.spreadsheet_id, sheet_name=self._sheet_name, data=data,
                                     col_ranges=f'B{item.row_index}:I{item.row_index}')
        updated_range = result['responses'][0].get('updatedRange', "")
        msg = f'spreadsheet ID: {self.spreadsheet_id} SHEET: {self._sheet_name}'
        if updated_range:
            self.logger.debug(f'SpreadSheet ID: {self.spreadsheet_id} Updated range: {updated_range}')
        else:
            self.logger.warning('Updated range not found in response from google API.\n'
                                'Need checking result on ' + msg)
        self.logger.debug('Saved data to ' + msg)
