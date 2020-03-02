from setuptools import setup, find_packages

setup(
      name="wRadia",
      author = "Ed Rial",
      version = "0.1",
      description='Python wrapper for Radia, easily accessible object attributes',
      dependency_links=['http://github.com/ochubar/Radia/tarball/master#egg=package-1.0&subdirectory=tree/master/cpp/py'],
      packages = find_packages(),
      install_requires = ['numpy'],
      )
#
