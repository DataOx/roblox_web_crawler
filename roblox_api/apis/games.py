from roblox_api.base import RobloxAPIBase


class RobloxGamesAPI(RobloxAPIBase):
    API_NAME = 'games'

    def get_games_by_group(self, group_id: str, **query_params):
        # docs: https://games.roblox.com/docs#!/Games/get_v2_groups_groupId_games
        return self.get(f'v2/groups/{group_id}/games', params=query_params)

    def get_games_list(self, **query_params):
        # docs: https://games.roblox.com/docs#!/Games/get_v1_games_list
        return self.get('v1/games/list', params=query_params)

    def get_games(self, **query_params):
        # docs: https://games.roblox.com/docs#!/Games/get_v1_games
        return self.get('/v1/games', params=query_params)

    def multi_get_place_details(self, **query_params):
        return self.get('/v1/games/multiget-place-details', params=query_params)


if __name__ == '__main__':
    from pprint import pprint
    from urllib.parse import urlparse
    from datetime import datetime
    from requests import Session
    n = datetime.now()
    s = Session()
    games_api = RobloxGamesAPI(s)
    # badges_api = RobloxBadgesAPI(s)
    # result = games_api.multi_get_place_details(placeIds=9103460924)
    # print(result)
    url = 'https://www.roblox.com/games/9103460924/UPDATE-Sword-Factory-X'
    parsed_url = urlparse(url)
    url_paths = parsed_url.path.split('/')
    title = url_paths[-1]
    place_id = url_paths[-2]
    title_words = title.split('-')
    # result = games_api.get_games_list(keyword=title)
    universe_id = '3421293944'
    result = games_api.get_games(universeIds=universe_id)
    games_api.on_close()
    pprint(result)
    # # end_time = datetime.now() + timedelta(minutes=1)
    # # while datetime.now() < end_time:
    # #     result = games_api.get_games_list(keyword=title)
    # print(games_api.total_request_count)

    # time.sleep(0.01)
    # game = result.get('games')[0]
    # game = None
    # for game_meta in result.get('games'):
    #     if place_id == str(game_meta['placeId']):
    #         game = game_meta
    #         break
    # universeId = game.get('universeId')
    # creatorId = game.get('creatorId')
    # placeId = game.get('placeId')
    # game_i = games_api.get_games(universeIds=universeId)
    # print(universeId)
    # pprint(game_i)
    # info = games_api.get_games_by_group(group_id=game.get('creatorId'))
    # game_i = None
    # for game_info in info.get('data'):
    #     if universeId == game_info.get('id'):
    #         game_i = game_info
    #         break
    # time.sleep(0.01)
    # pprint(game_i)
    # badges = badges_api.get_badges_by_universe_id(universe_id=game.get('universeId'))
    # e = datetime.now()
    # print(n, e)
    # print(game)
    # pprint(info.get('data'))
    # pprint(badges)
    s.close()
