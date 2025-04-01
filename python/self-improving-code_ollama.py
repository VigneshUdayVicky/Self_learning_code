import subprocess
import json

def fix_code_locally(code):
    """Fixes code using a local LLM like Code Llama (via Ollama)."""
    prompt = f"Fix all errors in this Python script and return the corrected code:\n\n{code}"
    
    result = subprocess.run(["ollama", "run", "codellama:7b-code", prompt],
                            capture_output=True, text=True)
    
    return result.stdout.strip()

script_path = "C:\\Users\\UVY1COB\\Desktop\\self-improving-python\\broken_code.py"
with open(script_path, "r", encoding="utf-8") as file:
    broken_code = file.read()

fixed_code = fix_code_locally(broken_code)

with open(script_path, "w", encoding="utf-8") as file:
    file.write(fixed_code)

print("✅ Code fixed successfully!")