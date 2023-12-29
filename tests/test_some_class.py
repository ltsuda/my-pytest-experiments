import logging

logger = logging.getLogger("TestSomeClass")


class TestSomeClass:
    def test_from_class_one(self):
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

    def test_from_class_two(self):
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
        assert "Hello" in "hello World testing"
