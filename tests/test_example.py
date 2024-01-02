import logging

import pytest

logger = logging.getLogger("test_example")


def test_example_one(module_logger):
    module_logger.info("hello world info")
    module_logger.debug("hello world debug")
    module_logger.warning("hello world warning")
    module_logger.error("hello world error")
    module_logger.tc_step("hello world tc_step")
    module_logger.critical("hello world critical")
    module_logger.fixture("hello world fixture")
    assert True


@pytest.mark.skip("skipped")
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
