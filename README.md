# GraphRepo ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square) [![BCH compliance](https://bettercodehub.com/edge/badge/NullConvergence/GraphRepo?branch=develop)](https://bettercodehub.com/)

This tool indexes Git repositories in Neo4j and implements multiple queries to select and process the data.
For a complete description, see the [online documentation](https://graphrepo.readthedocs.io/en/latest/).

<p align="center">
  <img src="https://raw.githubusercontent.com/NullConvergence/GraphRepo/develop/docs/source/GraphRepoSchema.svg">
</p>

###  1. Installation & First run

#### 1.1 Prereq
The only requirement is to have Python >=3.5 and Docker installed on your system.

#### 1.2 Install the production release with pip using the following command. Please be aware that the final release may miss some functionality.

```
$ pip install graphrepo
```

#### Alternative: Install the development version
```
$ git clone --recurse-submodules https://github.com/NullConvergence/GraphRepo
$ cd graphrepo/
$ pip install -r requirements.txt
```


#### 1.3 Run and configure Neo4j

The following instructions assume the Docker daemon is running on your machine.

```
$ docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data/exp:/data --volume=$HOME/neo4j/logs/exp:/logs --env NEO4J_AUTH=neo4j/neo4jj  neo4j:3.0
```

Open a browser window and go to [http://localhost:7474](http://localhost:7474). Here you can configure the neo4j password.
The default one is *neo4j*.

##### Optionally, configure Neo4j to allow larger heap size using the following attributes with the command above:

```
--env NEO4J_dbms_memory_pagecache_size=4g
--env NEO4J_dbms_memory_heap_max__size=4g
```

#### 1.4. Index and vizualize a repo

Please clone a project configure the constants in a config file, e.g., clone
the [GraphRepo](https://github.com/NullConvergence/GraphRepo) project in the ``repos`` folder and update the yaml file at [examples/configs/graphrepo.yml](https://github.com/NullConvergence/GraphRepo/blob/develop/examples/configs/graphrepo.yml).
Then index the repo using:

```
$ python -m examples.index_all --config=examples/configs/graphrepo.yml
```

Go to [http://<neo4j-address>:7474](http://<>:7474) and use the first query from Section 3.


#### 1.5. Retrieve all data from Neo4j

Assuming you succeded in step 1.4, use the follwing command to retrieve all indexed data:

```
$ python -m examples.mine_all --config=examples/configs/graphrepo.yml
```


### 2. Examples

For a comprehensive introduction and more examples, see the [documentation](https://graphrepo.readthedocs.io/en/latest/examples.html).



### 3. Useful Neo4j queries

#### 2.1 Match all nodes in a graph
```
MATCH (n) RETURN n
```


#### 2.2 Delete all nodes in a graph

```
MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
```



This project is enabled by [Pydriller](https://github.com/ishepard/pydriller).
