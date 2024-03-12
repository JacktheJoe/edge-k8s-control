
import subprocess
import re
import sys
from datetime import datetime

# Function to parse the date in the format used by Kubernetes 'Start Time' and the 'date' command output
def parse_date(date_str, is_kube_time=True):
    if is_kube_time:
        # Format for Kubernetes 'Start Time'
        try:
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            return datetime.strptime(date_str, '%a %d %b %Y %H:%M:%S %z')
    else:
        # Format for system 'date' command output
        return datetime.strptime(date_str, '%a %b %d %H:%M:%S %Z %Y')

# Check if the pod name is passed as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <pod-name>")
    sys.exit(1)

# Get the pod name from the command line argument
pod_name = sys.argv[1]

# Run the kubectl command
kubectl_command = f'kubectl describe pods -n kube-system {pod_name}'
process = subprocess.Popen(kubectl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = process.communicate()

# Initialize start_time
start_time = None

# Check for errors in kubectl command
if stderr:
    print(f"Error: {stderr.decode()}")
else:
    # Search for the start time in the command output
    start_time_line = re.search(r"^Start Time: .*", stdout.decode(), re.MULTILINE)
    if start_time_line:
        start_time_str = start_time_line.group(0).split(":", 1)[1].strip()
        start_time = parse_date(start_time_str)
        print(f"Pod Start Time: {start_time}")
    else:
        print("Start time not found")

# Only proceed if start_time is defined
if start_time:
    # Get the current system time
    date_command = 'date'
    process = subprocess.Popen(date_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    # Check for errors in date command
    if stderr:
        print(f"Error: {stderr.decode()}")
    else:
        # Extract the current system time
        current_time_str = stdout.decode().strip()
        current_time = parse_date(current_time_str, is_kube_time=False)
        print(f"Current System Time: {current_time}")

        # Calculate the time difference
        time_difference = current_time - start_time
        print(f"Time Difference: {time_difference}")