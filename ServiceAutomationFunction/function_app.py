import azure.functions as func
from manager import start_service
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="StartWindowsService", auth_level=func.AuthLevel.Anonymous)
def StartWindowsService(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the 'service' parameter from the query string or request body
    service_name = req.params.get('service')
    
    # If no 'service' parameter is found, try to get it from the request body
    if not service_name:
        try:
            req_body = req.get_json()
            service_name = req_body.get('service')
        except ValueError:
            pass

    # If no service name is provided, return an error response
    if not service_name:
        return func.HttpResponse("Please provide a 'service' parameter in the query string or request body.", status_code=400)

    # Call the start_service function to start the service
    result = start_service(service_name)

    # Return the result from start_service as the HTTP response
    return func.HttpResponse(result, status_code=200)