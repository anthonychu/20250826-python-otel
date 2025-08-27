import azure.functions as func
import logging
import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

RequestsInstrumentor().instrument()

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Make a call to http_trigger2
    response = requests.get('https://20250826-python-otel.azurewebsites.net/api/http_trigger2')
    logging.info(f'Response from http_trigger2: {response.status_code}')
    
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    

    

@app.route(route="http_trigger2")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")