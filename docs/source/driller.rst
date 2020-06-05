.. _DRILLER:

==================
Driller
==================

The Driller component parses the repository data and indexes it in Neo4j.
Under the hood it uses PyDriller to get all data from a repository.

At the moment, the Driller performs the following activities in a sequential order.
Given a config file, it:

* establishes a connection to Neo4j (or raises an exception if the connection fails),
* parses the data from PyDriller,
* indexes the data in Neo4j.


In order to index the data, you will need a config file (see :ref:`CONFIGURATION`) and the
following code::

    from graphrepo.driller import Driller

    driller = Driller(config_path='path-to-yaml-config-file.yml')
    driller.drill_batch()


For a complete example, see :ref:`EXAMPLES`.

