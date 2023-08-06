import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")

setup(name='pycopy-cpython-pycopy',
      version='0.4',
      description='Pycopy module pycopy ported to CPython',
      long_description='This is a compatibility module for the standard library of Pycopy project\n(https://github.com/pfalcon/pycopy). It allows applications using\nPycopy APIs to run on CPython.\n',
      url='https://github.com/pfalcon/pycopy-lib',
      author='Paul Sokolovsky',
      author_email='pycopy-dev@googlegroups.com',
      maintainer='Paul Sokolovsky',
      maintainer_email='pycopy-dev@googlegroups.com',
      license='MIT',
      py_modules=['pycopy', 'pycopy_imphook'],
      install_requires=['pycopy-cpython-uio'])
