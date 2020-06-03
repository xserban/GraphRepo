.. _architecture_toplevel:

==================
Architecture
==================

GraphRepo consists of 3 main components:

* Driller - it is used to parse data from a git repository and insert records in Neo4j,
* Miners and MinerManager - components which hold default query in order to retrieve data from Neo4j, and
* Mappers - components used to transform the data retrieved by Miners in specific format, filter or sort data.

The advantage of using custom mappers is that the load on Neo4j can be decreased,
using lighter queries to extract the data and more intensive data processing in the
custom mappers. For example, one can write a mapper using Sparq on raw data extracted
from Neo4j and use the Sparq engine for scalability.

.. image:: /GraphRepoArch.svg
   :width: 600

Specific information about each component can be found using the links above.