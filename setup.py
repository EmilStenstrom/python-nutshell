# -*- coding: utf-8 -*-

VERSION = '0.1.2'

from setuptools import setup, find_packages
setup(
    name='nutshell',
    packages=find_packages(),
    version=VERSION,
    description='A minimal python library to access Nutshell CRM:s JSON-RPC API.',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/python-nutshell',
    download_url='https://github.com/EmilStenstrom/python-nutshell/tarball/' + VERSION,
    install_requires=["requests"],
    keywords=['nutshell', 'nutshell-crm', 'json-rpc'],
    classifiers=[],
)
