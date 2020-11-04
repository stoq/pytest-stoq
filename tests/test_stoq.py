from unittest import mock

import pytest

from pytest_stoq.stoq import _get_plugin_configs, _install_plugin, _setup_test_environment


@mock.patch("pytest_stoq.stoq.stoqlib.api.new_store")
@mock.patch("pytest_stoq.stoq.importlib.import_module")
@mock.patch("pytest_stoq.stoq.get_plugin_manager")
def test_install_plugin(mock_get_plugin_manager, mock_import_module, mock_new_store):
    mock_store = mock_new_store.return_value.__enter__.return_value
    mock_plugin_manager = mock_get_plugin_manager.return_value
    mock_plugin = mock.Mock()
    mock_plugin.name = "pluginho"
    mock_import_module.return_value = mock.Mock(
        __file__="/path/to/pluginho/pluginho.py", pluginho=mock_plugin,
    )

    assert _install_plugin("plugin.pluginho") is None

    assert mock_get_plugin_manager.call_count == 2
    mock_plugin_manager.register_plugin_description.assert_called_once_with(
        "/path/to/pluginho/pluginho.plugin"
    )
    mock_plugin_manager.install_plugin.assert_called_once_with(mock_store, "pluginho")
    mock_plugin_manager.activate_plugin.assert_called_once_with("pluginho")


@mock.patch("pytest_stoq.stoq.stoqlib.api.new_store")
@mock.patch("pytest_stoq.stoq.importlib.import_module")
@mock.patch("pytest_stoq.stoq.get_plugin_manager")
def test_install_plugin_do_not_install_or_active_twice(
    mock_get_plugin_manager, mock_import_module, mock_new_store,
):
    mock_plugin_manager = mock_get_plugin_manager.return_value
    mock_plugin = mock.Mock()
    mock_plugin.name = "pluginho"
    mock_import_module.return_value = mock.Mock(
        __file__="/path/to/pluginho/pluginho.py", pluginho=mock_plugin,
    )
    mock_plugin_manager.installed_plugins_names = ["pluginho"]
    mock_plugin_manager.active_plugins_names = ["pluginho"]

    assert _install_plugin("plugin.pluginho") is None

    assert mock_get_plugin_manager.call_count == 2
    mock_plugin_manager.register_plugin_description.assert_called_once_with(
        "/path/to/pluginho/pluginho.plugin"
    )
    mock_plugin_manager.install_plugin.assert_not_called()
    mock_plugin_manager.activate_plugin.assert_not_called()


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
@pytest.mark.parametrize("quick", (True, False))
def test_setup_test_enviorment(mock_bootstrap, mock_install_plugin, request, quick, monkeypatch):
    monkeypatch.setattr(request.config.option, 'quick_mode', quick)

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=quick,
    )
    mock_install_plugin.assert_not_called()


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
@pytest.mark.parametrize('empty_value', ('None', 'False', 'f', 'false', '', '0'))
def test_setup_test_enviorment_quick_env_var_empty(
    mock_bootstrap, mock_install_plugin, monkeypatch, request, empty_value
):
    monkeypatch.setenv('STOQLIB_TEST_QUICK', empty_value)

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=False,
    )
    mock_install_plugin.assert_not_called()


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
@pytest.mark.parametrize('is_quick', (True, False))
def test_setup_test_enviorment_install_plugin(mock_bootstrap, mock_install_plugin, is_quick, request, monkeypatch):
    monkeypatch.setattr(request.config.option, 'quick_mode', is_quick)
    monkeypatch.setattr(request.config.option, 'plugin_cls', 'plug.In')

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=is_quick,
    )
    mock_install_plugin.assert_called_once_with("plug.In")


@mock.patch("pytest_stoq.stoq._register_plugin")
@mock.patch("pytest_stoq.stoq.get_plugin_manager")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
@pytest.mark.parametrize('raw_plugins,extra_plugins', (
    ("plugin1", ["plugin1"]),
    ("plugin1,plugin2", ["plugin1", "plugin2"]),
))
def test_setup_test_environment_activate_plugin(
        mock_bootstrap, mock_get_plugin_manager, register_plugin_mock,
        raw_plugins, extra_plugins, request, monkeypatch
):
    mock_activate_plugin = mock_get_plugin_manager.return_value.activate_plugin
    monkeypatch.setattr(request.config.option, 'stoq_plugins', raw_plugins)

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=False,
    )
    mock_get_plugin_manager.assert_called_once_with()
    register_plugin_mock.assert_any_call("plugin1")

    assert mock_activate_plugin.call_count == len(extra_plugins)
    for plugin_name in extra_plugins:
        mock_activate_plugin.assert_any_call(plugin_name)


def test_get_plugin_configs_empty(pytestconfig):
    config = _get_plugin_configs(pytestconfig)

    assert config['plugin_cls'] is None
    assert config['quick_mode'] is None
    assert config['skip_env_setup'] is None
    assert config['extra_plugins'] == []


def test_get_plugin_configs(pytestconfig, monkeypatch):
    monkeypatch.setattr(pytestconfig.option, 'plugin_cls', 'foo.bar.Plug.In')
    monkeypatch.setattr(pytestconfig.option, 'quick_mode', True)
    monkeypatch.setattr(pytestconfig.option, 'skip_env_setup', False)
    monkeypatch.setitem(pytestconfig.inicfg, 'STOQ_PLUGINS', 'stoq-plugin,other-plugin')

    config = _get_plugin_configs(pytestconfig)

    assert config['plugin_cls'] == 'foo.bar.Plug.In'
    assert config['quick_mode'] is True
    assert config['skip_env_setup'] is False
    assert config['extra_plugins'] == ['stoq-plugin', 'other-plugin']


def test_get_plugin_configs_stoq_plugins(pytestconfig, monkeypatch):
    monkeypatch.setattr(pytestconfig.option, 'stoq_plugins', 'stoq-plugin')

    config = _get_plugin_configs(pytestconfig)

    assert config['extra_plugins'] == ['stoq-plugin']
