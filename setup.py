#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='projectbook',
      version='0.1',
      packages=find_packages(),
      package_data={'projectbook': ['bin/*.*', 'static/*.*', 'templates/*.*']},
      exclude_package_data={'projectbook': ['bin/*.pyc']},
      scripts=['projectbook/bin/manage.py'])
