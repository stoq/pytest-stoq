import importlib
import os

import stoqlib.api
from stoqlib.database.testsuite import bootstrap_suite
from stoqlib.lib.configparser import StoqConfig, register_config
from stoqlib.lib.pluginmanager import get_plugin_manager


def _install_plugin(name):
    plugin_module_name, plugin_cls_name = name.rsplit(".", maxsplit=1)
    plugin_module = importlib.import_module(plugin_module_name)
    plugin_cls = getattr(plugin_module, plugin_cls_name)

    plugin_name = plugin_cls.name
    manager = get_plugin_manager()
    plugin_dir = os.path.dirname(plugin_module.__file__)
    plugin_package_name = os.path.basename(plugin_dir)
    desc_filename = os.path.join(plugin_package_name, "{}.plugin".format(plugin_name))
    manager.register_plugin_description(desc_filename)

    if name not in manager.installed_plugins_names:
        with stoqlib.api.new_store() as store:
            manager.install_plugin(store, plugin_name)

    if name not in manager.active_plugins_names:
        manager.activate_plugin(plugin_name)


def _setup_test_environment(request):
    if request.config.getvalue("skip_env_setup"):
        return

    config = StoqConfig()
    config.load_default()
    register_config(config)

    hostname = os.environ.get("STOQLIB_TEST_HOSTNAME")
    dbname = os.environ.get("STOQLIB_TEST_DBNAME")
    username = os.environ.get("STOQLIB_TEST_USERNAME")
    password = os.environ.get("STOQLIB_TEST_PASSWORD")
    port = int(os.environ.get("STOQLIB_TEST_PORT") or 0)
    quick = request.config.getvalue("quick_mode")
    quick = quick or os.environ.get("STOQLIB_TEST_QUICK", None) is not None

    bootstrap_suite(
        address=hostname,
        dbname=dbname,
        port=port,
        username=username,
        password=password,
        quick=quick,
    )

    plugin_cls = request.config.getvalue("plugin_cls") or request.config.inicfg.get("PLUGIN_CLASS")
    if not quick and plugin_cls:
        _install_plugin(plugin_cls)
