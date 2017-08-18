#!/usr/bin/env python

from os.path import join, dirname

execfile(join(dirname(__file__), 'src', 'ImageCompareTool', 'version.py'))

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

long_description=open(join(dirname(__file__), 'README.md',)).read()

setup(
  name             = 'robotframework-imagecompare',
  version          = VERSION,
  description      = 'Robot Framework Image Compare Tool',
  long_description = long_description,
  author           = 'Bloopark systems GmbH & Co. KG',
  author_email     = 'info@bloopark.com',
  url              = '',
  license          = 'Apache License 2.0',
  keywords         = 'robotframework checking testautomation image layout',
  platforms        = 'any',
  zip_safe         = False,
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework'],
  packages         = ['ImageCompareTool'],
)