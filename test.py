from ir import ir, VarType
from gen import Var, Fn, Int, Float, FloatArray
import glsl


def test(x: Int):
    pass


if __name__ == "__main__":
    arr = FloatArray([1., 2., 3.])
    x = arr[Int(0)]
    y = x + arr[Int(1)]
    y += arr[Int(2)]

    z = Var(type=VarType.FLOAT_ARRAY, set=0, binding=0)

    Fn(test)

    glsl.compile_to_glsl(ir)
