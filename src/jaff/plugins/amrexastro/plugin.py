import os

def main(network, path_template, path_build=None):
    from jaff.preprocessor import Preprocessor

    p = Preprocessor()

    ## Generate C++ code using header-only integrators (VODE)

    species = network.species
    charges = [sp.charge for sp in species]
    names = [sp.name for sp in species]

    e_index = names.index("e-")

    ch_ = []
    indices = []
    for i, ch in enumerate(charges):
        if ch >0:
            ch_.append("+")
            indices.append(i)
        elif ch < 0:
            ch_.append("-")
            indices.append(i)


    parts = []
    for idx, sign in zip(indices, ch_):
        if idx != e_index:
            mag = abs(charges[idx])    
            coeff = f"{float(mag)} * " if mag != 1 else ""
            base = f"{coeff}state.xn[{idx}]"
            if not parts:
                parts.append(f"-{base}" if sign == "-" else base)
            else:
                parts.append(f"- {base}" if sign == "-" else f"+ {base}")

    rhs = " ".join(parts) 
    charge_code = f"state.xn[{e_index}] = {rhs};"

    # Generate symbolic ODE and analytical Jacobian
    sode, jacobian = network.get_symbolic_ode_and_jacobian(idx_offset=0, use_cse=True, language="c++")

    import re

    def repl(match):
        i = int(match.group(1))
        return f"ydot({i+1})"

    def repl1(match):
        i = int(match.group(1))
        j = int(match.group(2))
        return f"jac({i+1},{j+1})"
    
    sode = re.sub(r"nden\[(\d+)\]", r"X(\1)", sode)
    sode = re.sub(r"\bcse(\d+)\b", r"x\1", sode)
    sode = re.sub(r"f\[(\d+)\]", repl, sode)
    sode = sode.replace("const double", "Real").replace("tgas", "T")

    jacobian = re.sub(r"nden\[(\d+)\]", r"X(\1)", jacobian)
    jacobian = re.sub(r"\bcse(\d+)\b", r"x\1", jacobian)
    jacobian = re.sub(r"J\((\d+)\s*,\s*(\d+)\)", repl1, jacobian)
    jacobian = jacobian.replace("const double", "Real").replace("tgas", "T")


    dEdt_code = network.get_dEdt(language="c++")

    dEdt_code = re.sub(r"nden\[(\d+)\]", r"X(\1)", dEdt_code)
    dEdt_code = re.sub(r"\bcse(\d+)\b", r"x\1", dEdt_code)
    dEdt_code = dEdt_code.replace("const double", "Real").replace("tgas", "T")


    # Generate temperature variable definitions for C++
    # These variables are commonly used in chemistry rate expressions
    temp_vars = """
Real T = state.T;
"""
    
    # Process all files with auto-detected comment styles
    p.preprocess(path_template,
                 ["actual_rhs.H", "actual_network_data.cpp"],
                 [{"TEMP_VARS": temp_vars, "ODE": sode, "DEDT": "return 0;", "JACOBIAN": jacobian}, 
                  {"CHARGE": charge_code}],
                 comment="auto",
                 path_build=path_build)
