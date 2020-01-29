from pytest_stoq.fixtures import *  # noqa


def pytest_addoption(parser):
    group = parser.getgroup("stoq")
    group.addoption(
        "--skip-env-setup",
        action="store_true",
        dest="skip_env_setup",
        default=None,
        help="Skip environment setup. Use with caution.",
    )
    group.addoption(
        "--plugin-cls",
        action="store",
        dest="plugin_cls",
        default=None,
        help=(
            "Specify the module path to the stoq plugin to be installed. "
            "e.g. my_plugin.plugin.PluginClass"
        ),
    )
    group.addoption(
        "--quick",
        action="store_true",
        dest="quick_mode",
        default=None,
        help="Quick database setup mode. Use with caution.",
    )
    group.addoption(
        "--stoq-plugins",
        action="store",
        dest="stoq_plugins",
        default=None,
        help=(
            "Specify a comma-separated list of stoq plugin names to be installled. "
            "e.g. nfce,passbook"
        ),
    )
