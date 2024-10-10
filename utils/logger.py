import logging
import os

from colorlog import ColoredFormatter


class SingletonMeta(type):
    """A metaclass for the Singleton pattern."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        handler = logging.StreamHandler()

        # Color formatting
        log_colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
            "TIMER": "blue",
        }

        formatter = ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s \033[37m%(message)s\033[0m \033[37m[%(module)s/%(funcName)s/line %(lineno)d]\033[0m",
            datefmt=None,
            reset=True,
            log_colors=log_colors,
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        logging.addLevelName(25, "TIMER")
        self.logger.timer = self.timer

    def get_logger(self):
        return self.logger

    def timer(self, message, *args, **kwargs):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger._log(25, message, args, **kwargs)

logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()
log_level = getattr(logging, logger_level, logging.INFO)
logger = Logger(log_level).get_logger()