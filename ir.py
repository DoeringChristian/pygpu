from dataclasses import dataclass
from copy import copy
from enum import Enum


@dataclass
class Id:
    idx: int


@dataclass
class Add:
    lhs: Id
    rhs: Id
    dst: Id


@dataclass
class IAdd:
    dst: Id
    rhs: Id


@dataclass
class GetItem:
    src: Id
    dst: Id
    idx: Id


@dataclass
class Const:
    dst: Id
    val: float


@dataclass
class Arg:
    dst: Id


@dataclass
class Load:
    dst: Id
    set: int
    binding: int


@dataclass
class FnBegin:
    pass


@dataclass
class FnEnd:
    pass


@dataclass
class FnBody:
    pass


@dataclass
class FnCall:
    op: Id
    vars: list[Id]


class Ir:
    ops = []
    vars = []

    def alloc(self, type: type) -> Id:
        ret = Id(len(self.vars))
        self.vars.append(type)
        return ret

    def __repr__(self):
        rep = f"Ir({self.ops=}, {self.vars=})"
        return rep

    def type(self, id: Id) -> type:
        print(f"{self.vars[id.idx]}")
        return self.vars[id.idx]


ir = Ir()
