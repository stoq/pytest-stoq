import os

import pytest

import stoqlib.api
from stoqlib.database.testsuite import bootstrap_suite
from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.lib.configparser import StoqConfig, register_config


def pytest_addoption(parser):
    group = parser.getgroup("stoq")
    group.addoption(
        "--skip-db-setup",
        action="store_true",
        dest="skip_db_setup",
        default=None,
        help="Run the tests with quick database setup mode.",
    )
    group.addoption(
        "--extra-plugins",
        action="store",
        dest="extra_plugins",
        default=None,
        nargs="+",
        help="Additional plugins to be installed before running the test suite.",
    )


@pytest.fixture(autouse=True, scope="session")
def stoq_test_environment(request):
    if request.config.getvalue("skip_db_setup"):
        return

    config = StoqConfig()
    config.load_default()
    register_config(config)

    hostname = os.environ.get("STOQLIB_TEST_HOSTNAME")
    dbname = os.environ.get("STOQLIB_TEST_DBNAME")
    username = os.environ.get("STOQLIB_TEST_USERNAME")
    password = os.environ.get("STOQLIB_TEST_PASSWORD")
    port = int(os.environ.get("STOQLIB_TEST_PORT") or 0)
    quick = os.environ.get("STOQLIB_TEST_QUICK", None) is not None

    bootstrap_suite(
        address=hostname,
        dbname=dbname,
        port=port,
        username=username,
        password=password,
        quick=quick,
        extra_plugins=request.config.getvalue("extra_plugins"),
    )


@pytest.fixture(scope="session")
def store():
    return stoqlib.api.get_default_store()


@pytest.fixture(scope="session")
def current_station(store):
    return stoqlib.api.get_current_station(store)


@pytest.fixture(scope="session")
def current_user(store):
    return stoqlib.api.get_current_user(store)


@pytest.fixture(scope="session")
def current_branch(store):
    return stoqlib.api.get_current_branch(store)


@pytest.fixture(scope="session")
def example_creator(store, current_station, current_user, current_branch):
    creator = ExampleCreator()
    creator.set_store(store)
    creator.current_station = current_station
    creator.current_user = current_user
    creator.current_branch = current_branch
    return creator
