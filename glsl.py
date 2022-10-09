import ir


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
                pass
            case ir.Const(dst, val, type):
                pass

    print(glsl)
