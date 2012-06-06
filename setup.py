# -*- coding: utf-8 -*-
"""
This module contains the tool of Products.RemoteProvider
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3.1dev'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(name='Products.RemoteProvider',
      version=version,
      description="Remote Provider Content Type",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        ],
      keywords='contenttype remote provider',
      author='Syslab.com GmbH',
      author_email='mailto:info@syslab.com',
      url='https://svn.syslab.com/svn/syslabcom/Products.RemoteProvider',
      license='GPL + EUPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'Products.LinguaPlone',
                        ],
      extras_require={
          'test': [
              'plone.app.testing',
              'mock',
          ],
      },
      entry_points="""
      # -*- entry_points -*-
      """,
      )
