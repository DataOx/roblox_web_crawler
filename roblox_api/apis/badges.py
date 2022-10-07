from roblox_api.base import RobloxAPIBase


class RobloxBadgesAPI(RobloxAPIBase):
    API_NAME = 'badges'

    def get_badges_info(self, badge_id: str):
        # docs: https://badges.roblox.com/docs#!/Badges/get_v1_badges_badgeId
        return self.get(f'v1/badges/{badge_id}')

    def get_badges_by_universe_id(self, universe_id: str, **query_params):
        # docs: https://badges.roblox.com/docs#!/Badges/get_v1_universes_universeId_badges
        return self.get(f'v1/universes/{universe_id}/badges', params=query_params)
