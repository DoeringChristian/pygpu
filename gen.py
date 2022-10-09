
from typing import overload, Callable
from ir import Id, Ir, VarType
from ir import *
import ir
from inspect import signature


class Var:
    id: Id

    @property
    def type(self) -> VarType:
        return ir.ir.vars[self.id.idx]

    @overload
    def __init__(self, const: int):
        pass

    @overload
    def __init__(self, const: float):
        pass

    @overload
    def __init__(self, type: VarType, set: int, binding: int):
        pass

    def __init__(self, **kwargs):
        match kwargs:
            case {'type': type}:
                self.id = ir.ir.alloc(type)
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
            ir.ir.ops.append(IAdd(self.id, other.id))
            return self
        else:
            raise Exception("Should index with jit variables")
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
            ir.ir.ops.append(Add(self.id, other.id, dst.id))
            return dst
        else:
            raise Exception("Should index with jit variables")
            other = Var(other)
            return self + other

    @overload
    def __getitem__(self, key: int) -> 'Var':
        pass

    def __repr__(self):
        return f"Var({self.id=}, {self.type=})"


class Int(Var):
    def __init__(self, *args):
        Var.__init__(self, type=Int)
        match args:
            case [int(const)]:
                ir.ir.ops.append(Const(self.id, const, Int))
            case _:
                raise Exception("Could not construct int")


class Float(Var):
    def __init__(self, *args):
        Var.__init__(self, type=Float)
        match args:
            case [float(const)]:
                ir.ir.ops.append(Const(self.id, const, Float))
            case _:
                raise Exception("Could not construct int")


class Array(Var):
    subtype: type

    def __init__(self, **kwargs):
        self.subtype = kwargs['subtype']
        Var.__init__(self, type=kwargs['type'])

    def __getitem__(self, key) -> 'Var':
        dst = Var(type=self.subtype)
        ir.ir.ops.append(GetItem(self.id, dst.id, key.id))
        return dst


class FloatArray(Array):
    def __init__(self, *args):
        Array.__init__(self, type=FloatArray, subtype=Float)
        match args:
            case [list(const)]:  # TODO: Diffrent types of arrays
                ir.ir.ops.append(Const(self.id, const, FloatArray))
            case _:
                raise Exception("Could not construct int")


class IntArray(Array):
    def __init__(self, *args):
        Array.__init__(self, type=IntArray, subtype=Int)
        match args:
            case [list(const)]:  # TODO: Diffrent types of arrays
                ir.ir.ops.append(Const(self.id, const, FloatArray))
            case _:
                raise Exception("Could not construct int")


class Fn:
    args: list[type]
    op: Id

    def __init__(self, fn):
        self.op = ir.Id(len(ir.ir.ops))
        ir.ir.ops.append(ir.FnBegin(""))
        sig = signature(fn)
        args = []
        for name, param in sig.parameters.items():
            type = param.annotation
            args.append(Var(type=type))
            ir.ir.ops.append(ir.Arg(args[-1].id, type=type))

        fn(*args)

        ir.ir.ops.append(ir.FnEnd(""))

    def __call__(self, *args):
        ir.ir.ops.append(ir.FnCall(self.op, [arg.id for arg in args]))


def fn(name: str, f: Callable):
    ir.ir.ops.append(ir.FnBegin(name))
    f()
    ir.ir.ops.append(ir.FnEnd(name))
