import os
import json
from dotenv import load_dotenv
from datetime import timedelta
from celery import Celery
from fastapi import FastAPI, Request, HTTPException, Response
import uvicorn
from logs.logging_config import logger
from utils import backup_request
from views import create_shipment_view


load_dotenv()
AUTH_TOKEN = os.getenv("X_API_KEY")


app = FastAPI()
celery_app = Celery("tasks", broker="redis://localhost:6379/0")


celery_app.conf.beat_schedule = {
    "update-geosession-daily": {
        "task": "update_geosession",
        "schedule": timedelta(days=1),
    },
}

# farfill.xyz/api/mintsoft
# farfill.xyz/api/mintsoft/CreateShipment
# farfill.xyz/api/mintsoft/CancelShipment


# farfill.xyz/api/mintsoft/test
# farfill.xyz/api/mintsoft/test/CreateShipment
# farfill.xyz/api/mintsoft/test/CancelShipment


@app.get("/api/mintsoft")
async def index(request: Request):
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    response = {"message": "Hello World!"}

    await backup_request(request, response)
    return response


@app.get("/api/mintsoft/test")
async def index_test(request: Request):
    logger.info(f"{index.__name__} -- INDEX TEST ENDPOINT TRIGGERED")
    response = {"message": "Hello Test!"}

    await backup_request(request, response)
    return response


@app.post("/api/mintsoft/test/CreateShipment")
async def create_shipment_test(request: Request):
    logger.info(f"{create_shipment_test.__name__} -- CREATE SHIPMENT TEST ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response_data = {"Success": False, "ErrorMessages": "Unauthorized"}
        response = Response(
            content=json.dumps(response_data),
            status_code=401,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response

    try:
        payload = await request.json()
        logger.info(f"{create_shipment_test.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment_test.__name__} -- ! BAD PAYLOAD ERROR")
        response_data = {"Success": False, "ErrorMessages": "Bad Payload"}
        response = Response(
            content=json.dumps(response_data),
            status_code=422,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py

        await backup_request(request, response)

        return response


@app.post("/api/mintsoft/CreateShipment")
async def create_shipment(request: Request):
    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response_data = {"Success": False, "ErrorMessages": "Unauthorized"}
        response = Response(
            content=json.dumps(response_data),
            status_code=401,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response

    try:
        payload = await request.json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        response_data = {"Success": False, "ErrorMessages": "Bad Payload"}
        response = Response(
            content=json.dumps(response_data),
            status_code=422,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py

        await backup_request(request, response)

        return response



@app.delete("/api/mintsoft/test/CancelShipment")
async def cancel_shipment_test(request: Request):
    logger.info(f"{cancel_shipment_test.__name__} -- CANCEL SHIPMENT TEST ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response_data = {"Success": False, "ErrorMessages": "Unauthorized"}
        response = Response(
            content=json.dumps(response_data),
            status_code=401,
            media_type="application/json"
        )
        logger.warning(f"{cancel_shipment_test.__name__} -- ! UNAUTHORIZED REQUEST")

        await backup_request(request, response_data)

        return response
    
    try:
        payload = await request.json()
        logger.info(f"{cancel_shipment_test.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{cancel_shipment_test.__name__} -- ! BAD PAYLOAD ERROR")
        response_data = {"Success": False, "ErrorMessages": "Bad Payload"}
        response = Response(
            content=json.dumps(response_data),
            status_code=422,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response
    
    response = {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }

    await backup_request(request, response)
    return response


@app.delete("/api/mintsoft/CancelShipment")
async def cancel_shipment(request: Request):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response_data = {"Success": False, "ErrorMessages": "Unauthorized"}
        response = Response(
            content=json.dumps(response_data),
            status_code=401,
            media_type="application/json"
        )
        logger.warning(f"{cancel_shipment.__name__} -- ! UNAUTHORIZED REQUEST")

        await backup_request(request, response_data)

        return response
    
    try:
        payload = await request.json()
        logger.info(f"{cancel_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{cancel_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        response_data = {"Success": False, "ErrorMessages": "Bad Payload"}
        response = Response(
            content=json.dumps(response_data),
            status_code=422,
            media_type="application/json"
        )
        await backup_request(request, response_data)
        return response
    
    response = {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }

    await backup_request(request, response)
    return response


@app.get("/backups")
async def get_backups(request: Request):
    logger.info(f"{get_backups.__name__} -- GET BACKUPS ENDPOINT TRIGGERED")

    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response_data = {"Success": False, "ErrorMessages": "Unauthorized"}
        response = Response(
            content=json.dumps(response_data),
            status_code=401,
            media_type="application/json"
        )
        logger.warning(f"{get_backups.__name__} -- ! UNAUTHORIZED REQUEST")
        await backup_request(request, response_data)
        return response

    response = {
        "success": False,
        "data": []
        }

    try:
        with open("data/backups.json", "r") as f:
            response["data"] = json.load(f)
            response["success"] = True
    except Exception:
        logger.exception(f"{get_backups.__name__} -- !!! ERROR LOADING BACKUPS")

    return response


if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")


    