"""File for build project in python-packet"""

from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='splitres',
    version='1.2',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://gitwork.ru/barabass/splitres.git',
    author='German Borovkov'
)
