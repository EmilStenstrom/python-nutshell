# -*- coding: utf-8 -*-
from setuptools import setup
VERSION = '0.2'

download_url = 'https://github.com/EmilStenstrom/python-nutshell/tarball/{0}'
setup(
    name='nutshell',
    packages=["nutshell"],
    version=VERSION,
    description='A python library to access Nutshell CRM:s JSON-RPC API.',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/python-nutshell',
    download_url='https://github.com/EmilStenstrom/python-nutshell/tarball/' + VERSION,
    install_requires=["requests>=2.9.1", "six>=1.10.0"],
    tests_require=["mock>=1.0.1", "nose>=1.3.4", "flake8>=2.5.4"],
    test_suite="nose.collector",
    keywords=['nutshell', 'nutshell-crm', 'json-rpc'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ])
