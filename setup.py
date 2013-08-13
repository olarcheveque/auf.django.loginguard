from setuptools import setup, find_packages
import sys, os

version = '0.0'
name = 'auf.django.loginguard'

setup(name=name,
      version=version,
      description="Provides login guard toolkit",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django authentication security',
      author='Olivier Larchev\xc3\xaaque',
      author_email='olivier.larcheveque@auf.org',
      url='http://pypi.auf.org/%s' % name,
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages = ['auf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
