#!/usr/bin/env python
# coding: utf-8

from setuptools import setup


setup(
    name='yjs',
    version='0.0.2',
    author='yjs',
    author_email='yjs@gmail.com',
    url='https://91yjs.ml',
    description=u'云计算，永远的家',
    packages=['yjs'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'yjs=yjs:yjs',
        ]
    }
)
