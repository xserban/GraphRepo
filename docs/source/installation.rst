.. _INSTALLATION:

========================
Overview & Installation
========================

GraphRepo is a tool to index git repositorie in Neo4j, query and aggregate the data.
Under the hood it uses `PyDriller <https://github.com/ishepard/pydriller>`_ to parse the data from a repository.

Requirements
============

* Python 3.4 (or newer)
* Neo4j 3 - we recommend using Neo4j 3 until Py2Neo releases v5
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

    $ docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data/exp:/data --volume=$HOME/neo4j/logs/exp:/logs neo4j:3.0

Run the tests::

$ pytest


Or see the :ref:`EXAMPLES`.