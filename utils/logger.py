import logging

from config import LOG_FORMAT_FILE, LOG_FORMAT_CONSOLE, LOG_LEVEL, LOG_FILEPATH, LOG_CONSOLE


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name, level=LOG_LEVEL)
        self._set_handlers()

    def _set_handlers(self):
        if LOG_CONSOLE is True:
            formatter_console = logging.Formatter(LOG_FORMAT_CONSOLE)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter_console)
            self.addHandler(console_handler)
        formatter_file = logging.Formatter(LOG_FORMAT_FILE)
        file_handler = logging.FileHandler(LOG_FILEPATH)
        file_handler.setFormatter(formatter_file)
        self.addHandler(file_handler)
