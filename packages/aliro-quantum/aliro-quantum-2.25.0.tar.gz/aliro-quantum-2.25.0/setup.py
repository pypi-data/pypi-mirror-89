# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 2.25.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301
from os import path

NAME = "aliro-quantum"
VERSION = "2.25.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

REQUIRES = [
    "certifi",
    "python-dateutil",
    "six >= 1.10",
    "sseclient-py >= 1.7",
    "urllib3 >= 1.15"
]

setup(
    name=NAME,
    version=VERSION,
    description="Aliro Quantum App",
    author="OpenAPI Generator community",
    author_email="nick@aliroquantum.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Aliro Quantum App"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
