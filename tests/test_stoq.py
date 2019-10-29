from unittest import mock

import pytest

from pytest_stoq.stoq import _install_plugin, _setup_test_environment


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

    mock_get_plugin_manager.assert_called_once_with()
    mock_plugin_manager.register_plugin_description.assert_called_once_with(
        "pluginho/pluginho.plugin"
    )
    mock_plugin_manager.install_plugin.assert_called_once_with(mock_store, "pluginho")
    mock_plugin_manager.activate_plugin.assert_called_once_with("pluginho")


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
@pytest.mark.parametrize("quick", (True, False))
def test_setup_test_enviorment(mock_bootstrap, mock_install_plugin, request, quick):
    request.config.option.quick_mode = quick

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=quick,
    )
    mock_install_plugin.assert_not_called()


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
def test_setup_test_enviorment_install_plugin(mock_bootstrap, mock_install_plugin, request):
    request.config.option.quick_mode = False
    request.config.option.plugin_cls = "plug.In"

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=False,
    )
    mock_install_plugin.assert_called_once_with("plug.In")


@mock.patch("pytest_stoq.stoq._install_plugin")
@mock.patch("pytest_stoq.stoq.bootstrap_suite")
def test_setup_test_enviorment_do_not_install_plugin(mock_bootstrap, mock_install_plugin, request):
    request.config.option.quick_mode = True
    request.config.option.plugin_cls = "plug.In"

    assert _setup_test_environment(request) is None

    mock_bootstrap.assert_called_once_with(
        address=None, dbname=None, port=0, username=None, password=None, quick=True,
    )
    mock_install_plugin.assert_not_called()
