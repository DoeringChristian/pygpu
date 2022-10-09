import ir
import gen


def glsl_type(type: type) -> str:
    if type == gen.Float:
        return "float"
    elif type == gen.Int:
        return "int"
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
                glsl += "){\n"
            case ir.FnEnd():
                glsl += "}\n"
            case ir.Arg(dst, type):
                glsl += glsl_type(type) + f" var{dst.idx}, "
            case ir.Const(dst, val, type):
                pass

    print(glsl)
