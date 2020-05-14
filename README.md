# GraphRepo [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/SE-ML/awesome-seml/blob/master/contributing.md) [![BCH compliance](https://bettercodehub.com/edge/badge/NullConvergence/GraphRepo?branch=develop)](https://bettercodehub.com/)

This tool maps a Github repository to a Neo4j database. Each entity in a repository has a custom model (which can be found in [graphrepo/models](https://github.com/NullConvergence/GraphRepo/tree/develop/graphrepo/models)).
Whenever we instantiate a new model, if a py2neo graph object is given to its constructor, a neo4j node is created.
The new miners and mappers enable queries to Neo4j from GraphRepo. You can write your own miners for specific queries or data aggregation. Writing custom miners instead of querying Neo4j outside GraphRepo has several advantages: (1) reproducibility - sharing a list of repositories and a custom miner would be sufficient to reproduce research results, (2) flexibility - write custom mappings and aggregations in python, which are not possible in Neo4j (among with miners one can also define custom mappers, which can be any aggregation function or transformation to any custom data type), (3) increased scalability/elasticity for big data - the custom miners and mappers can make use of big data technologies, such as Spark or scientific computational libraries such as Numpy to scale processing on big data (instead of scaling Neo4j nodes).

###  Running the project

#### 1. Prereq
The only requirement is to have Python and Docker installed on your system.

#### 1.1 Install the production release with pip using the following command. Please be aware that the final release may miss some functionality.

```
$ pip install graphrepo
```

#### Alternative: Install the development version
```
$ git clone --recurse-submodules https://github.com/NullConvergence/GraphRepo
$ cd graphrepo/
$ python setup.py develop
```


#### 1.2 Run and configure Neo4j

The following instructions assume the Docker daemon is running on your machine.

```
$ docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data/exp:/data --volume=$HOME/neo4j/logs/exp:/logs neo4j:3.0
```

Open a browser window and go to [http://localhost:7474](http://localhost:7474). Here you can configure the neo4j password.
The default one is *neo4j*.



#### 2. Index and vizualize a repo

Please configure the constants in [examples/config.yml](https://github.com/NullConvergence/GraphRepo/blob/develop/examples/config.yml), then run the file using the
following command:

```
$ python index_all.py
```

Go to [http://localhost:7474](http://localhost:7474) and use the first query from Section 2.


#### 3. Mine data from the repo
Please configure the constants in [examples/config.yml](https://github.com/NullConvergence/GraphRepo/blob/develop/examples/config.yml), then run the miners using the
following command:

```
$ python mine_all.py
```




### 2. Useful Neo4j queries

#### 2.1 Match all nodes in a graph
```
MATCH (n) RETURN n
```


#### 2.2 Delete all nodes in a graph

```
MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
```



This project is enabled by [Pydriller](https://github.com/ishepard/pydriller).
