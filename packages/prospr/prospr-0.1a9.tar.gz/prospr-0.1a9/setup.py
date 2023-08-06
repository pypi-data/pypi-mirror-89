#!/usr/bin/env python3
"""
File:           setup.py
Description:    This file contains the setup required for distributing the
                package on PyPi.org.
"""

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prospr",
    version="0.1a9",
    author="okkevaneck",
    description="A toolbox for protein folding with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okkevaneck/prospr",
    license_file="LICENSE",
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib",
        "seaborn",
        "numpy",
        "pandas"
    ],
    package_data={"": ["prospr/core/**/*.so"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 "
        "(LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
