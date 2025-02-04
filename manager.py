import subprocess
import os
import logging

# Setup logging
LOG_FILE = "C:\\Automation\\service_log.txt"

# Ensure the directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Ensure the log file exists; create it if it doesn't
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w'):  # Create an empty log file
        pass

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def start_service(service_name):
    """Start a Windows service and log the action."""
    try:
        result = subprocess.run(["sc", "start", service_name], capture_output=True, text=True, check=True)
        message = f"Service '{service_name}' started successfully."
        logging.info(message)
        return message
    except subprocess.CalledProcessError as e:
        error_message = f"Error starting service '{service_name}': {e.stderr} (Exit Code: {e.returncode})"
        logging.error(error_message)
        return error_message


if __name__ == "__main__":
    service_name = "Spooler"  # Change this to any Windows service you'd like to test.
    result = start_service(service_name)
    print(result)
