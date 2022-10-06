from urllib.parse import urlparse

from utils.items import UrlItem


def is_invalid_roblox_url(url_item: UrlItem) -> bool:
    parse_url = urlparse(url_item.URL)
    paths = parse_url.path.split('/')
    if not ('roblox.com' in parse_url.netloc):
        url_item.message = 'It is not roblox URL'
        return True
    if 'games' not in paths:
        url_item.message = 'path of URL does not start with "games"'
        return True
    return False


def is_valid_roblox_url(url_item: UrlItem) -> bool:
    parse_url = urlparse(url_item.URL)
    paths = parse_url.path.split('/')
    if 'roblox.com' in parse_url.netloc:
        return True
    if not (paths[0].startswith('games')):
        return True
    return False
