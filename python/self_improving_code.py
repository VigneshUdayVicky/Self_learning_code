import os
import subprocess
import sys
import json
import traceback
from pathlib import Path
import time
import vscode  # Ensure this module is installed and properly configured

# CONFIGURATION
PACKAGE_NAME = "your_python_package"  # Replace with the actual package name
END_GOAL = "Run without errors in all environments"
VENV_DIR = "venvs"

# Step 1: Detect Installed Python Versions
def get_python_versions():
    versions = []
    for path in os.environ["PATH"].split(os.pathsep):
        python_path = Path(path) / "python"
        if python_path.exists():
            versions.append(str(python_path))
    return versions

# Step 2: Create Virtual Environments
def setup_envs(python_versions):
    os.makedirs(VENV_DIR, exist_ok=True)
    for py in python_versions:
        env_path = Path(VENV_DIR) / f"env_{Path(py).name}"
        subprocess.run([py, "-m", "venv", str(env_path)])
        print(f"✅ Created virtual environment: {env_path}")

def install_package(env_path):
    pip_path = env_path / "Scripts" / "pip" if sys.platform == "win32" else env_path / "bin" / "pip"
    subprocess.run([str(pip_path), "install", PACKAGE_NAME], capture_output=True)

# Step 3: Execute Package and Log Errors
def run_package(env_path, python_exec):
    py_exec = env_path / "Scripts" / "python" if sys.platform == "win32" else env_path / "bin" / "python"
    try:
        result = subprocess.run([str(py_exec), "-m", PACKAGE_NAME], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            raise RuntimeError(result.stderr)
    except Exception as e:
        error_log = f"Error in {python_exec}: {traceback.format_exc()}"
        with open("error_log.txt", "a") as log_file:
            log_file.write(error_log + "\n")
        print(f"❌ Error logged for {python_exec}")

# Step 4: Generate Debugging Questions
def generate_feedback_questions():
    if not Path("error_log.txt").exists():
        return []
    with open("error_log.txt", "r") as log_file:
        errors = log_file.readlines()
    questions = [
        f"What might have caused this error? {error.strip()}" for error in errors
    ]
    return questions

# Step 5: Send to VS Code Copilot
def send_to_copilot(questions):
    try:
        # Use the VS Code Copilot Chat API to send questions
        copilot_chat = vscode.commands.executeCommand("github.copilot-chat.ask", "\n".join(questions))
        print("💬 Sending to Copilot Chat:")
        print("🤖", copilot_chat)
        return copilot_chat
    except Exception as e:
        print(f"❌ Failed to send questions to Copilot Chat: {e}")
        return []

# Step 6: Apply Fixes
def apply_fixes(suggestions):
    print("🔧 Applying Fixes:")
    for fix in suggestions:
        try:
            with open(PACKAGE_NAME + ".py", "r+") as f:
                content = f.read()
                new_content = content + "\n# Copilot Fix: " + fix  # This is a placeholder for real patching
                f.seek(0)
                f.write(new_content)
            print(f"✅ Applied fix: {fix}")
        except FileNotFoundError:
            print(f"❌ File {PACKAGE_NAME}.py not found. Skipping fix.")

# Step 7: Main Loop - Repeat Until Goal is Met
def main():
    python_versions = get_python_versions()
    setup_envs(python_versions)
    
    for py in python_versions:
        env_path = Path(VENV_DIR) / f"env_{Path(py).name}"
        install_package(env_path)
        run_package(env_path, py)
    
    while True:
        questions = generate_feedback_questions()
        if not questions:
            print("🎉 End goal achieved! No errors found.")
            break
        suggestions = send_to_copilot(questions)
        apply_fixes(suggestions)
        time.sleep(5)  # Small delay to allow changes to be applied

if __name__ == "__main__":
    main()