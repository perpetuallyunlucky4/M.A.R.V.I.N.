import re
import subprocess
from plugins.plugin_base import Plugin

class pythonPlugin(Plugin):
    def can_handle(self, message: str) -> str:
        return "[WRITE_PY]" in message and "[/WRITE_PY]" in message
    
    def handle(self, message: str, gen_code_path="/home/pi/marvin/marvin_code.py") -> list[str]:
        pattern = r"\[WRITE_PY\](.*?)\[/WRITE_PY\]"
        code_blocks = re.findall(pattern, message, re.DOTALL)
        result = []

        for i, block in enumerate(code_blocks):
            block = block.strip()
            print(f"\033[38;2;255;60;60mcode block number {i + 1}: \n{block}\n\033[0m")
            confirm = input("\033[38;2;255;60;60mdo you want to run the code? (Y/n):\033[0m").strip().lower()
                
            if confirm != "y":
                continue
            
            with open(gen_code_path, "w") as file:
                file.write(block)
                
            print(f"\033[38;2;255;60;60mrunning {gen_code_path}...\n\033[0m")
                
            try:
                output = subprocess.run(
                    ["python3", gen_code_path],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                result.append(f"output[{i}]:\n{output.stdout.strip()}")
                if output.stderr:
                    result.append(f"errors[{i}]:\n{output.stderr.strip()}")
            except subprocess.TimeoutExpired:
                result.append(f"error[{i}]: code timed out")
            except Exception as e:
                result.append(f"execution failed[{i}]:\n{e}")
    
        return result

