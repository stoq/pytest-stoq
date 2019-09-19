from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.domain.person import Branch, LoginUser
from stoqlib.domain.station import BranchStation
from stoqlib.domain.till import Till
from storm.store import Store


def test_store(store):
    assert isinstance(store, Store)


def test_current_station(current_station):
    assert isinstance(current_station, BranchStation)


def test_current_user(current_user):
    assert isinstance(current_user, LoginUser)


def test_current_branch(current_branch):
    assert isinstance(current_branch, Branch)


def test_current_till(current_till):
    assert isinstance(current_till, Till)


def test_example_creator(example_creator, current_station, current_user, current_branch):
    assert isinstance(example_creator, ExampleCreator)
    assert example_creator.current_station == current_station
    assert example_creator.current_user == current_user
    assert example_creator.current_branch == current_branch
