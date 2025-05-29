import re
import subprocess

def run(command, gen_code_path):
    pattern = r"\[WRITE_PY\](.*?)\[/WRITE_PY\]"
    code_blocks = re.findall(pattern, command, re.DOTALL)
    result = []
    if not code_blocks:
        print("no blocks found")
        return result
    
    for i, block in enumerate(code_blocks):
        block = block.strip()
        print(f"code block number {i + 1}: \n{block}\n")
        confirm = input("do you want to run the code? (Y/n):").strip().lower()
                
        if confirm != "y":
            continue
        with open(gen_code_path, "w") as file:
            file.write(block)
                
        print(f"running {gen_code_path}...\n")
                
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

print(run("[WRITE_PY] \nprint('hello world!')\nprint('wassup')[/WRITE_PY] and [WRITE_PY] hi [/WRITE_PY]", "/home/pi/marvin/marvin_code.py"))
