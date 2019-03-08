# GraphRepo

This tool maps a Github repository to a Neo4j database. Each entity in a repository has a custom model (which can be found in [graphrepo/models](https://github.com/NullConvergence/GraphRepo/tree/develop/graphrepo/models)).
Whenever we instantiate a new model, if a py2neo graph object is given to its constructor, a neo4j node is created.

### 1. Running the project

#### Prereq
The only requirement is to have Python and Docker installed on your system.

#### 1.1 Install the production release with pip

```
$ pip install graphrepo
```

#### Alternative: Install the development version
```
$ git clone https://github.com/NullConvergence/GraphRepo
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


#### 1.3 Index and vizualize your repo:

Please configure the constants in [examples/index_all.py](https://github.com/NullConvergence/GraphRepo/blob/develop/examples/index_all.py), then run the file using the
following command:

```
$ python examples/index_all.py
```

Go to [http://localhost:7474](http://localhost:7474) and use the first query from Section 2.



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
