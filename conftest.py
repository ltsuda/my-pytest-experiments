import datetime
from pathlib import Path

import pytest
from pytest import Item
from slugify import slugify


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: Item):
    """Pytest test setup hook

    Args:
        item (Item): test invocation item
    """
    # create a logfile per test case
    item_path_name = None
    config = item.config
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
    item_name = slugify(item.name)
    if item.path:
        item_path_name = slugify(item.path.name.removesuffix(".py"))

    date_formatted = datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S")
    date_slugified = slugify(date_formatted)

    path_args = ["results", date_slugified, "logs"]
    if item_path_name:
        path_args.append(item_path_name)
    path_args.append(f"{item_name}.log")

    full_fname = Path(*path_args)
    logging_plugin.set_log_path(full_fname)  # pyright: ignore[reportOptionalMemberAccess]
    # end of create a logfile per test case
    yield
