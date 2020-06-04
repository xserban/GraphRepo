.. _architecture_toplevel:

==================
Architecture
==================

GraphRepo consists of 3 main components:

* :ref:`DRILLER` - component used to parse data from a git repository and insert records in Neo4j,
* :ref:`MINERS` and MinerManager - components which hold default queries and interfaces for retrieving data from Neo4j, and
* :ref:`MAPPERS` - components used to transform the data retrieved by Miners in specific format, filter or sort data.

The advantage of using custom mappers is that the load on Neo4j can be decreased,
using lighter queries to extract the data and more intensive data processing in the
custom mappers. For example, one can write a mapper using PySpark on raw data extracted
from Neo4j and use the Apache Spark engine for scalability.

.. image:: /GraphRepoArchLong.svg
   :width: 500
   :align: center

Specific information about each component can be found using the links above.