from neo4j import GraphDatabase


class GraphRepo(object):
    def __init__(self, url, user, password):
        self._driver = GraphDatabase.driver(
            url, auth=(user, password),  encrypted=False)

    def close(self):
        self._driver.close()
