from setuptools import setup, find_packages


def read_reqs(filename: str):
  req = []
  with open(filename, 'r') as f:
    for line in f:
      if line.strip() and not line.startswith('-r'):
        req.append(line.strip())

  return req


install_requires = read_reqs("requirements.txt")

setup(name="graphrepo",
      version="0.2",
      description="A tool that maps a Github repo to Neo4j",
      url="https://github.com/NullConvergence/GraphRepo",
      license='Apache License',
      python_requires='>=3.4',
      install_requires=install_requires,
      packages=find_packages(),
      package_dir={'graphrepo': 'graphrepo'})
