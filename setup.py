from setuptools import setup, find_packages

setup(name="graphrepo",
      version="0.1",
      description="A tool that maps a Github repo to Neo4j",
      url="https://github.com/NullConvergence/GraphRepo",
      license='Apache License',
      python_requires='>=3.5',
      install_requires=[
          'py2neo==4.2.0',
          'pydriller==1.7'
      ],
      packages=find_packages(),
      package_dir={'graphrepo': 'graphrepo'})
