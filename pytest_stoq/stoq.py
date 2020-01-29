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

    if plugin_name not in manager.installed_plugins_names:
        with stoqlib.api.new_store() as store:
            manager.install_plugin(store, plugin_name)

    if plugin_name not in manager.active_plugins_names:
        manager.activate_plugin(plugin_name)


def _setup_test_environment(request):
    plugin_config = _get_plugin_configs(request.config)
    if plugin_config['skip_env_setup']:
        return

    stoq_config = StoqConfig()
    stoq_config.load_default()
    register_config(stoq_config)

    quick = plugin_config['quick_mode'] or _to_falsy(os.environ.get("STOQLIB_TEST_QUICK", None))
    bootstrap_suite(
        address=os.environ.get("STOQLIB_TEST_HOSTNAME"),
        dbname=os.environ.get("STOQLIB_TEST_DBNAME"),
        port=int(os.environ.get("STOQLIB_TEST_PORT") or 0),
        username=os.environ.get("STOQLIB_TEST_USERNAME"),
        password=os.environ.get("STOQLIB_TEST_PASSWORD"),
        quick=quick,
        extra_plugins=plugin_config['extra_plugins'],
    )

    plugin_cls = plugin_config['plugin_cls']
    if plugin_cls:
        _install_plugin(plugin_cls)


def _get_plugin_configs(config):
    extra_plugins = config.getvalue("stoq_plugins") or config.inicfg.get("STOQ_PLUGINS", '')
    extra_plugins = extra_plugins.split(',') if extra_plugins else None
    return {
        'plugin_cls': config.getvalue("plugin_cls") or config.inicfg.get("PLUGIN_CLASS"),
        'quick_mode': config.getvalue("quick_mode"),
        'skip_env_setup': config.getvalue("skip_env_setup"),
        'extra_plugins': extra_plugins
    }


def _to_falsy(value):
    if value in ('0', '', 'None', 'False', 'false', 'f'):
        return False
    return bool(value)
