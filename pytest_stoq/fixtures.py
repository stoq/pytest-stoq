import pytest
import stoqlib.api
from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.domain.till import Till

from .stoq import _setup_test_environment


@pytest.fixture(autouse=True, scope="session")
def stoq_test_environment(request):
    _setup_test_environment(request)


@pytest.fixture
def store():
    store = stoqlib.api.new_store()
    yield store
    store.rollback()


@pytest.fixture
def current_station(store):
    return stoqlib.api.get_current_station(store)


@pytest.fixture
def current_user(store):
    return stoqlib.api.get_current_user(store)


@pytest.fixture
def current_branch(store):
    return stoqlib.api.get_current_branch(store)


@pytest.fixture
def current_till(store, example_creator, current_station):
    return Till.get_current(store, current_station) or example_creator.create_till()


@pytest.fixture
def example_creator(store, current_station, current_user, current_branch):
    creator = ExampleCreator()
    creator.set_store(store)
    creator.current_station = current_station
    creator.current_user = current_user
    creator.current_branch = current_branch
    return creator
