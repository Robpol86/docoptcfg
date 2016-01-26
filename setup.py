#!/usr/bin/env python
"""Setup script for the project."""

from __future__ import print_function

import codecs
import os

from setuptools import find_packages, setup


def readme():
    """Try to read README.rst or return empty string if failed.

    :return: File contents.
    :rtype: str
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'README.rst'))
    handle = None
    try:
        handle = codecs.open(path, encoding='utf-8')
        return handle.read(131072)
    except IOError:
        return ''
    finally:
        getattr(handle, 'close', lambda: None)()


setup(
    author='@Robpol86',
    author_email='robpol86@gmail.com',
    classifiers=['Private :: Do Not Upload'],
    description='docopt wrapper adding config file and environment variable support.',
    install_requires=['docopt'],
    keywords='docopt config configuration environment',
    license='MIT',
    long_description=readme(),
    name='docoptcfg',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/Robpol86/docoptcfg',
    version='1.0.0',
    zip_safe=True,
)
