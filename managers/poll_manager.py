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

    def __init__(self, spreadsheet_id: str = None):
        self.spreadsheet_id = spreadsheet_id
        self._sheet_name: str = ''
        self.logger = Logger(self.__class__.__name__)

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
                self.save_to_db(roblox_scraper, **scraped_data)
                if self.spreadsheet_id and roblox_item.row_index > 1 and self._sheet_name:
                    self.extract_product_to_spreadsheet(roblox_item)
                    sheet_saving_delay = self.spreadsheet_saving_delay + randint(0, 1000) / 1000.0
                    self.logger.debug('saved to spreadsheet. ')
                    time.sleep(sheet_saving_delay)

    def save_to_db(self, scraper: BaseScraper, **scraper_data) -> BaseModel:
        if scraper.name not in self.SCRAPERS:
            raise NotSupportedScraper('This scraper {} not supported with this managers for saving to db')
        if not scraper_data:
            raise ValueError('Empty scraped_data for saving to db')
        if scraper.name == 'roblox':
            obj = create_extract_product(**scraper_data)
            self.logger.info('Saved to model ExtractProduct ID: ' + str(obj.id))
            return obj
        raise ValueError('Not added script for saving to db for scrapper %s' % scraper.name)

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
        updated_range = result.get('updatedRange', '')
        msg = f'spreadsheet ID: {self.spreadsheet_id} SHEET: {self._sheet_name}'
        if updated_range:
            self.logger.debug('Updated range: ' + updated_range)
        else:
            self.logger.warning('Updated range not found in response from google API. \n'
                                'Need checking result on ' + msg)
        self.logger.debug('Saved data to ' + msg)


if __name__ == '__main__':
    from utils.items import UrlItem
    from config import GOOGLE_SPREADSHEET_ID

    manager = PoolModuleManager(spreadsheet_id=GOOGLE_SPREADSHEET_ID)
    manager.run_roblox_scraping(
        urls_data=UrlsData(
            data=[
                UrlItem(URL='https://www.roblox.com/games/7837709870/NFL-Shop', row_index=3),
                # UrlItem(URL='https://www.roblox.com/games/10102215973/Lil-Nas-X-Concert-Experience', row_index=4),
                # UrlItem(URL='https://www.roblox.com/games/6679274937/Vans-World', row_index=5),
                # UrlItem(URL='https://www.roblox.com/games/7619937171/Tai-Verdes-Concert-Experience', row_index=6),
                # UrlItem(URL='https://www.roblox.com/games/7462526249/NIKELAND-ZOOM-FREAK-4', row_index=7),
                # UrlItem(URL='https://www.roblox.com/games/7665858439/DJ-Party-Space-Station', row_index=8),
                # UrlItem(URL='https://www.roblox.com/games/8649501395/UPDATE-8-NFL-Tycoon', row_index=9),
                # UrlItem(URL='https://www.roblox.com/games/8523408215/Alo-Sanctuary', row_index=10),
                # UrlItem(URL='https://www.roblox.com/games/8967359816/24kGoldn-Concert-Experience', row_index=11),
                # UrlItem(URL='https://www.roblox.com/games/8209480473/Planet-Hip-Hop-Spotify-Island', row_index=12),
                # UrlItem(URL='https://www.roblox.com/games/7830918930/Gucci-Town', row_index=13),
                # UrlItem(URL='https://www.roblox.com/games/10204556059/NARS-Color-Quest', row_index=14),
                # UrlItem(URL='https://www.roblox.com/games/10057963710/George-Ezra-s-Gold-Rush-Kid-Experience', row_index=15),
                # UrlItem(URL='https://www.roblox.com/games/7603178367/Chipotle-Burrito-Builder', row_index=16),
                # UrlItem(URL='https://www.roblox.com/games/9648883891/RESORT-Festival-Tycoon', row_index=17),
                # UrlItem(URL='https://www.roblox.com/games/9524757503/iHeartLand-Music-Tycoon', row_index=18),
                # UrlItem(URL='https://www.roblox.com/games/9426082120/Samsung-Superstar-Galaxy', row_index=19),
                # UrlItem(URL='https://www.roblox.com/games/9656012212/The-VMA-Experience', row_index=20),
                # UrlItem(URL='https://www.roblox.com/games/9249776514/Givenchy-Beauty-House', row_index=21),
                # UrlItem(URL='https://www.roblox.com/games/9129288160/FASHION-SHOW-Tommy-Play', row_index=22),
                # UrlItem(URL='https://www.roblox.com/games/8526353932/McLaren-F1-Racing-Experience', row_index=23),
                # UrlItem(URL='https://www.roblox.com/games/5853107391/Stranger-Things-Starcourt-Mall', row_index=24),
                # UrlItem(URL='https://www.roblox.com/games/10980366634/Walmart-Universe-of-Play', row_index=25),
                # UrlItem(URL='https://www.roblox.com/games/10895555747/Walmart-Land', row_index=26),
                # UrlItem(URL='https://www.roblox.com/games/10602062861/Amazon-Trip-Around-the-Blox', row_index=27)
            ],
            sheet_name='Roblox'
        )
    )
