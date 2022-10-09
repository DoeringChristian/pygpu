
from typing import overload, Callable, Optional
from ir import Id, Ir
from ir import *
import ir
from inspect import signature


class Var:
    id: Id

    @property
    def type(self) -> type:
        return ir.ir.vars[self.id.idx]

    @overload
    def __init__(self, const: int):
        pass

    @overload
    def __init__(self, const: float):
        pass

    def __init__(self, *args, **kwargs):
        match (args, kwargs):
            case ([], {'type': type, 'set': set, 'binding': binding}):
                self.id = ir.ir.alloc(type)
                ir.ir.ops.append(ir.Load(self.id, set, binding))
            case ([], {'type': type}):
                self.id = ir.ir.alloc(type)
            case ([const], {'type': type}):
                self.id = ir.ir.alloc(type)
                ir.ir.ops.append(ir.Const(self.id, const))
            case _:
                raise Exception("Error invallid arguments")

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

    def init_const(self, *args, **kwargs):
        match args:
            case [const]:
                ir.ir.ops.append(Const(self.id, const))
            case _:
                match kwargs:
                    case {'set': set, 'binding': binding}:
                        self.__init__(type=type)
                        ir.ops.append(Load(self.id, set, binding))
                raise Exception(
                    f"Could not construct variable of type: {type(self)} with arguments: {args=}, {kwargs=}")


class Int(Var):
    def __init__(self, *args, **kwargs):
        kwargs['type'] = Int
        Var.__init__(self, *args, **kwargs)


class Float(Var):
    def __init__(self, *args, **kwargs):
        kwargs['type'] = Float
        Var.__init__(self, *args, **kwargs)


class Array(Var):
    subtype: type

    def __init__(self, *args, **kwargs):
        Var.__init__(self, *args, **kwargs)

    def __getitem__(self, key) -> 'Var':
        dst = Var(type=self.subtype)
        ir.ir.ops.append(GetItem(self.id, dst.id, key.id))
        return dst


class FloatArray(Array):
    def __init__(self, *args, **kwargs):
        self.subtype = Float
        kwargs['type'] = FloatArray
        Array.__init__(self, *args, **kwargs)


class IntArray(Array):
    def __init__(self, *args, **kwargs):
        self.subtype = Int
        kwargs['type'] = IntArray
        Array.__init__(self, *args, **kwargs)


class Fn:
    args: list[type]
    op: Id
    ret: Optional[Id]

    def __init__(self, fn):
        self.op = ir.Id(len(ir.ir.ops))
        ir.ir.ops.append(ir.FnBegin())
        sig = signature(fn)
        args = []
        for name, param in sig.parameters.items():
            type = param.annotation
            args.append(Var(type=type))
            ir.ir.ops.append(ir.Arg(args[-1].id))

        ir.ir.ops.append(ir.FnBody())

        self.ret = fn(*args)

        ir.ir.ops.append(ir.FnEnd())

    def __call__(self, *args) -> Optional[Var]:
        ret = None
        id = None
        if self.ret is not None:
            ret = Var(type=self.ret.type)
            id = ret.id
        ir.ir.ops.append(
            ir.FnCall(self.op, [arg.id for arg in args], id))
        return ret


def precomp(fn: Callable) -> Callable:
    return Fn(fn)
