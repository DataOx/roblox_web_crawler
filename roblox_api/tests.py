import unittest

from requests import Session

from roblox_api.apis import RobloxBadgesAPI, RobloxGamesAPI


class TestAPIs(unittest.TestCase):
    def setUp(self) -> None:
        self.session = Session()
        self.badges_api = RobloxBadgesAPI(session=self.session)
        self.games_api = RobloxGamesAPI(session=self.session)
        self.game_title = 'NIKELAND-ZOOM-FREAK-4'
        self.universe_id = '3421293944'

    def test_games_list(self):
        games_meta_data = self.games_api.get_games_list(keyword=self.game_title)
        self.assertTrue(games_meta_data)
        self.assertIsNotNone(games_meta_data.get('games'))
        self.assertTrue(games_meta_data.get('games'))
        for game_meta in games_meta_data.get('games'):
            self.assertIsNotNone(game_meta.get('name'), msg='not found game name with key "name"')
            self.assertIsNotNone(game_meta.get('creatorId'), msg='not found creator id with key "creatorId"')
            self.assertIsNotNone(game_meta.get('universeId'), msg='not found universe id with key "universeId"')

    def test_games_by_group(self):
        games_info = self.games_api.get_games_by_group(group_id='12205780')
        self.assertTrue(games_info)
        self.assertIsNotNone(games_info.get('data'))
        self.assertTrue(games_info.get('data'))
        for game_data in games_info.get('data'):
            self.assertIsNotNone(game_data.get('name'), msg='not found game name with key "name"')
            self.assertIsNotNone(game_data.get('created'), msg='not found creation value with key "created"')
            self.assertIsNotNone(game_data.get('updated'), msg='not found updated value with key "updated"')
            self.assertIsNotNone(game_data.get('placeVisits'), msg='not found visits value with key "placeVisits"')

    def test_badges_by_universe_id(self):
        result = self.badges_api.get_badges_by_universe_id(universe_id=self.universe_id)
        self.assertIsNotNone(result)
        badges = result.get('data')
        self.assertIsNotNone(badges)
        for badge in badges:
            statistics = badge.get('statistics')
            self.assertIsNotNone(statistics)
            self.assertIsNotNone(statistics.get('awardedCount'))

    def tearDown(self) -> None:
        self.session.close()


if __name__ == '__main__':
    unittest.main()
