from datetime import datetime
from urllib.parse import urlparse

from utils.items import UrlItem
from pytz import timezone


def validate_roblox_url_for_scraping(url_data: UrlItem):
    parsed_url = urlparse(url_data.URL)
    url_path_list = [i for i in parsed_url.path.split('/') if i]
    try:
        if url_path_list[0].lower() != 'games' or not url_path_list[-2].isdigit():
            return False
    except ValueError:
        return False
    return True


def get_pacific_time() -> datetime:
    return datetime.now(tz=timezone('US/Pacific'))
