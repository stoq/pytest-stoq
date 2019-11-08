import pytest


@pytest.mark.parametrize(
    "fixture_name",
    ("store", "current_station", "current_user", "current_branch", "example_creator"),
)
def test_fixture_are_setup_correctly(testdir, fixture_name):
    code = """
        def test_iculo({0}):
            assert {0}
    """
    testdir.makepyfile(code.format(fixture_name))

    result = testdir.runpytest("-v", "--skip-env-setup")

    result.stdout.fnmatch_lines(["*::test_iculo PASSED*"])
    assert result.ret == 0


def test_ini(testdir):
    ini = """
    [pytest]
    PLUGIN_CLASS = plug.Inho
    """
    testdir.makeini(ini)
    code = """
        def test_iculo(request):
            assert request.config.inicfg.get("PLUGIN_CLASS") == "plug.Inho"
    """
    testdir.makepyfile(code)

    result = testdir.runpytest("-v", "--skip-env-setup")
    result.stdout.fnmatch_lines(["*::test_iculo PASSED*"])
    assert result.ret == 0
