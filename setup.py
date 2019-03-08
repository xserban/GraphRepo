from setuptools import find_packages
from setuptools import setup

setup(name="graphrepo",
      version="0.1",
      description="A tool that maps a Github repo to Neo4j",
      url="https://github.com/NullConvergence/GraphRepo",
      author="NullConvergence",
      license='Apache2',
      install_requires=[
          'py2neo',
          'pydriller',
      ],
      packages=find_packages())
