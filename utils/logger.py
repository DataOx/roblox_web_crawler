import logging

from config import LOG_FORMAT_CONSOLE, LOG_LEVEL


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name, level=LOG_LEVEL)
        self._set_handlers()

    def _set_handlers(self):
        formatter_console = logging.Formatter(LOG_FORMAT_CONSOLE)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter_console)
        self.addHandler(console_handler)
