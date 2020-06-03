.. _CONFIGURATION:

==================
Configuration
==================

For any activity, GraphRepo uses a yaml (.yml) configuration with 2 objects:

* a Neo4j instance configuration, and
* a repository configuration,

as follows::

    neo:
      db_url: localhost # the url for the Neo4j database
      port: 7687 # the Neo4j port
      db_user: neo4j # Neo4j authentication username
      db_pwd: neo4jj # Neo4j authentication password
      batch_size: 100 # the batch size for inserting the records in Neo4j - this setting depends on the Neo4j resources

    project:
      repo: repos/pydriller/ # the repository filepath
      start_date: "1 February, 2018" # the start date for indexing (leave empty if it corresponds with the initial start date of the project)
      end_date: "30 March, 2018" # the start date for indexing (leave empty if it corresponds with the last commit)
      project_id: 'pydriller' # a unique project id for the database


Neo4j configuration
===========

GraphRepo connects to Neo4j using the Bold REST API from `py2neo asd>`_.
Currently the only attributes needed to connect are the url+port and the authentication credentials.
All other configurations (e.g., setting the user permissions) are done on the database side.


Repository configuration
===========

In order to insert a repository in the database, it has to be cloned on the local machine (where GraphRepo will run).
Afterwards, we can link the cloned repository with GraphRepo using the ``project.repo`` attribute in the config file.

Moreover, if we don't want to use all the repository data (e.g., if the repository is very large), we can configure
the index dates using the ``project.start_date`` and ``project.end_date`` attributes

The ``project.project_id`` attribute is used to give each project a unique identifier.
Currently, GraphRepo indexes all repositories in the same database.
This decision allows to mine information about developers that work at different projects (think of teams of developers)
without merging data from different databases.


For examples of config files, see the projects repository, ``examples/configs/pydriller.yml``.






