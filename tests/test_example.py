import logging

logger = logging.getLogger("test_example")


def test_example_one():
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


def test_example_two():
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
