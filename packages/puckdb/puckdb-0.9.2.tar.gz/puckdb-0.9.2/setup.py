#!/usr/bin/env python

#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of puckdb
# (see https://github.com/carstencodes/puckdb).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from setuptools import setup, find_packages

__VERSION__ = "0.9.2"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="puckdb",
    version=__VERSION__,
    license="BSD-3-Clause",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="A concurrent overlay on pickleDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/puckdb",
    install_requires=[],
    package_dir={"": "src"},
    keywords="da, platform, environment, development",
    python_requires=">=3.8, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Typing :: Typed",
    ],
)
