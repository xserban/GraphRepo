```
$ cd <git-project>
$ python git2neo > git.sql
# import the output in a new database
$ bin/neo4j-shell -path git.db -file git.sql
# or
$ docker exec -ti $CONTAINER /var/lib/neo4j/bin/neo4j-shell -path git.db -file git.sql
```