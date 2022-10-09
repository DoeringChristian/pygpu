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
            ret += "};"
            return ret


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
        raise Exception("Type not supported")


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
            case ir.Arg(dst, type):
                glsl += glsl_type(type) + f" var{dst.idx},"
            case ir.Const(dst, val, type):
                glsl += glsl_type(type) + \
                    f" var{dst.idx}" + glsl_const_assignment(val) + "\n"
            case ir.Const(dst, val, type):
                pass

    print(glsl)
