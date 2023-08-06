# Always prefer setuptools over distutils
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='twep',
      version='0.0.11',  # Required
      description='Multitask time-series forecasting',  # Optional
      long_description=long_description,  # Optional
      long_description_content_type='text/markdown',  # Optional (see note above)
      url='',  # Optional
      author='Aiola Labs',  # Optional
      author_email='',  # Optional
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
      python_requires='>=3.5',
      install_requires=['numpy>=1.19.1']  # Optional
)
