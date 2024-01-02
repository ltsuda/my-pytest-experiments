import logging
from typing import cast

FIXTURE = 21
TC_STEP = 22
logging.addLevelName(FIXTURE, "FIXTURE")
logging.addLevelName(TC_STEP, "TC_STEP")


class MyLogger(logging.Logger):
    """Inherit from standard Logger and add custom levels.

    Args:
        logging (logging.Logger): parent class
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def fixture(self, msg, *args, **kwargs):
        """Custom logging level function to be used in Pytest's fixtures

        Args:
            msg (str): message to be logged
        """
        if self.isEnabledFor(FIXTURE):
            self._log(FIXTURE, msg, args, **kwargs)

    def tc_step(self, msg, *args, **kwargs):
        """Custom logging level function to be used in test cases files

        Args:
            msg (str): message to be logged
        """
        if self.isEnabledFor(TC_STEP):
            self._log(TC_STEP, msg, args, **kwargs)


logging.setLoggerClass(MyLogger)


def get_logger(name, level=logging.INFO) -> MyLogger:
    """Get custom MyLogger logger instance

    Args:
        name (str): logger name, example __name__
        level (int, optional): logging level value. Defaults to logging.INFO.

    Note: as Pytest root logger configuration is present in pyproject.toml for live logging,
    this function is overriding root level DEBUG with INFO. If using the default logger from logging
    package, it will use the DEBUG level.

    Returns:
        MyLogger: custom logging.Logger subclass with more log levels
    """
    logger = cast(MyLogger, logging.getLogger(name))
    logger.setLevel(level)

    return logger
