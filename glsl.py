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


def glsl_load(dst: ir.Id, set, binding) -> str:
    type = ir.ir.type(dst)
    if type == gen.FloatArray:
        ret = f"layout(std430, set={set}, binding={binding}) buffer Buf{dst.idx}" + "{\n"
        ret += f"    {glsl_type(type)} var{dst.idx}[];\n"
        ret += "};\n\n"
        return ret

    pass


def compile_to_glsl(src: ir.Ir) -> str:
    glsl = """
#version 450
"""

    indentlvl = 0

    def indent() -> str:
        ret = ""
        for i in range(indentlvl):
            ret += "    "
        return ret

    for idx, op in enumerate(src.ops):
        print(f"{idx}: {op}")

        match op:
            case ir.FnBegin():
                glsl += indent()
                glsl += "void fn" + f"{idx}" + "("
            case ir.FnBody():
                glsl += indent()
                glsl = glsl[:-1]  # TODO: find better way to remove comma
                glsl += "){\n"
                indentlvl += 1
            case ir.FnEnd():
                glsl += "}\n"
                indentlvl -= 1
            case ir.Arg(dst):
                glsl += indent()
                glsl += glsl_type(ir.ir.type(dst)) + f" var{dst.idx},"
            case ir.Const(dst, val):
                glsl += indent()
                glsl += glsl_type(ir.ir.type(dst)) + \
                    f" var{dst.idx}" + glsl_const_assignment(val) + ";\n"
            case ir.Add(lhs, rhs, dst):
                glsl += indent()
                glsl += f"{glsl_type(ir.ir.type(dst))} var{dst.idx} = var{lhs.idx} + var{rhs.idx};\n"
            case ir.IAdd(dst, rhs):
                glsl += indent()
                glsl += f"var{dst.idx} += var{rhs.idx};\n"
            case ir.GetItem(src, dst, idx):
                glsl += indent()
                glsl += f"{glsl_type(ir.ir.type(dst))} var{dst.idx} = var{src.idx}[var{idx.idx}];\n"
            case ir.Load(dst, set, binding):
                glsl += indent()
                glsl += glsl_load(dst, set, binding)
            case ir.FnCall(op, vars):
                glsl += indent()
                glsl += f"fn{op.idx}("
                for var in vars:
                    glsl += f"var{var.idx}, "
                glsl = glsl[:-2]  # TODO: find better way to remove comma
                glsl += ");"

    print(glsl)
