#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-stoq",
    version="0.6.0",
    author="Stoq Team",
    author_email="stoq-devel@async.com.br",
    maintainer="Stoq Team",
    maintainer_email="stoq-devel@async.com.br",
    license="GNU GPL v3.0",
    url="https://github.com/stoq/pytest-stoq",
    description="A plugin to pytest stoq",
    long_description=read("README.rst"),
    packages=["pytest_stoq"],
    python_requires=">=3.4",
    install_requires=["pytest>=3.5.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={"pytest11": ["stoq = pytest_stoq.plugin"]},
)
