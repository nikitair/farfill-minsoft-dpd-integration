import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Response
import uvicorn
from logs.logging_config import logger
# from utils import save_to_backup
# from schemas import CreateShipmentRequest, CancelShipmentRequest
from views import create_shipment_view

load_dotenv()
AUTH_TOKEN = os.getenv("X_API_KEY")

app = FastAPI()

# @app.on_event("startapp")
def startup_event():
    ...

# farfill.xyz/api/mintsoft
# farfill.xyz/api/mintsoft/CreateShipment
# farfill.xyz/api/mintsoft/CancelShipment


# farfill.xyz/api/mintsoft/test
# farfill.xyz/api/mintsoft/test/CreateShipment
# farfill.xyz/api/mintsoft/test/CancelShipment


@app.get("/api/mintsoft")
async def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}


@app.get("/api/mintsoft/test")
async def index_test():
    logger.info(f"{index.__name__} -- INDEX TEST ENDPOINT TRIGGERED")
    return {"message": "Hello Test!"}


# @app.get("/api/Order/{id}/Shipments")
@app.post("api/mintsoft/test/CreateShipment")
async def create_shipment_test(request: Request):
    logger.info(f"{create_shipment_test.__name__} -- CREATE SHIPMENT TEST ENDPOINT TRIGGERED")

    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response = Response(
            content=json.dumps({"Success": False, "ErrorMessages": "Unauthorized"}),
            status_code=401,
            media_type="application/json"
        )
        return response

    try:
        payload = await request.json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py

        return response


@app.post("/api/mintsoft/CreateShipment")
async def create_shipment(request: Request):
    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response = Response(
            content=json.dumps({"Success": False, "ErrorMessages": "Unauthorized"}),
            status_code=401,
            media_type="application/json"
        )
        return response

    try:
        payload = await request.json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py

        return response


@app.delete("/api/mintsoft/CancelShipment")
async def cancel_shipment_test(request: Request):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT TEST ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response = Response(
            content=json.dumps({"Success": False, "ErrorMessages": "Unauthorized"}),
            status_code=401,
            media_type="application/json"
        )
        return response
    
    try:
        payload = await request.json()
        logger.info(f"{cancel_shipment_test.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{cancel_shipment_test.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})
    

    return {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }


@app.delete("/api/mintsoft/test/CancelShipment")
async def cancel_shipment(request: Request):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    headers = request.headers

    token = headers.get("X-API-KEY")
    if token != AUTH_TOKEN:
        response = Response(
            content=json.dumps({"Success": False, "ErrorMessages": "Unauthorized"}),
            status_code=401,
            media_type="application/json"
        )
        return response
    
    try:
        payload = await request.json()
        logger.info(f"{cancel_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{cancel_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})
    

    return {
        "Success": True,
        "ErrorMessages": ["Already Shipped", "Another message"]
        }


if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")

    