#!/usr/bin/env python

from distutils.core import setup

setup(name='underscore.py',
      version='0.1.6',
      description='Port of underscore.js into python',
      author='Serkan Yersen',
      author_email='serkanyersen@gmail.com',
      url='https://github.com/serkanyersen/underscore.py/',
      packages=['underscore'],
      package_dir={'underscore': 'src'}
     )
