# GraphRepo ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square) [![BCH compliance](https://bettercodehub.com/edge/badge/NullConvergence/GraphRepo?branch=develop)](https://bettercodehub.com/)

GraphRepo is a tool for mining software repositories in real time. It indexes Git repositories in Neo4j and implements multiple queries to select and process the repository data.

For a complete description, see the [online documentation](https://graphrepo.readthedocs.io/en/latest/).
<!-- For a [demo](https://github.com/NullConvergence/GraphRepo-Demo) using Jupyter notebooks follow this [link](https://github.com/NullConvergence/GraphRepo-Demo) or see the [video demo](https://www.youtube.com/watch?v=x1ha0fRltGI). -->

<p align="center">
  <img src="https://raw.githubusercontent.com/NullConvergence/GraphRepo/develop/docs/source/GraphRepoSchema.svg">
</p>x

###  1. Installation & First run

#### 1.1 Prereq
The only requirement is to have Python >=3.5 and Docker installed on your system.

#### 1.2 Install using pip

The production release can be installed using pip:

```
$ pip install graphrepo
```

<!--
#### Alternative: Install the development version

Note that the development version may have new, but unreliable or poorly documented features.

```
$ git clone --recurse-submodules https://github.com/NullConvergence/GraphRepo
$ cd graphrepo/
$ pip install -r requirements.txt
```
-->


#### 1.3 Run and configure Neo4j

The following instructions assume the Docker daemon is running on your machine:

```
$ docker run -p 7474:7474 -p 7687:7687 -v $HOME/neo4j/data:/data -v $HOME/neo4j/plugins:/plugins  -e NEO4JLABS_PLUGINS=\[\"apoc\"\]   -e NEO4J_AUTH=neo4j/neo4jj neo4j:3.5.11
```

Open a browser window and go to [http://localhost:7474](http://localhost:7474). Here you can configure the neo4j password.
The default one is *neo4jj*.

##### Optionally, configure Neo4j to allow larger heap size using the following attributes with the command above:

```
--env NEO4J_dbms_memory_pagecache_size=4g
--env NEO4J_dbms_memory_heap_max__size=4g
```

#### 1.4. Index and vizualize a repo

In order to index a repository, you must clone it on localhost, and point GraphRepo to it. For example:
```
$ mkdir repos
$ cd repos
$ git clone https://github.com/ishepard/pydriller
```

Now enter the [examples](/examples) folder from this repository, and edit the configuration file for PyDriller to reflect the database URL and desired batch size:
```
$ cd ../examples/
$ nano configs/pydriller.yml
```

Afterwards, we can run the script from the examples folder which indexes the repository in Neo4j:

```
$ python -m examples.index_all --config=examples/configs/pydriller.yml
```

Go to [http://localhost:7474](http://localhost:7474) and use the query from 3.1


#### 1.5. Retrieve all data from Neo4j using GraphRepo

Assuming you succeded in step 1.4, use the follwing command to retrieve all indexed data:

```
$ python -m examples.mine_all --config=examples/configs/pydriller.yml
```


### 2. Examples

For a comprehensive introduction and more examples, see the [documentation](https://graphrepo.readthedocs.io/en/latest/examples.html).



### 3. Useful Neo4j queries for the web interface

#### 3.1 Match all nodes in a graph
```
MATCH (n) RETURN n
```


#### 3.2 Delete all nodes and relationships in a graph

```
MATCH (n) DETACH DELETE n;
```

#### 3.2 Delete a limited number commits and relationship

```
MATCH (n:Commit)
// Take the first 100 commits nodes and their rels
WITH n LIMIT 100
DETACH DELETE n
RETURN count(*);
```



This project is enabled by [Pydriller](https://github.com/ishepard/pydriller).
