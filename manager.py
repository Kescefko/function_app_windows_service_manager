import subprocess
import logging

# Setup logging
LOG_FILE = "C:\\Automation\\service_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def start_service(service_name):
    """Start a Windows service and log the action."""
    try:
        # Attempt to start the service using the 'sc' command
        result = subprocess.run(["sc", "start", service_name], capture_output=True, text=True, check=True)
        message = f"Service '{service_name}' started successfully."
        logging.info(message)
        return message
    except subprocess.CalledProcessError as e:
        error_message = f"Error starting service '{service_name}': {e.stderr}"
        logging.error(error_message)
        return error_message

if __name__ == "__main__":
    service_name = "Spooler"  # Change this to any Windows service you'd like to test.
    result = start_service(service_name)
    print(result)
