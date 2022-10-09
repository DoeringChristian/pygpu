from dataclasses import dataclass
from copy import copy
from enum import Enum


@dataclass
class Id:
    idx: int


class VarType(Enum):
    INT = 0
    FLOAT = 1
    FLOAT_ARRAY = 2
    INT_ARRAY = 3


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
class ConstFloat:
    dst: Id
    val: float


@dataclass
class ConstFloatArray:
    dst: Id
    val: []


@dataclass
class ConstInt:
    dst: Id
    val: int


@dataclass
class Load:
    dst: Id
    set: int
    binding: int


class Ir:
    ops = []
    types = []
    next: Id = Id(0)

    def alloc(self, type: VarType) -> Id:
        if not isinstance(type, VarType):
            raise Exception("Allocation needs var type")
        ret = Id(len(self.types))
        self.types.append(type)
        return ret

    def __repr__(self):
        rep = f"Ir({self.ops=}, {self.types=})"
        return rep


ir = Ir()
