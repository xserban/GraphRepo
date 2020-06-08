.. _DS:

==================
Schema
==================

The resulting Neo4j schema consists of 5 node types and 6 relationship types, as illustrated below:

.. figure:: /GraphRepoSchema.svg
   :width: 45 %
   :align: center

Nodes
===========


Branch
-----------

Each branch identified by PyDriller is indexed as a node with the following attributes::

  {
    "hash": "string - unique identifier",
    "project_id": "string - project id from config (can be used to select all branches from a project)",
    "name": "string - branch name",
  }

Commit
-----------

Each commit is indexed as a node with the following attributes::

  {
    "hash": "string - unique identifier which corresponds with the commit hash in git",
    "is_merge": "int - 1 if the commit is merge, 0 otherwise",
    "timestamp": "int - Unix epoch, time of the commit",
    "project_id": "string - project id from config (can be used to select all branches from a project)"
  }



Developer
-----------

Each developer is indexed as a node with the following attributes::

  {
    "hash": "string - unique identifier",
    "name": "string - developer name as in git",
    "email": "string - developer email as in git",
  }

Currently the mail and email information is not anonymized.

File
-----------


Each file is indexed as a node with the following attributes::

  {
    "hash": "string - unique identifier",
    "name": "string - file short name as in git",
    "project_id": "string - project id from config (can be used to select all branches from a project)",
    "type": "string - file extension, e.g., '.py'"
  }



Method
-----------

Each method is indexed as a node with the following attributes::

  {
    "hash": "string - unique identifier",
    "name": "string - method name as in file",
    "file_name": "string - parent file name",
    "project_id": "string - project id from config (can be used to select all branches from a project)",
    "type": "string - file extension, e.g., '.py'"
  }



Relationships
==============

Author
-----------

An Author relationship exists between each commit and its author.
The direction is from Commit to Author and the relationship attributes are::

  {
    "timestamp": "int - Unix epoch, time of the commit"
  }


BranchCommit
-----------
A BranchCommit relationship exists between each branch and the branch commits.
The direction is from Branch to Commit. This relationship does not have any special attributes.


Method
-----------

An Method relationship exists between each file and its methods.
The direction is from File to Method. This relationship does not have any special attributes.
In order to find out if the method is still part of the file or it was deleted, we can use the FileMiner.


Parent
-----------
A parent relationship exists between each commit its parent/parents.
This relationship does not have any special attributes.


UpdateFile
-----------

An UpdateFile relationship exists between a commit that edited a file and the edited file.
The direction is from Commit to File and the relationship attributes are::

  {
    "timestamp": "int - Unix epoch, time of the commit",
    "old_path": "string - old path, if the file was moved (see type attribute)",
    "path": "string - current file path",
    "diff: "string - commit diff",
    "source_code": "string - source code after the commit",
    "source_code_before": "string - source before after the commit",
    "nloc": "int - file lines of code after the commit",
    "complexity": "int - file complexity after the commit",
    "token_count": "int - number of tokens after the commit",
    "added": "int - number of lines added in commit",
    "removed": "int - number of lines removed in commit",
    "type": "string - type of update. Possible values are: 'ADD', 'COPY', 'RENAME', 'DELETE', 'MODIFY', 'UNKNOWN' "
  }


UpdateMethod
-------------

An UpdateMethod relationship exists between a commit that edited a method and the edited method.
The direction is from Commit to Method and the relationship attributes are::

  {
    "timestamp": "int - Unix epoch, time of the commit",
    "long_name": "string - method long name, including parameters",
    "parameters": "string - method parameters",
    "complexity": "int - method complexity, after commit",
    "nloc": "int - method lines of code, after commit",
    "fan_in": "int - method fan in, after commit",
    "fan_out": "int - method fan out, after commit",
    "general_fan_out": "int -method general fan out, after commit",
    "length": "int -method general fan out, after commit",
    "token_count": "int -method nr of tokens, after commit",
    "start_line": "int -method start line, after commit",
    "end_line": "int -method end line, after commit",
 }
