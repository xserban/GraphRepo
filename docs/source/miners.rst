.. _MINERS:

==================
Miners
==================

Miners are special classes which hold default Neo4j queries that can be used to extract data.
At the moment, there are 4 standard miners, specific to the most important node entities in the graph:

* ``CommitMiner`` - holds all default queries for commits (including relationships to other nodes),
* ``DeveloperMiner`` - holds all default queries for developers (including relationships to other nodes),
* ``FileMiner`` - holds all default queries for files (including relationships to other nodes),
* ``MethodMiner`` - holds all default queries for methods (including relationships to other nodes),

and a ``MineManager``, which initializes and configures all miners.

We recommend to always use the ``MineManager`` for initialization, since there is no overhead over initializing only one miner.
Using a config file (see :ref:`CONFIGURATION`), the ``Minemanager`` can be initialized as follows::

    from graphrepo.miners import MineManager

    miner = MineManager(config_path=args.config)

    # The specific miners can now be accessed as:
    miner.commit_miner.get_all()

    miner.dev_miner.get_all()

    miner.file_miner.get_all()

    miner.method_miner.get_all()