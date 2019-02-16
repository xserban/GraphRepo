""" This class holds all possible relationships in the graph
"""
from py2neo.data import Relationship

# class Relationships(object):
#   AUTHORSHIP = Relationship.type("Authorship")

class Authorship(Relationship): pass
class Parent(Relationship): pass