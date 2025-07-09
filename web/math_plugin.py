import math
import re
from plugins.plugin_base import Plugin

class mathPlugin(Plugin):
    def can_handle(self, message: str) -> bool:
        return "[MATH]" in message and "[/MATH]" in message
    
    def handle(self, message: str) -> list[str]:
        message = message.replace("^", "**")
        pattern = r"\[MATH\](.*?)\[/MATH\]"
        calc_blocks = re.findall(pattern, message, re.DOTALL)
    
        results = []
    
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__") and callable(v)}
        constants = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "inf": math.inf,
        "nan": math.nan
            }
        safe_globals = {"__builtins__": {}, **allowed_names, **constants}
    
        for expr in calc_blocks:
            expr = expr.strip()
            try:
                result = eval(expr, safe_globals, {})
                results.append(f"{expr} = {result}")
            except Exception as e:
                results.append(f"{expr}: {e}")
        return results
