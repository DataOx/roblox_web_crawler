import logging

from config import LOG_FORMAT, LOG_LEVEL, LOG_FILEPATH, LOG_CONSOLE


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name, level=LOG_LEVEL)
        self.formatter = logging.Formatter(LOG_FORMAT)
        self._set_handlers()

    def _set_handlers(self):
        if LOG_CONSOLE is True:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.addHandler(console_handler)
        file_handler = logging.FileHandler(LOG_FILEPATH)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)
