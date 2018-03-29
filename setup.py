#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of requests2jmx-via-bzt.
# https://github.com/belonesox/requests2jmx-via-bzt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Stas Fomin <stas-fomin@yandex.ru>

from setuptools import setup, find_packages
from requests2jmx_via_bzt import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='requests2jmx-via-bzt',
    version=__version__,
    description='Convert any tests with requests like Selenium to Jmeter JMX file using blazemeter service.',
    long_description='''
Convert any tests with requests like Selenium to Jmeter JMX file using blazemeter service.
''',
    keywords='',
    author='Stas Fomin',
    author_email='stas-fomin@yandex.ru',
    url='https://github.com/belonesox/requests2jmx-via-bzt',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'requests2jmx-via-bzt=requests2jmx_via_bzt.cli:main',
        ],
    },
)
