import logging

logger = logging.getLogger(__name__)


def test_ui_one():
    logger.info("hello world")
    logger.info("hello world")
    logger.debug("hello world")
    logger.info("hello world")
    logger.info("hello world")
    logger.warning("hello world")
    logger.info("hello world")
    logger.info("hello world")
    logger.error("hello world")
    logger.info("hello world")
    logger.info("hello world")
    logger.critical("hello world")
    assert True
