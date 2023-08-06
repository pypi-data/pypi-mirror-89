#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import dreamtools
from dreamtools import cfgloader
from dreamtools import tools

cfg = ["cfg/*.yml"]
with open('README.md') as readme:
    long_description = readme.read()

setup(
    name= 'dreamtools-dreamgeeker',
    install_requires= ['setuptools','pyaml',
                      'requests', 'cerberus>= 1.3.2', 'pillow >= 8.0.1', 'pytz>=pytz==2020.4'
                      ],
    author= "dreamgeeker",
    author_email= "dreamgeeker@couleurwest-it.com",
    version= dreamtools.__version__,
    description= "outils de developpement de base",
    long_description= long_description,
    url='https://github.com/couleurwest/dreamgeeker-tools',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    packages=find_packages(),
    package_data={'dreamtools': cfg},
    include_package_data=True,
    python_requires='>=3.8',
    entry_points= {
        'console_scripts': [
            'tools-installer = scripts.__main__:setproject'
        ],
    }
)