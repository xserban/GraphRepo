.. _DRILLERS:

==================
Drillers
==================

All Drillers parse a repository and insert it in Neo4j.
Under the hood all drillers uses PyDriller to extract data from a repository.

Drillers perform the following activities.
Given a config file, they:

* establish a connection to Neo4j (or raise an exception if the connection fails),
* parse the data from PyDriller,
* insert the data in Neo4j.


Currently there are 3 drillers available:

* Driller - default driller that stores the data parsed from the repository in RAM memory.
* CacheDriller - stores the data parsed from the repository on disk (thus saving RAM memory at the cost of more disk writes and decreased performance).
* QueueDriller - stores the data parsed from a repository to a queue. Currently it supports RabbitMQ and Artemis. Please take note that two drillers must be used in case of a queue: (i) one that parses the data from Git repos and (ii) one that indexes the data in Neo4j.
The queue driller is the most scalable one since it allows to have multiple instances for indexing. Thus it solves some scalability issues (e.g., PyDriller is single threaded).

In order to index the data, you will need a config file (see :ref:`CONFIGURATION`) and the
following code::

    from graphrepo.drillers.drillers import Driller

    # Initialize the database indexes
    try:
      driller.init_db()
    except Exception as exc:
      print("DB already initialized")

    # configure driller
    driller = Driller(config_path='path-to-yaml-config-file.yml')

    # drill (extract data and store it in Neo4j)
    driller.drill_batch()

    # merge duplicate nodes
    driller.merge_all()


For a complete example, see :ref:`EXAMPLES`.

