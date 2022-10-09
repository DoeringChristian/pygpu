from ir import ir, VarType
from gen import Var, Fn, Int, Float, FloatArray, precomp
import glsl


@precomp
def test(x: Int):
    a = x + Int(10)
    pass


if __name__ == "__main__":
    arr = FloatArray([1., 2., 3.])
    x = arr[Int(0)]
    y = x + arr[Int(1)]
    y += arr[Int(2)]

    z = Var(type=VarType.FLOAT_ARRAY, set=0, binding=0)

    glsl.compile_to_glsl(ir)
