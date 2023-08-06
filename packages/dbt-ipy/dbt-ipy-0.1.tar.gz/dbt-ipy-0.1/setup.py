# setup.py
from setuptools import setup

setup(
  name="dbt-ipy",
  version="0.1",
  packages=["dbt-ipy"],
  license="GNU GPLv3",
  author="José María Riego",
  author_email="jmriego@telefonica.net",
  url="http://www.github.com/jmriego/dbt-ipy",
  description="IPython magic to use dbt",
  long_description=open("README.rst").read(),
  keywords="ipython dbt sql",
  install_requires = ['ipython', 'dbt'],
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Framework :: IPython",
      "Programming Language :: Python",
  ],
)
