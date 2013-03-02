#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pimp',
    version='0.1dev',
    description='pimp installs magic packages. Install rpm packages from PyPi. No refunds.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/pimp',
    license='MIT',
    install_requires=['pip', 'shutilwhich', 'tempdir'],
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'pimp = pimp:main',
        ],
    }
)
