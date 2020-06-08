.. _DRILLERS:

==================
Drillers
==================

All Drillers parse a repository and insert it in Neo4j.
Under the hood all drillers uses PyDriller to extract data from a repository.

At the moment, all Drillers perform the following activities, in a sequential order.
Given a config file, they:

* establish a connection to Neo4j (or raise an exception if the connection fails),
* parse the data from PyDriller,
* insert the data in Neo4j.


Currently there are 2 drillers available:

* Driller - default driller that stores the data parsed from the repository in RAM memory, and
* CacheDriller - stores the data parsed from the repository on disk (thus saving RAM memory at the cost of more disk writes and decreased performance).

In order to index the data, you will need a config file (see :ref:`CONFIGURATION`) and the
following code::

    from graphrepo.drillers.drillers import Driller

    driller = Driller(config_path='path-to-yaml-config-file.yml')
    driller.drill_batch()


For a complete example, see :ref:`EXAMPLES`.

