#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup

setup(
    name = 'TracCAS',
    version = '2.0.1',
    packages = ['traccas'],

    author = 'Noah Kantrowitz',
    author_email = 'noah@coderanger.net',
    description = 'A modified authentication plugin to use the Yale CAS system.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license = 'BSD',
    keywords = 'trac 0.11 plugin cas authentication',
    url = 'http://trac-hacks.org/wiki/TracCasPlugin',

    install_requires = ['Trac'],

    entry_points = {
        'trac.plugins': [
            'traccas.traccas = traccas.traccas'
        ]
    }
)
