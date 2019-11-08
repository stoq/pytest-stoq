===========
pytest-stoq
===========

.. image:: https://img.shields.io/pypi/v/pytest-stoq.svg
    :target: https://pypi.org/project/pytest-stoq
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-stoq.svg
    :target: https://pypi.org/project/pytest-stoq
    :alt: Python versions

.. image:: https://circleci.com/gh/stoq/pytest-stoq.svg?style=svg
    :target: https://circleci.com/gh/stoq/pytest-stoq
    :alt: CI Build

A plugin to pytest stoq.

This plugin automatically set up the stoq test environment. It also provide a range of
fixtures to ease the testing of stoq-related projects.


Installation
============

You can install "pytest-stoq" via `pip`_ from `PyPI`_::

    $ pip install pytest-stoq


Command-line options
====================

- ``--plugin-cls``: the plugin class path to be installed. Useful for testing stoq plugin projects.
- ``--quick``: setup stoq using the quick strategy.
- ``--skip-env-setup``: pytest-stoq won't setup the database, install plugins etc. (in case you already have the test env ready).

Fixtures
========

The plugin provides the following fixtures:

- ``store``: an instance of storm's (ORM) store used to access the database. It suffers rollback after each test case and cannot be committed, closed or rollbacked manually
- ``example_creator``: instance creates (inserts) database objects with example/test data
- ``current_station``
- ``current_user``
- ``current_branch``
- ``current_till``


Local Development
=================

(optional) Setup your virtualenv using python 3.5+

Install test requirements::

    $ pip install -Ur requirements-test.txt

Setup pre-commit::

    $ pre-commit install

Run tests using pytest::

    $ make test


License
=======

Distributed under the terms of the `GNU GPL v3.0`_ license, "pytest-stoq" is free and open source software


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
