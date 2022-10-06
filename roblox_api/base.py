import time
from typing import Dict, Optional, Any, Union
from urllib.parse import urljoin

from requests import Session, Request, Response, PreparedRequest

from roblox_api.exceptions import RobloxException
from utils.logger import Logger


class RobloxRequestsAPIBase:
    API_NAME: str
    BASE_URL = 'https://{}.roblox.com'

    def __init__(self, session: Session):
        assert self.API_NAME
        self.logger = Logger(self.__class__.__name__)
        self.session = session
        self.base_url = self.BASE_URL.format(self.API_NAME)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request('GET', path=path, params=params)

    def post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request('POST', path=path, json=params)

    def request(self, method: str, path: str = None, **kwargs) -> Any:
        if path.startswith('/'):
            path = path[1:]
        request = Request(method, urljoin(self.base_url, path), **kwargs)
        self.process_request(request)
        response = self.session.send(request.prepare())
        return self.process_response(response)

    def retry_request(self, response: Response):
        return self.process_response(self.session.send(response.request))

    def process_request(self, request: Union[Request, PreparedRequest]) -> None:
        # add authorization or other headers manipulation overriding this method
        request.headers['Accept'] = 'application/json'

    def process_response(self, response: Response) -> Any:
        if response.status_code == 429:
            wait_time = int(response.headers['Retry-After']) if response.headers.get('Retry-After') else 30
            self.logger.info('429 status code. Waiting {}s...'.format(wait_time))
            time.sleep(wait_time)
            return self.retry_request(response)
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
        else:
            errors = data.get('errors')
            if errors:
                raise RobloxException(
                    msg='\n'.join([f'{num}. {error["message"]}' for num, error in enumerate(errors, start=1)]),
                    response=response
                )
            return data


class RobloxAPIBase(RobloxRequestsAPIBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._get_requests_count = 0
        self._post_requests_count = 0
        self._total_requests_count = 0
        self._retries_requests_count = 0

    @property
    def get_requests_count(self) -> int:
        return self._get_requests_count

    @property
    def post_requests_count(self) -> int:
        return self._post_requests_count

    @property
    def total_requests_count(self) -> int:
        return self._total_requests_count + self._retries_requests_count

    @property
    def retries_requests_count(self) -> int:
        return self._retries_requests_count

    def request(self, *args, **kwargs) -> Any:
        request = super().request(*args, **kwargs)
        self._total_requests_count += 1
        return request

    def get(self, *args, **kwargs) -> Any:
        get_request = super().get(*args, **kwargs)
        self._get_requests_count += 1
        return get_request

    def post(self, *args, **kwargs) -> Any:
        post_request = super().post(*args, **kwargs)
        self._post_requests_count += 1
        return post_request

    def retry_request(self, *args, **kwargs) -> Any:
        retry_request = super().retry_request(*args, **kwargs)
        self._retries_requests_count += 1
        return retry_request

    def info_count_requests(self, count: int, before_msg: str = None, level: str = 'debug'):
        if count > 0:
            msg = f'Requests to Roblox {self.__class__.__name__} Count: {count}'
            if before_msg:
                msg = before_msg + ' ' + msg
            level = level.lower()
            if hasattr(self.logger, level):
                getattr(self.logger, level)(msg)

    def on_close(self):
        self.info_count_requests(count=self.get_requests_count, before_msg='GET')
        self.info_count_requests(count=self.post_requests_count, before_msg='POST')
        self.info_count_requests(count=self.retries_requests_count, before_msg='Retries')
        self.info_count_requests(count=self.total_requests_count, before_msg='Total', level='info')
