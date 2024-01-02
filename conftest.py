import datetime
import uuid
from pathlib import Path

import pytest
from pytest import Item, Session
from slugify import slugify

log_fullpath = pytest.StashKey[Path]()
session_datetime = pytest.StashKey[str]()
RESULTS_PATH = "results"


def prepare_logfile_path(item: Item, *, path: list[str], session_datetime: str) -> Path:
    """Create logfile full path per test invocation <item>

    Args:
        item (Item): pytest Item
        path (list[str]): list of names to create file structure
        session_datetime (str): pytest session formatted datetime

    Returns:
        Path: full logfile path
    """
    item_path_name = None
    item_name = slugify(item.name)
    path_args = path.copy()

    path_args.extend([session_datetime, "logs"])

    if item.path:
        item_path_name = slugify(item.path.name.removesuffix(".py"))

    path_args.append(str(uuid.uuid4()))

    if item_path_name:
        path_args.pop()
        path_args.append(item_path_name)

    path_args.append(f"{item_name}.log")

    full_filepath = Path(*path_args)
    return full_filepath


@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session: Session):
    """Pytest hook called for performing the main runtest loop (after collection finished).

    Args:
        session (Session): test execution Session
    """
    date_formatted = slugify(datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    session.stash[session_datetime] = date_formatted


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: Item):
    """Pytest test setup hook

    Args:
        item (Item): test invocation item
    """
    config = item.config
    skip_mark = item.get_closest_marker("skip")

    if not skip_mark:
        # create logfile per test case
        # https://docs.pytest.org/en/stable/how-to/logging.html#live-logs
        session_date = item.session.stash[session_datetime]
        file_path = prepare_logfile_path(item, path=[RESULTS_PATH], session_datetime=session_date)
        logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
        logging_plugin.set_log_path(file_path)  # pyright: ignore[reportOptionalMemberAccess]
        item.stash[log_fullpath] = file_path
        # end create logfile per test case

    yield


def remove_empty_logfile_dir(logfile_path: Path) -> None:
    """Remove empty parent directory for logfile

    Currently is using when logfile directory's name is an UUID from 'prepare_logfile_path' function

    Args:
        logfile_path (Path): test log file path
    """
    parent_dir = logfile_path.parent
    if parent_dir.is_dir() and not any(parent_dir.iterdir()):
        parent_dir.rmdir()


def remove_empty_logfile(logfile_path: Path) -> None:
    """Remove log file if is empty

    Args:
        logfile_path (Path): test log file path
    """
    if not logfile_path.read_text():
        logfile_path.unlink(missing_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item):
    """Pytest setup, test and teardown report hook

    Args:
        item (Item): test invocation item
    """
    outcome = yield
    result = outcome.get_result()
    skip_mark = item.get_closest_marker("skip")

    if not skip_mark:
        item_logfile_path: Path = item.stash[log_fullpath]

        if item_logfile_path.exists():
            full_filepath = item_logfile_path.resolve()

            if result.skipped:
                remove_empty_logfile(full_filepath)

            if result.longrepr and not result.skipped:
                # append failed message representation like AssertionError to respective test log file
                with open(full_filepath, "a+") as f:
                    f.write(f"{result.longreprtext}\n")

        # create summary.log with setup/test/teardown results for all executed test cases
        result_logs_path = item_logfile_path.parent.parent
        summary_path = Path(result_logs_path, "summary.log")
        summary_filepath = summary_path.resolve()

        summary_message = f"{item.nodeid}:::{result.outcome.upper()}\n"
        if result.when == "setup":
            with open(summary_filepath, "a+") as f:
                f.write(f"SETUP:::{summary_message}")

                if result.failed:
                    f.write(f"TEST:::{summary_message}")

        if result.when == "call" or result.skipped:
            with open(summary_filepath, "a+") as f:
                f.write(f"TEST:::{summary_message}")

        if result.when == "teardown":
            with open(summary_filepath, "a+") as f:
                f.write(f"TEARDOWN:::{summary_message}\n")
            # remove empty log file at the end of test teardown
            # example: if test doesn't have any logging call
            remove_empty_logfile(item_logfile_path)
            remove_empty_logfile_dir(item_logfile_path)

        # end create summary.log with setup/test/teardown results for all executed test cases
