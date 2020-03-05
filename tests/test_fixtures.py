from unittest import mock

from stoqlib import api
from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.domain.person import Branch, LoginUser
from stoqlib.domain.sale import Sale
from stoqlib.domain.station import BranchStation
from stoqlib.domain.till import Till
from stoqlib.lib.parameters import ParameterAccess
from storm.store import Store


def test_store(store):
    assert isinstance(store, Store)


def test_store_mocked(store):
    assert isinstance(store.close, mock.Mock)
    assert isinstance(store.commit, mock.Mock)
    assert isinstance(store.rollback, mock.Mock)


def test_new_store(mock_new_store, store):
    with api.new_store() as new_store:
        assert new_store is store


def test_store_does_not_commit(testdir, store):
    code = """
        def test_store_rollbacks(store, example_creator):
            example_creator.create_sale()
    """
    testdir.makepyfile(code)
    sale_count = store.find(Sale).count()

    result = testdir.runpytest("-v", "--skip-env-setup")

    result.stdout.fnmatch_lines(["*::test_store_rollbacks PASSED*"])
    assert result.ret == 0
    assert store.find(Sale).count() == sale_count


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


def test_sysparam(sysparam):
    assert isinstance(sysparam, ParameterAccess)
