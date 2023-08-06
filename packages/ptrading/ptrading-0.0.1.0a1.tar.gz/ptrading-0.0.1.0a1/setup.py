"""
# -*- coding: utf-8 -*-
# Copyright © 2020 Abhishek Pratapa. All rights reserved.
#
# Use of this source code is governed by a BSD-3-clause license that can
# be found in the LICENSE.txt file or at https://opensource.org/licenses/BSD-3-Clause
"""

import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ptrading",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.0.1.0a1",
    description="Trading Tools written on top of the Alpaca API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abhishekpratapa/ptrading",
    author="Abhishek Pratapa",
    author_email="abhishekpratapa@gmail.com",
    license="BSD-3-Clause",
    include_package_data=True,
    install_requires=[
        "alpaca-trade-api==0.51.0",
        "numpy==1.18.5"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)