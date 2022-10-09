from ir import ir, VarType
from gen import Var


if __name__ == "__main__":
    arr = Var([1., 2., 3.])
    x = arr[0]
    y = x + arr[1]
    print(f"{y=}")
    y += arr[2]

    z = Var(type=VarType.FLOAT_ARRAY, set=0, binding=0)

    print(f"{ir=}")
