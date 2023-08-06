#!/usr/bin/env python
# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="TDhelper",
    version="1.7.3",
    keywords=("pip", "TDhelper", "featureextraction"),
    description="create spider class.",
    long_description=long_description,
    long_description_content_typ="text/markdown",
    license="MIT Licence",
    url="https://github.com/TangJing/TDlib",
    author="T.D",
    author_email="yeihizhi@163.com",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires=["bson==0.5.10",
                      "certifi==2020.4.5.1",
                      "chardet==3.0.4",
                      "idna==2.9",
                      "mysql-connector-python==8.0.19",
                      "protobuf==3.12.2",
                      "pycryptodome==3.9.7",
                      "pymongo==3.10.1",
                      "PyMySQL==0.9.3",
                      "python-dateutil==2.8.1",
                      "requests==2.23.0",
                      "six==1.15.0",
                      "urllib3==1.25.9",
                      "openpyxl==3.0.4",
                      "xlrd==1.1.0"
                      ]
)
