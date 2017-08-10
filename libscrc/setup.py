# -*- coding:utf8 -*-
""" Setup script for crc16 library. """
from os import path
from setuptools import setup, find_packages, Extension
from codecs import open

# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library CRC Modules.
# History:  2017-08-09 Wheel Ver:0.0.1 [Heyn] Initialize
#           2017-08-10 Wheel Ver:0.0.2 [Heyn] New CRC8

"""
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='libscrc',
    version='0.0.2',

    description='Library for calculating CRC8\CRC16\CRC32',
    long_description=long_description,

    url='http://heyunhuan513.blog.163.com',

    author='Heyn',
    author_email='heyunhuan@gmail.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords=['CRC16', 'CCITT', 'XMODEM', 'KERMIT'],

    # packages=find_packages(exclude=['libscrc.']),
    packages=['libscrc'],
    ext_modules=[Extension('libscrc._crc8',  sources=['src/_crc8module.c' ]),
                 Extension('libscrc._crc16', sources=['src/_crc16module.c']),
                 Extension('libscrc._crc32', sources=['src/_crc32module.c']),
                ],

)
