import os

import pytest

import stoqlib.api
from stoqlib.database.testsuite import bootstrap_suite
from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.lib.configparser import StoqConfig, register_config
from stoqlib.lib.environment import configure_locale


@pytest.fixture(autouse=True, scope='session')
def stoq_test_environment():
    configure_locale('en_US')

    config = StoqConfig()
    config.load_default()
    register_config(config)

    hostname = os.environ.get('STOQLIB_TEST_HOSTNAME')
    dbname = os.environ.get('STOQLIB_TEST_DBNAME')
    username = os.environ.get('STOQLIB_TEST_USERNAME')
    password = os.environ.get('STOQLIB_TEST_PASSWORD')
    port = int(os.environ.get('STOQLIB_TEST_PORT') or 0)
    quick = os.environ.get('STOQLIB_TEST_QUICK', None) is not None

    bootstrap_suite(address=hostname, dbname=dbname, port=port,
                    username=username, password=password, quick=quick)


@pytest.fixture(scope='session')
def store():
    return stoqlib.api.get_default_store()


@pytest.fixture(scope='session')
def example_creator(store):
    creator = ExampleCreator()
    creator.set_store(store)
    return creator


@pytest.fixture(scope='session')
def current_station(example_creator, current_branch):
    return example_creator.create_station(branch=current_branch)


@pytest.fixture(scope='session')
def current_user(example_creator):
    return example_creator.create_user()


@pytest.fixture(scope='session')
def current_branch(example_creator):
    return example_creator.create_branch()
