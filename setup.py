#!/usr/bin/env python
"""
sentry-redflash
===============

An extension for Sentry which integrates with Redflash. (SMS/twitter
notifications, https://github.com/aquamatt/RedFlash)

:copyright: (c) 2012 by David Szotten.
:license: MIT, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=4.6.0',
]

setup(
    name='sentry-redflash',
    version='0.0.7',
    author='David Szotten',
    author_email='Author name (as one word) at gmail.com',
    url='http://github.com/davidszotten/sentry-redflash',
    description='A Sentry extension which integrates with Redflash.',
    long_description=__doc__,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
       'sentry.plugins': [
            'pluginname = sentry_redflash.plugin:RedflashPlugin'
        ],
    },
)
