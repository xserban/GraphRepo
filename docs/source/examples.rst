.. _EXAMPLES:

==================
Examples
==================

In the project's repository there are many examples on how to
use GraphRepo to index and mine data.

Please note that in order to run the plotting examples you have to install ``pandas`` and ``plotly``, for example using pip::

    $ pip install pandas

1. Index data
==============

In this example, we index all data from PyDriller in Neo4j.
The example assumes you are running a Neo4j instance in Docker, as indicated in :ref:`CONFIGURATION`.

In order to run the example, clone the projects using the following commands::

    $ git clone --recurse-submodules https://github.com/NullConvergence/GraphRepo
    $ cd graphrepo
    $ mkdir repos
    $ cd repos
    $ git clone https://github.com/ishepard/pydriller

In this step we cloned the GraphRepo project, which includes the example scripts to run
and the PyDriller project, which we want to experiment with.

In order to run the indexing example, make sure to configure the config file in ``examples/configs/pydriller.yml``
and set the ``neo`` object to your database settings.

Then run::

    $ python -m examples.index_all --config=examples/config/pydriller.yml

After indexing finishes, you can go to ``http://<database-url>:7474/browser/``
and explore the project, with a query like: ``MATCH (n) RETURN n``.


2. Retrieve all data
=====================

This step assumes you already indexed the PyDriller repository
in Neo4j, as indicated at Step 1.
In order to retrieve all information for PyDriller, we can run
the following example::

    $ python -m examples.mine_all --config=examples/config/pydriller.yml

This script will print the number of nodes indexed in the database.


3. Plot file complexity over time
===================================

This step assumes you already indexed the PyDriller repository
in Neo4j, as indicated at Step 1.
In this example we will use the miners to retrieve a file and
plot its complexity evolution over time.
The file used is ``examples/file_complexity.py``.
The complexity is stored in the ``UpdateFile`` relationship (see Data Structure).
The ``get_change_history`` from the ``File`` miner retrieves all the ``UpdateFile``
relationships that point to the file.

For plotting, in the example we map the data to a pandas DataFrame and use Plotly,
although any other libraries can be used.

In order to display the plot, run::

    $ python -m examples.file_complexity --config=examples/configs/pydriller.yml




3. Plot file methods complexity over time
==========================================

This step assumes you already indexed the PyDriller repository
in Neo4j, as indicated at Step 1.
In this example we will use the miners to retrieve and plot the complexity
evolution over time of all methods in a file.
The file used is ``examples/all_method_complexity.py``.
The complexity is stored in the ``UpdateFile`` relationship (see Data Structure).
We first get all the methods for a file, then, for each method, we get the
update information as in Step 2.

For plotting, in the example we map the data to a pandas DataFrame and use Plotly,
although any other libraries can be used.

In order to display the plot, run::

    $ python -m examples.all_method_complexity --config=examples/configs/pydriller.yml

