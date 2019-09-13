from stoqlib.domain.exampledata import ExampleCreator
from stoqlib.domain.person import Branch, LoginUser
from stoqlib.domain.station import BranchStation
from storm.store import Store

import pytest


@pytest.mark.parametrize(
    "fixture_name",
    ("store", "current_station", "current_user", "current_branch", "example_creator"),
)
def test_fixture_are_setup_correctly(testdir, fixture_name):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    code = """
        def test_iculo({0}):
            assert {0}
    """
    testdir.makepyfile(code.format(fixture_name))

    # run pytest with the following cmd args
    result = testdir.runpytest("-v", "--skip-db-setup")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_iculo PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_fixture_store(store):
    assert isinstance(store, Store)


def test_fixture_current_station(current_station):
    assert isinstance(current_station, BranchStation)


def test_fixture_current_user(current_user):
    assert isinstance(current_user, LoginUser)


def test_fixture_current_branch(current_branch):
    assert isinstance(current_branch, Branch)


def test_fixture_example_creator(example_creator, current_station, current_user, current_branch):
    assert isinstance(example_creator, ExampleCreator)
    assert example_creator.current_station == current_station
    assert example_creator.current_user == current_user
    assert example_creator.current_branch == current_branch
