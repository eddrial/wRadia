from setuptools import setup, find_packages

setup(
      name="wRadia",
      author = "Ed Rial",
      version = "0.1",
      dependency_links=['http://github.com/eddrial/aapy/tarball/master#egg=package-1.0'],
      packages = find_packages(),
      install_requires = ['numpy'],
      )
#