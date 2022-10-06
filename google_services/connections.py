import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from utils.logger import Logger
from config import GOOGLE_SERVICE_ACCOUNT


SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')

credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SERVICE_ACCOUNT, SCOPES)


def get_spreadsheets_service() -> discovery.build:
    # Authentication
    http_auth = credentials.authorize(httplib2.Http())
    spreadsheets_service = discovery.build('sheets', 'v4', http=http_auth, num_retries=3)
    return spreadsheets_service


logger = Logger('Google Service')
