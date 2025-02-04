import subprocess
import os
import logging
import azure.functions as func

# Setup logging
LOG_FILE = "C:\\Automation\\service_log.txt"

# Ensure the directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Ensure the log file exists; create it if it doesn't
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w'):  # Create an empty log file
        pass

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")


def check_service_status(service_name):
    """Check if a Windows service is running using PowerShell."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Get-Service -Name {service_name} | Select-Object -ExpandProperty Status"],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        return status
    except Exception as e:
        return f"ERROR: {str(e)}"


def start_service(service_name):
    """Start a Windows service using PowerShell if it is not already running."""
    status = check_service_status(service_name)

    if status == "Running":
        message = f"Service '{service_name}' is already running. No action needed."
        logging.info(message)
        return message

    try:
        subprocess.run(
            ["powershell", "-Command", f"Start-Service -Name {service_name}"],
            capture_output=True, text=True, check=True
        )
        message = f"Service '{service_name}' started successfully."
        logging.info(message)
        return message
    except subprocess.CalledProcessError as e:
        error_message = f"Error starting service '{service_name}': {e.stderr} (Exit Code: {e.returncode})"
        logging.error(error_message)
        return error_message


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function HTTP Trigger to Start a Windows Service."""
    service_name = req.params.get('service')
    
    if not service_name:
        try:
            req_body = req.get_json()
            service_name = req_body.get('service')
        except ValueError:
            pass

    if not service_name:
        return func.HttpResponse("Please provide a 'service' parameter in the query string or request body.", status_code=400)

    result = start_service(service_name)

    return func.HttpResponse(result, status_code=200)

