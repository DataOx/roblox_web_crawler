from urllib.parse import urlparse
from typing import Dict, Any, List, Optional, Iterator

from requests import Request

from utils.items import UrlsData
from roblox_api.apis import RobloxGamesAPI, RobloxBadgesAPI
from roblox_api.exceptions import RobloxException
from scrapers.items import RobloxItem
from scrapers.sessions import ScraperSession


class RobloxScraper(ScraperSession):
    name = 'roblox'

    def __init__(self, urls_data: UrlsData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls_data = urls_data.data
        self.games_api = RobloxGamesAPI(session=self.session)
        self.badges_api = RobloxBadgesAPI(session=self.session)
        self.badges_won_ever_set = set()

    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        self.games_api.on_close()
        self.badges_api.on_close()
        total_get_requests_count = self.games_api.get_requests_count + self.badges_api.get_requests_count
        if total_get_requests_count > 0:
            self.logger.debug('GET Requests count: ' + str(total_get_requests_count))
        total_post_requests_count = self.games_api.post_requests_count + self.badges_api.post_requests_count
        if total_post_requests_count > 0:
            self.logger.debug('POST Requests count: ' + str(total_post_requests_count))
        retries_total_count = self.games_api.retries_requests_count + self.badges_api.retries_requests_count
        if retries_total_count > 0:
            self.logger.debug('Retries requests Count: ' + str(retries_total_count))
        total_requests_count = self.games_api.total_requests_count + self.badges_api.total_requests_count
        if total_requests_count > 0:
            self.logger.info('Total requests count: ' + str(total_requests_count))

    def raise_error(self, msg):
        self.logger.error(msg)
        raise RobloxException(msg)

    def start_scraping(self, requests_delay: float = 0.25) -> Iterator[RobloxItem]:
        self.logger.info('Start scraping...')
        self.logger.info('URLS Count: ' + str(len(self.urls_data)))

        for url_data in self.urls_data:
            url = url_data.URL
            # 1 getting title of game for searching
            if len(self.get_path_list(url)) < 3:
                url = self.get_url_with_title(url.replace(urlparse(url).path.split('/')[-1], ''))
            url_paths = self.get_path_list(url)
            url_title, place_id = url_paths[-1], int(url_paths[-2])
            try:
                # 2 searching and filtering game data by title
                search_result = self.games_api.get_games_list(keyword=url_title)
                self.sleep(requests_delay)
                game_meta_data = self.get_game_data_by_place_id(place_id, search_result.get('games', []))
                if game_meta_data is None:
                    self.raise_error(f'Not Found meta data of game by Place ID: {place_id}')

                universe_id, game_official_name = game_meta_data.get('universeId'), game_meta_data.get('name')
                # 3 getting game info details by universe id
                games_info = self.games_api.get_games(universeIds=universe_id)
                game_info = self.get_game_details_by_universe_id(universe_id=universe_id,
                                                                 games_info=games_info.get('data', []))
                if game_info is None:
                    self.raise_error(f'Data of game details not found! Place ID: {place_id}')

                self.sleep(requests_delay)
                # 4 searching and adding won ever field value to self.badges_won_ever_set after clearing
                self.badges_won_ever_set.clear()
                self.badges_search_won_ever(universe_id=universe_id, requests_delay=requests_delay)
            except RobloxException as roblox_error:
                yield RobloxItem(message=roblox_error.msg, url=url, row_index=url_data.row_index)
                continue
            # 5 create a RobloxItem object and pull out all the data
            item = RobloxItem(message='Success', url=url, name=game_official_name,
                              row_index=url_data.row_index, created=game_info['created'],
                              updated=game_info['updated'], visits=game_info.get('visits', 0),
                              favorites=game_info.get('favoritedCount', 0),
                              badges_total=max(self.badges_won_ever_set) if self.badges_won_ever_set else 0)
            self.success_scraped()
            yield item
        self.logger.info('Over scraping Roblox!')

    def badges_search_won_ever(self, universe_id, next_page_cursor: str = None, requests_delay: float = 0.01) -> None:
        # saving found field won ever value to the list self.badges_won_list
        badges = self.badges_api.get_badges_by_universe_id(universe_id=universe_id, cursor=next_page_cursor)
        for badge_data in badges.get('data'):
            self.badges_won_ever_set.add(badge_data['statistics']['awardedCount'])
        cursor = badges.get('nextPageCursor')
        if cursor:
            self.sleep(requests_delay)
            self.badges_search_won_ever(universe_id, next_page_cursor=cursor)

    def get_url_with_title(self, url: str) -> str:
        """
        to get the title, you need to send a request to the page with the number after games
        ex: https://www.roblox.com/games/7462526249
        so that the site redirects to the url with the title
        """
        request = Request(url=url, method='GET')
        request.headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                                        ' Chrome/105.0.0.0 Safari/537.36'
        response = self.session.send(request=request.prepare(), allow_redirects=True)
        return response.url

    @staticmethod
    def get_game_data_by_place_id(place_id: int, games: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not games:
            return
        for game_data in games:
            if game_data.get('placeId') == place_id:
                return game_data

    @staticmethod
    def get_game_details_by_universe_id(universe_id: int, games_info: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not games_info:
            return
        for game_info in games_info:
            if game_info.get('id') == universe_id:
                return game_info

    @staticmethod
    def get_path_list(url: str) -> List[str]:
        return [i for i in urlparse(url).path.split('/') if i]


if __name__ == '__main__':
    from utils.items import UrlItem

    scraper = RobloxScraper(
        urls_data=UrlsData(
            data=[
                UrlItem(URL='https://www.roblox.com/games/7837709870/NFL-Shop'),
                # UrlItem(URL='https://www.roblox.com/games/10102215973/Lil-Nas-X-Concert-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/6679274937/Vans-World'),
                # UrlItem(URL='https://www.roblox.com/games/7619937171/Tai-Verdes-Concert-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/7462526249/NIKELAND-ZOOM-FREAK-4'),
                # UrlItem(URL='https://www.roblox.com/games/7665858439/DJ-Party-Space-Station'),
                # UrlItem(URL='https://www.roblox.com/games/8649501395/UPDATE-8-NFL-Tycoon'),
                # UrlItem(URL='https://www.roblox.com/games/8523408215/Alo-Sanctuary'),
                # UrlItem(URL='https://www.roblox.com/games/8967359816/24kGoldn-Concert-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/8209480473/Planet-Hip-Hop-Spotify-Island'),
                # UrlItem(URL='https://www.roblox.com/games/7830918930/Gucci-Town'),
                # UrlItem(URL='https://www.roblox.com/games/10204556059/NARS-Color-Quest'),
                # UrlItem(URL='https://www.roblox.com/games/10057963710/George-Ezra-s-Gold-Rush-Kid-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/7603178367/Chipotle-Burrito-Builder'),
                # UrlItem(URL='https://www.roblox.com/games/9648883891/RESORT-Festival-Tycoon'),
                # UrlItem(URL='https://www.roblox.com/games/9524757503/iHeartLand-Music-Tycoon'),
                # UrlItem(URL='https://www.roblox.com/games/9426082120/Samsung-Superstar-Galaxy'),
                # UrlItem(URL='https://www.roblox.com/games/9656012212/The-VMA-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/9249776514/Givenchy-Beauty-House'),
                # UrlItem(URL='https://www.roblox.com/games/9129288160/FASHION-SHOW-Tommy-Play'),
                # UrlItem(URL='https://www.roblox.com/games/8526353932/McLaren-F1-Racing-Experience'),
                # UrlItem(URL='https://www.roblox.com/games/5853107391/Stranger-Things-Starcourt-Mall'),
                # UrlItem(URL='https://www.roblox.com/games/10980366634/Walmart-Universe-of-Play'),
                # UrlItem(URL='https://www.roblox.com/games/10895555747/Walmart-Land'),
                # UrlItem(URL='https://www.roblox.com/games/10602062861/Amazon-Trip-Around-the-Blox')
            ],
        )
    )
    for scraped_data in scraper.start_scraping():
        print(str(scraped_data.created_at))
        print(scraped_data.dict())
    scraper.close(None, None, None)
