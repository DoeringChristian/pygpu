
from typing import overload
from ir import Id, Ir, ir, VarType
from ir import *


class Var:
    id: Id

    @property
    def type(self) -> VarType:
        return ir.types[self.id.idx]

    @overload
    def __init__(self, const: int):
        pass

    @overload
    def __init__(self, const: float):
        pass

    @overload
    def __init__(self, type: VarType, set: int, binding: int):
        pass

    def __init__(self, *args, **kwargs):
        print(f"{args=}")
        match args:
            case [int(const)]:
                self.__init__(type=VarType.INT)
                ir.ops.append(ConstInt(self.id, const))
            case [float(const)]:
                self.__init__(type=VarType.FLOAT)
                ir.ops.append(ConstFloat(self.id, const))
            case [list(const)]:  # TODO: Diffrent types of arrays
                self.__init__(type=VarType.FLOAT_ARRAY)
                ir.ops.append(ConstFloatArray(self.id, const))
            case _:
                match kwargs:
                    case {'type': type}:
                        self.id = ir.alloc(type)
                    case {'type': type, 'set': set, 'binding': binding}:
                        self.__init__(type=type)
                        ir.ops.append(Load(self.id, set, binding))
                    case _:
                        raise Exception("Error valid no argument provided")

    @overload
    def __iadd__(self, other: 'Var'):
        pass

    @overload
    def __iadd__(self, other: int):
        pass

    @overload
    def __iadd__(self, other: float):
        pass

    def __iadd__(self, other):
        if isinstance(other, Var):
            ir.ops.append(IAdd(self.id, other.id))
            return self
        else:
            self += Var(other)
            return self

    @overload
    def __add__(self, other: 'Var'):
        pass

    @overload
    def __add__(self, other: int):
        pass

    @overload
    def __add__(self, other: float):
        pass

    def __add__(self, other):
        if isinstance(other, Var):
            dst = Var(type=self.type)
            ir.ops.append(Add(self.id, other.id, dst.id))
            return dst
        else:
            other = Var(other)
            return self + other

    @overload
    def __getitem__(self, key: int) -> 'Var':
        pass

    def __getitem__(self, key) -> 'Var':
        print(f"{key=}")
        if isinstance(key, Var) and key.type == VarType.INT:
            match self.type:
                case VarType.FLOAT_ARRAY:
                    dst = Var(type=VarType.FLOAT)
                    ir.ops.append(GetItem(self.id, dst.id, key.id))
                    return dst
                case VarType.INT_ARRAY:
                    dst = Var(type=VarType.INT)
                    ir.ops.append(GetItem(self.id, dst.id, key.id))
                    return dst
                case _:
                    raise Exception("This type is not indexable")
        elif isinstance(key, int):
            return self[Var(key)]
        else:
            raise Exception("An Array cannot be indexed with this type")

    def __repr__(self):
        return f"Var({self.id=}, {self.type=})"
