""" This class holds all possible relationships in the graph
"""
from py2neo.data import Relationship

class Branch(Relationship): pass
class Authorship(Relationship): pass
class Parent(Relationship): pass

class YearMonth(Relationship): pass
class MonthDay(Relationship): pass
class DayCommit(Relationship): pass