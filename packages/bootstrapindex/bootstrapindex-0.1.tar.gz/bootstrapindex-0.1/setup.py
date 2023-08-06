#In this directory, type pip install .
from setuptools import setup

setup(name='bootstrapindex',
      version='0.1',
      description='Returns block bootstrap indexes for walk-forward analysis (expanding or sliding window)',
      packages=['bootstrapindex'],
      author = 'Jirong Huang',
      author_email = 'jironghuang88@gmail.com',
      zip_safe=False)

