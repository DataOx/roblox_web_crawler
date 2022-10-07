import os
import logging
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).parent
STATIC = os.path.join(BASE_DIR, 'static')

# GOOGLE SERVICES
GOOGLE_SPREADSHEET_RETRIES = int(os.environ.get('GOOGLE_SPREADSHEET_RETRIES', 1))
GOOGLE_SERVICE_ACCOUNT = os.path.join(STATIC, 'credentials.json')
GOOGLE_SPREADSHEET_ID = os.environ.get('GOOGLE_SPREADSHEET_ID')
GOOGLE_MIN_BACKOFF_TIME = 30
GOOGLE_MAX_BACKOFF_TIME = 300  # 5 min

# Logging
LOG_LEVEL = logging.NOTSET
LOG_FORMAT_CONSOLE = '[%(name)s/%(levelname)s]: %(message)s'  # it will look through celery

# DATABASES
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'test_db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'root')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.environ.get('POSTGRES_INTERNAL_PORT', 5432))

# REDIS
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "pwdlocal")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'

# TOKENS
API_KEYS = os.environ.get('API_KEYS', '').split(' ')
