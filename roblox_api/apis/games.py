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
