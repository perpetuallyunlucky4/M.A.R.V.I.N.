import math
import re

def run(command):
    pattern = r"\[MATH\](.*?)\[/MATH\]"
    calc_blocks = re.findall(pattern, command, re.DOTALL)
    
    if not calc_blocks:
        return []
    eqtns = []
    for expr in calc_blocks:
        expr = expr.strip()
        try:
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__") and callable(v)}
            constants = {
                "pi": math.pi,
                "e": math.e,
                "tau": math.tau,
                "inf": math.inf,
                "nan": math.nan
            }
            safe_globals = {"__builtins__": {}, **allowed_names, **constants}
            result = eval(expr, safe_globals, {})
            eqtns.append(f"{expr} = {result}")
        except Exception as e:
            eqtns.append(f"{expr}: {e}")
    return eqtns

print(run("[MATH] 3 * pi**2 [/MATH]  and [MATH]hello[/MATH]"))
