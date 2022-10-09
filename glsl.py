import ir
import gen


def glsl_const_assignment(const) -> str:
    match const:
        case float(const):
            return f" = {const}"
        case int(const):
            return f" = {const}"
        case list(consts):
            ret = f"[{len(consts)}] = " + "{"
            for const in consts:
                ret += f"{const}, "
            ret = ret[:-2]  # TODO: find better way to remove comma
            ret += "}"
            return ret
        case _:
            raise Exception(
                f"There is no glsl equivalent for this constant: {const=}")


def glsl_type(type: type) -> str:
    if type == gen.Float:
        return "float"
    elif type == gen.Int:
        return "int"
    elif type == gen.IntArray:
        return "int"
    elif type == gen.FloatArray:
        return "float"
    else:
        raise Exception(f"Type not supported {type=}")


def compile_to_glsl(src: ir.Ir) -> str:
    glsl = """
#version 450
    """

    for idx, op in enumerate(src.ops):
        print(f"{idx}: {op}")
        match op:
            case ir.FnBegin():
                glsl += "void fn" + f"{idx}" + "("
            case ir.FnBody():
                glsl = glsl[:-1]  # TODO: find better way to remove comma
                glsl += "){\n"
            case ir.FnEnd():
                glsl += "}\n"
            case ir.Arg(dst):
                glsl += glsl_type(ir.ir.type(dst)) + f" var{dst.idx},"
            case ir.Const(dst, val):
                glsl += glsl_type(ir.ir.type(dst)) + \
                    f" var{dst.idx}" + glsl_const_assignment(val) + ";\n"
            case ir.Add(lhs, rhs, dst):
                glsl += f"{glsl_type(ir.ir.type(dst))} var{dst.idx} = var{lhs.idx} + var{rhs.idx};\n"
            case ir.IAdd(dst, rhs):
                glsl += f"var{dst.idx} += var{rhs.idx};\n"
            case ir.GetItem(src, dst, idx):
                glsl += f"{glsl_type(ir.ir.type(dst))} var{dst.idx} = var{src.idx}[var{idx.idx}];\n"

    print(glsl)
