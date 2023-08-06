from setuptools import find_packages, setup
import os


VERSION = '0.1.0'
PACKAGE_NAME = 'montyhall'
AUTHOR = 'Jose Viegas'
AUTHOR_EMAIL = 'jviegas6@gmail.com'
URL = 'https://github.com/jviegas6/montyHall'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'This is a package to run the Monty Hall experiment'
with open('README.md', 'r') as fi:
    LONG_DESCRIPTION = fi.read()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pandas>=1.0.0'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.6'
      )