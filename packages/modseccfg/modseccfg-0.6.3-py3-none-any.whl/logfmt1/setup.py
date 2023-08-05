#!/usr/bin/env python3
# encoding: utf-8
# api: pip
# type: build
# title: config for setuptools
#
# Notably the .deb will install as just dist-packages/logfmt1.py.
# Whereas the .whl creates a logfmt1/__init__.py wrapper and
# directory structure.
# - share/ files shouldn't really reside within the pkg.
#

from pluginconf.setup import setup


setup(
    fn="./logfmt1.py",
    long_description="@README.rst",
    package_dir={"logfmt1": "./"},
    packages=["logfmt1"],
    package_data={
        "logfmt1": [
           "./share/*",
           "./share/update/*"
        ],
    },
    #data_files=[],
    entry_points={
        "console_scripts": [
            "logex=logfmt1.logex:main",
            "update-logfmt=logfmt1.update_logfmt:main",
        ]
    }
)

