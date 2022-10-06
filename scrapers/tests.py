import unittest
from datetime import datetime
from urllib.parse import urlparse

from scrapers import RobloxScraper
from scrapers.items import RobloxItem

from utils.items import UrlsData, UrlItem


class TestScrapyRoblox(unittest.TestCase):
    UNIVERSE_ID = '2906645204'

    def setUp(self) -> None:
        self.url = 'https://www.roblox.com/games/9796340173/UPD-Button-Simulator-Explorers-2'
        self.parse_expected_url = urlparse(self.url)
        self.items = UrlsData(
            data=[UrlItem(URL=self.url),
                  UrlItem(URL='https://www.roblox.com/games/10753832846/NEW-AXES-Axe-Gui-Factory'),
                  UrlItem(URL='https://www.roblox.com/games/9103460924/NEW-MAP-Sword-Factory-X'),
                  UrlItem(URL='https://www.roblox.com/games/10710676163/SPTS-Origin'),
                  UrlItem(URL='https://www.roblox.com/games/5926001758/Color-Block'),
                  UrlItem(URL='https://www.roblox.com/games/4616652839/2XP-2ND-YEAR-Shindo-Life'),
                  UrlItem(URL='https://www.roblox.com/games/4995012899'),
                  UrlItem(URL='https://www.roblox.com/games/8304191830/RAID-Anime-Adventures'),
                  UrlItem(URL='https://www.roblox.com/games/10660791703/cart-ride-around-nothing'),
                  UrlItem(URL='https://www.roblox.com/games/6953291455/Eating-Simulator'),],
            sheet_name='Test'
        )
        self.scraper = RobloxScraper(self.items)

    def test_get_url_with_title(self):
        expected_url, expected_title = self.parse_expected_url.geturl(), self.parse_expected_url.path.split('/')[-1]
        result_url = self.scraper.get_url_with_title(expected_url.replace(expected_title, ''))
        self.assertTrue(result_url)
        self.assertIsInstance(result_url, str)

        parsed_result_url = urlparse(result_url)
        check_url = parsed_result_url.geturl()
        url_without_params = check_url.split('?')[0] if '?' in check_url else check_url
        self.assertEqual(url_without_params, expected_url)
        self.assertEqual(parsed_result_url.path.split('/')[-1], expected_title)

    def test_badges_search_won_ever(self):
        self.scraper.badges_search_won_ever(self.UNIVERSE_ID)
        self.assertTrue(self.scraper.badges_won_ever_set, msg='Not found won ever field value in badges data')

        for won_ever in self.scraper.badges_won_ever_set:
            self.assertIsInstance(won_ever, int)

    def test_start_scraping(self):
        self.assertTrue(self.scraper.urls_data)

        for scraped_data in self.scraper.start_scraping():
            self.assertIsInstance(scraped_data, RobloxItem)
            self.assertIsNotNone(scraped_data.row_index)
            self.assertIsNotNone(scraped_data.created)
            self.assertIsInstance(scraped_data.created, datetime)
            self.assertIsNotNone(scraped_data.updated)
            self.assertIsInstance(scraped_data.updated, datetime)
            self.assertIsNotNone(scraped_data.visits)
            self.assertIsInstance(scraped_data.visits, int)
            self.assertIsNotNone(scraped_data.badges_total)
            self.assertIsInstance(scraped_data.badges_total, int)

    def tearDown(self) -> None:
        self.scraper.close(None, None, None)


if __name__ == '__main__':
    unittest.main()
