# -*- coding: utf-8 -*-

VERSION = '0.1.2'

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
    install_requires=["requests", "six>=1.10"],
    keywords=['nutshell', 'nutshell-crm', 'json-rpc'],
    classifiers=[],
)
