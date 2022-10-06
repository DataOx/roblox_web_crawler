from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Union

from utils import get_pacific_time


@dataclass
class RobloxItem:
    url: str
    name: str = 'Not found'
    row_index: int = field(default=0)
    message: str = None
    created: Union[str, datetime] = None
    updated: Union[str, datetime] = None
    favorites: int = field(default=0)
    visits: int = field(default=0)
    badges_total: int = field(default=0)

    def __post_init__(self):
        try:
            if self.created and isinstance(self.created, str):
                self.created = self._parse_datetime_from_str(self.created)
        except ValueError:
            msg = 'Cannot parse datetime for created value: {}'.format(self.created)
            if not self.message:
                self.message = msg
            else:
                self.message += '\n' + msg

        try:
            if self.updated and isinstance(self.updated, str):
                self.updated = self._parse_datetime_from_str(self.updated)
        except ValueError:
            msg = 'Cannot parse datetime for updated value: {}'.format(self.updated)
            if not self.message:
                self.message = msg
            else:
                self.message += '\n' + msg
        self._created_at = get_pacific_time()

    _default_format = '%Y-%m-%dT%H:%M:%S.%f'

    def _parse_datetime_from_str(self, value: str) -> datetime:
        if '.' in value:
            split_value = value.split('.')
            value = f'{split_value[0]}.{split_value[1][:6]}'
        if value.endswith('Z'):
            value = value[:-1]
        return datetime.strptime(
            value,
            self._default_format if '.' in value else self._default_format.split('.')[0]
        )

    @property
    def created_at(self):
        return self._created_at

    dict = asdict
