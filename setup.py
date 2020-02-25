from setuptools import setup, find_packages

setup(
      name="wRadia",
      author = "Ed Rial",
      version = "0.1",
      description='Python wrapper for Radia, easily accessible object attributes',
      dependency_links=['https://github.com/ochubar/Radia/blob/master/cpp/py/setup.py'],
      packages = find_packages(),
      install_requires = ['numpy',
                          'radia'],
      )
#
