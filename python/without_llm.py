import traceback
import os

SCRIPT_NAME = "without_llm.py"

def buggy_function():
    return 1 / (1e-10)  # Fixed ZeroDivisionError  # Intentional error

def log_error(error_msg):
    """Log error messages into a file"""
    with open("error_log.txt", "a") as f:
        f.write(error_msg + "\n")

def analyze_and_fix():
    """Simple function to suggest a fix based on error log"""
    if "ZeroDivisionError" in open("error_log.txt").read():
        with open(SCRIPT_NAME, "r") as f:
            code = f.read()
        
        # Replace division by zero with a fallback value
        new_code = code.replace("1 / (1e-10)  # Fixed ZeroDivisionError", "1 / (1e-10)  # Fixed ZeroDivisionError")

        with open(SCRIPT_NAME, "w") as f:
            f.write(new_code)

        print("Script updated to fix ZeroDivisionError. Restarting...")
        os.system(f"python {SCRIPT_NAME}")  # Restart script

def main():
    try:
        buggy_function()
    except Exception as e:
        error_msg = traceback.format_exc()
        print("Error encountered. Logging and fixing...")
        log_error(error_msg)
        analyze_and_fix()

if __name__ == "__main__":
    main()
