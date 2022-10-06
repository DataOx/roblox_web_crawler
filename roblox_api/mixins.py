from typing import Any


class RequestsCounterMixin:
    _get_requests_count = 0
    _post_requests_count = 0
    _total_requests_count = 0
    _retries_requests_count = 0

    @property
    def retries_requests_count(self) -> int:
        return self._retries_requests_count

    def retry_request(self, *args, **kwargs) -> Any:
        retry_request = super().retry_request(*args, **kwargs)
        self._retries_requests_count += 1
        return retry_request

    @property
    def total_requests_count(self) -> int:
        return self._total_requests_count + self._retries_requests_count

    def request(self, *args, **kwargs) -> Any:
        request = super().request(*args, **kwargs)
        self._total_requests_count += 1
        return request

    @property
    def get_requests_count(self) -> int:
        return self._get_requests_count

    def get(self, *args, **kwargs) -> Any:
        get_request = super().get(*args, **kwargs)
        self._get_requests_count += 1
        return get_request

    @property
    def post_requests_count(self) -> int:
        return self._post_requests_count

    def post(self, *args, **kwargs) -> Any:
        post_request = super().post(*args, **kwargs)
        self._post_requests_count += 1
        return post_request

    def info_count_requests(self, count: int, before_msg: str = None):
        print(count)
        if count > 0:
            msg = f'Requests to Roblox {self.__class__.__name__} Count: {count}'
            if before_msg:
                msg = before_msg + ' ' + msg
            self.logger.info(msg)
