from setuptools import setup, find_packages

setup(
      name="wradia",
      author = "Ed Rial",
      version = "0.1",
      description='Python wrapper for Radia, easily accessible object attributes',
      dependency_links=['http://github.com/ochubar/Radia/tarball/master#egg=package-1.0&subdirectory=env/radia_python'],
      packages = find_packages(),
      install_requires = ['numpy',
                          'radia',
                          ''],
      package_data={'': ['radia_py3_7_x86_64.so']},
      )
#
