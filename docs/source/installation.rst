.. _INSTALLATION:

========================
Overview & Installation
========================

GraphRepo is a tool that indexes Git repositories in Neo4j, and allows to query and aggregate the data.
Under the hood it uses `PyDriller <https://github.com/ishepard/pydriller>`_ to parse the data from a repository.

Requirements
============

* Python 3.4 (or newer)
* Neo4j 3
* Docker (Optional) - we recommend to use Docker for Neo4j (as indicated below)

Installation - using pip
=========================

Assuming python and pip are installed, use:

.. sourcecode:: none

    $ pip install graphrepo


Installation - clone source code (dev version)
===============================================

The latest development version can be cloned from Github::

    $ git clone --recurse-submodules https://github.com/NullConvergence/GraphRepo
    $ cd graphrepo


Install the requirements:

.. sourcecode:: none

    $ pip install -r requirements.txt

Run a docker instance with Neo4j::

    $ docker run -p 7474:7474 -p 7687:7687 -v $HOME/neo4j/data:/data -v $HOME/neo4j/plugins:/plugins  -e NEO4JLABS_PLUGINS=\[\"apoc\"\]   -e NEO4J_AUTH=neo4j/neo4jj neo4j:3.5.11

Run the tests::

$ pytest


Or see the :ref:`EXAMPLES`.