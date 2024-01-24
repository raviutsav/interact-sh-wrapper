import subprocess

# Example: Capture text printed just after executing the program in terminal

# Command to run
command = "./interactsh-client"

# Run the command and capture the output
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=True)

# Capture the output immediately after execution
output = process.stdout.read()

# Print the captured output
print("Captured Output:")
print(output)

# Wait for the process to complete

# Get the return code
return_code = process.returncode
print("\nReturn Code:", return_code)
