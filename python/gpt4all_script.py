import os
from gpt4all import GPT4All

# Set the path to your GPT4All model
MODEL_NAME = "mistral-7b"  # Change this to the actual model you downloaded

# Function to fix broken code using GPT4All
def fix_code_locally(broken_code):
    # Load GPT4All model
    model = GPT4All(MODEL_NAME)

    # Create a prompt for GPT4All
    prompt = f"Fix the errors and optimize the following Python code:\n\n{broken_code}\n\nCorrected Code:"

    # Generate response
    fixed_code = model.generate(prompt)

    return fixed_code.strip()

# Example: Broken Python Code
broken_code = """
def greet(name)
    print("Hello, " + name)
    
greet("World"
"""

# Fix the code
fixed_code = fix_code_locally(broken_code)

# Save fixed code to a file
output_file = "fixed_script.py"
with open(output_file, "w") as f:
    f.write(fixed_code)

print(f"✅ Fixed code saved to {output_file}")
print("🔍 Preview of Fixed Code:\n")
print(fixed_code)
