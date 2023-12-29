import datetime
from pathlib import Path

import pytest
from pytest import Item
from slugify import slugify

log_fullpath = pytest.StashKey[Path]()


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

    file_path = Path(*path_args)
    logging_plugin.set_log_path(file_path)  # pyright: ignore[reportOptionalMemberAccess]
    item.stash[log_fullpath] = file_path
    # end of create a logfile per test case
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item):
    outcome = yield
    result = outcome.get_result()

    item_logfile_path = item.stash[log_fullpath]
    if item_logfile_path.exists():
        file = item_logfile_path.resolve()

        if result.skipped:
            content = file.read_text()
            if not content:
                item_logfile_path.unlink(missing_ok=True)

        if result.longrepr and not result.skipped:
            with open(file, "a") as f:
                f.write(f"{result.longreprtext}\n")

    results_path = Path(item_logfile_path.cwd(), "results")
    summary_path = Path(results_path, "summary.log")
    summary_filepath = summary_path.resolve()

    if result.when == "setup":
        mode = "a" if summary_path.exists() else "w"
        with open(summary_filepath, mode) as f:
            f.write(f"SETUP:::{item.nodeid}:::{result.outcome.upper()}\n")

            if result.failed:
                f.write(f"\tTEST:::{item.nodeid}:::{result.outcome.upper()}\n")

    if result.when == "call" or result.skipped:
        mode = "a" if summary_path.exists() else "w"
        with open(summary_filepath, mode) as f:
            f.write(f"\tTEST:::{item.nodeid}:::{result.outcome.upper()}\n")

    if result.when == "teardown":
        mode = "a" if summary_path.exists() else "w"
        with open(summary_filepath, mode) as f:
            f.write(f"TEARDOWN:::{item.nodeid}:::{result.outcome.upper()}\n")
