#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

if sys.version_info < (2, 7):
    print('thefuck requires Python version 2.7 or later' +
          ' ({}.{} detected).'.format(*sys.version_info[:2]))
    sys.exit(-1)
elif (3, 0) < sys.version_info < (3, 3):
    print('thefuck requires Python version 3.3 or later' +
          ' ({}.{} detected).'.format(*sys.version_info[:2]))
    sys.exit(-1)

VERSION = '1.48'

install_requires = ['psutil', 'colorama', 'six']

if sys.version_info < (3, 4):
    install_requires.append('pathlib')

setup(name='thefuck',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/thefuck',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'release']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={'console_scripts': [
          'thefuck = thefuck.main:main',
          'thefuck-alias = thefuck.shells:app_alias']})
