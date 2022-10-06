import os
from typing import Union

from celery import Celery

from config import GOOGLE_SPREADSHEET_ID, REDIS_URL, LOG_FILEPATH
from dao.connections import db
from dao.models import ExtractProduct
from managers import PoolModuleManager
from utils.items import UrlsData
from scrapers.items import RobloxItem

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
    if os.path.exists(LOG_FILEPATH):
        os.chmod(LOG_FILEPATH, 0o777)  # permission for writing to file for user
    if urls_data.data:
        print('Running Scraping...')
        manager = PoolModuleManager(GOOGLE_SPREADSHEET_ID, saving_db=False)
        manager.run_roblox_scraping(urls_data, requests_delay=0)
