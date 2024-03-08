from fastapi import FastAPI, Request, HTTPException
import uvicorn
from logs.logging_config import logger
from utils import save_to_backup
from views import create_shipment_view

app = FastAPI()


@app.get("/")
async def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}


# @app.get("/api/Order/{id}/Shipments")
@app.get("/farfill.xyz/api/mintsoft/test/CreateShipment")
async def get_shipment(request: Request, id: int):
    logger.info(f"{get_shipment.__name__} -- GET SHIPMENT ENDPOINT TRIGGERED")
    shipments_data = request.json()
    # save_to_backup(shipments_data)


@app.post("/api/Order/{id}/Shipments/CreateShipment")
async def create_shipment(request: Request, id: int):
    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED; id - {id}")

    payload = None
    
    try:
        payload = await request.json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py
        return response


# @app.delete("/api/Order/{id}/Shipments/CancelShipment")
@app.delete("/farfill.xyz/api/mintsoft/test/CreateShipment")
async def cancel_shipment(request: Request, id: int):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")
    pass



if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
