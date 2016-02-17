# -*- coding: utf-8 -*-

VERSION = '0.2'

from setuptools import setup
setup(
    name='nutshell',
    packages=["nutshell"],
    version=VERSION,
    description='A minimal python library to access Nutshell CRM:s JSON-RPC API.',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/python-nutshell',
    download_url='https://github.com/EmilStenstrom/python-nutshell/tarball/' + VERSION,
    install_requires=["requests>=2.9.1", "six>=1.10.0"],
    tests_require=["mock>=1.0.1", "nose>=1.3.7"],
    test_suite="nose.collector",
    keywords=['nutshell', 'nutshell-crm', 'json-rpc'],
    classifiers=[],
)
