"""
Utility package for Python
"""
from setuptools import setup

setup(name='kelmore-utils',
      version='1.0',
      description='Utility package for Python',
      author='kelmore5',
      author_email='kelmore5@gmail.com',
      license='MIT',
      packages=['kelmore_utils', 'kelmore_utils.app', 'kelmore_utils.db', 'kelmore_utils.types'],
      install_requires=[
          'xlrd', 'openpyxl', 'dill', 'pbkdf2', 'pycryptodome'
      ],
      zip_safe=False)
