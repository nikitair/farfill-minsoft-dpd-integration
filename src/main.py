from fastapi import FastAPI, Request, HTTPException
import uvicorn
from logs.logging_config import logger
from utils import save_to_backup


app = FastAPI()


@app.get("/")
def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}


@app.get("/api/Order/{id}/Shipments")
def get_shipment(request: Request, id: int):
    logger.info(f"{get_shipment.__name__} -- GET SHIPMENT ENDPOINT TRIGGERED")
    shipments_data = request.json()
    # save_to_backup(shipments_data)


@app.post("/api/Order/{id}/Shipments/CreateShipment")
def create_shipment(request: Request, shipment_id: int):
    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    
    try:
        payload = request.get_json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})

    if payload:
        # call views her
       return payload



@app.delete("/api/Order/{id}/Shipments/CancelShipment")
def cancel_shipment(request: Request, id: int):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")
    pass



if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
