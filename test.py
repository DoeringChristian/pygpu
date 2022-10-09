from gen import Var, Fn, Int, Float, FloatArray, precomp
from ir import ir
import glsl

z = FloatArray(set=0, binding=0)


@precomp
def test(x: Int):
    arr = FloatArray([1., 2., 3.])
    x = arr[Int(0)]
    y = x + arr[Int(1)]
    y += arr[Int(2)]
    return y


if __name__ == "__main__":
    # print(f"{ir=}")

    x = Int(1)
    y = test(x)

    glsl.compile_to_glsl(ir)
