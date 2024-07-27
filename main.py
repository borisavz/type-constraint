from typing import Optional

from constraint import *


class Type:
    def __le__(self, other):
        raise Exception("LE not defined!")


class ListType(Type):
    def __init__(self, name: str, nested: "Type", parent: Optional["Type"]=None):
        self.name = name
        self.nested = nested
        self.parent = parent

    def __le__(self, other):
        if not isinstance(other, ListType):
            return False

        return self.nested <= other.nested

    def __repr__(self):
        return self.name


class MapType(Type):
    def __init__(self, name: str, key: "Type", value: "Type"):
        self.name = name
        self.key = key
        self.value = value

    def __le__(self, other):
        if not isinstance(other, MapType):
            return False

        return self.key <= other.key and self.value <= other.value

    def __repr__(self):
        return self.name


class ClassType(Type):
    def __init__(self, name: str, parent: Optional["Type"]=None):
        self.name = name
        self.parent = parent

    def __le__(self, other):
        if self == other:
            return True

        if self.parent is None:
            return False

        return self.parent <= other

    def __repr__(self):
        return self.name


a = ClassType("a")
b = ClassType("b")
c = ClassType("c")
d = ClassType("d")

b.parent = a
c.parent = a
d.parent = a

lt = ListType("lt", c)
mt = MapType("mt", b, d)

problem = Problem()

problem.addVariable("t", [d, c, b, a])
problem.addVariable("b", [c, b, a])
problem.addVariable("x", [lt])
problem.addVariable("y", [mt])


problem.addConstraint(lambda t: t <= a, ("t"))
problem.addConstraint(lambda b: b <= a, ("b"))

problem.addConstraint(lambda x, t: x.nested <= t, ("x", "t"))

problem.addConstraint(lambda y, t: y.key <= t, ("y", "t"))
problem.addConstraint(lambda y, b: y.value <= b, ("y", "b"))

solution = problem.getSolutions()
print(solution)