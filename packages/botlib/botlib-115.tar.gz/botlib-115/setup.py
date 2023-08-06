# BOTLIB - pure python3 bot library
#
# this file is place in the public domain

"library to program bots"

import os

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='115',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="pure python3 bot library you can use to program bots",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    namespace_packages=["bot"],
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
