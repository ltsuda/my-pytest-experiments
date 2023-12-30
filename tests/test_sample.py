import logging

import pytest

logger = logging.getLogger("test_sample")


@pytest.fixture
def my_fixture():
    logger.info("my_fixture log")
    assert False


@pytest.fixture
def my_teardown():
    yield
    logger.info("teardown log")
    assert False


def test_sample_one(my_fixture):
    logger.debug(my_fixture)
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


def test_sample_two():
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


@pytest.mark.xfail(reason="xfailing", strict=True)
def test_sample_three():
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


def test_sample_four(my_teardown):
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
