#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python library that allows you to interact programmatically with an instance of
the Genestack platform.
"""
from __future__ import absolute_import, print_function

from distutils.core import setup
exec(open('genestack_client/version.py').read())

setup(
    name='genestack_client',
    version=__version__,
    packages=['genestack_client', 'genestack_client.settings', 'genestack_client.scripts'],
    url='https://github.com/genestack/python-client',
    license='MIT',
    author='Genestack Limited',
    author_email='',
    description='Genestack Python Client Library',
    long_description=__doc__,
    long_description_content_type="text/markdown",
    install_requires=['keyring', 'requests', 'pyOpenSSL', 'jsonschema', 'future', 'pyrsistent==0.16.0'],
    python_requires='>2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    entry_points={
        'console_scripts': [
            'genestack-user-setup = genestack_client.scripts.genestack_user_setup:main',
            'genestack-shell = genestack_client.scripts.shell:main',
            'genestack-application-manager = genestack_client.scripts.genestack_application_manager:main',
            'genestack-uploader = genestack_client.scripts.genestack_uploader:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

    project_urls={
        'Documentation': 'http://genestack-client.readthedocs.io/en/stable/',
        'Source': 'https://github.com/genestack/python-client/',
        'Tracker': 'https://github.com/genestack/python-client/issues',
    },
    keywords=['genestack', 'genomics', 'api'],
)
