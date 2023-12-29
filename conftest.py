import datetime
import uuid
from pathlib import Path

import pytest
from pytest import Item
from slugify import slugify

log_fullpath = pytest.StashKey[Path]()


def prepare_logfile_path(item: Item, path: list[str]) -> Path:
    """Create logfile full path per test invocation <item>

    Args:
        item (Item): pytest Item
        path (list[str]): list of names to create file structure

    Returns:
        Path: full logfile path
    """
    item_path_name = None
    item_name = slugify(item.name)
    path_args = path.copy()

    date_formatted = datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S")
    date_formatted = slugify(date_formatted)

    path_args.extend([date_formatted, "logs"])

    if item.path:
        item_path_name = slugify(item.path.name.removesuffix(".py"))

    path_args.append(str(uuid.uuid4()))

    if item_path_name:
        path_args.pop()
        path_args.append(item_path_name)

    path_args.append(f"{item_name}.log")

    full_filepath = Path(*path_args)
    return full_filepath


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: Item):
    """Pytest test setup hook

    Args:
        item (Item): test invocation item
    """
    config = item.config

    # create logfile per test case
    file_path = prepare_logfile_path(item, path=["results"])
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
    logging_plugin.set_log_path(file_path)  # pyright: ignore[reportOptionalMemberAccess]
    item.stash[log_fullpath] = file_path
    # end create logfile per test case

    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item):
    outcome = yield
    result = outcome.get_result()

    item_logfile_path: Path = item.stash[log_fullpath]
    parent_dir = item_logfile_path.parent
    if parent_dir.is_dir() and not any(parent_dir.iterdir()):
        parent_dir.rmdir()

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
