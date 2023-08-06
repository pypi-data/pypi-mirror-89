#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: ZHANG XINZENG
# Created on 2020-12-24 15:17
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class BinaryDistribution(setuptools.dist.Distribution):
    def has_ext_modules(self):
        return True


setuptools.setup(
    name="robinpy",
    version="0.12.24",
    author="xinebf",
    author_email="me@xienbf.com",
    description="A beautiful song",
    long_description=long_description,
    package_data={"dolphin": ["excel.cp38-win_amd64.pyd"]},
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['pywin32'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8, <3.9',
    distclass=BinaryDistribution
)
