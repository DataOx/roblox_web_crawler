from celery import Celery

from config import GOOGLE_SPREADSHEET_ID, REDIS_URL
from managers import PoolModuleManager
from utils.items import UrlsData


app = Celery(name='roblox_web_crawler_tasks', broker=REDIS_URL, backend=REDIS_URL)


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


app.config_from_object(CeleryConfig)


@app.task(rate_limit='20/s')
def run_scraping_roblox(urls_data: UrlsData):
    if urls_data.data:
        manager = PoolModuleManager(GOOGLE_SPREADSHEET_ID, saving_db=False)
        manager.run_roblox_scraping(urls_data, requests_delay=0)
