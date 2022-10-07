from requests import RequestException


class RobloxException(RequestException):
    def __init__(self, msg: str, *args, **kwargs):
        self.msg = msg
        super().__init__(*args, **kwargs)

