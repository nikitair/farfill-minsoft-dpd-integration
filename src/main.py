import os
from fastapi import FastAPI, Request
import uvicorn
from logs.logging_config import logger
from dotenv import load_dotenv
import json


load_dotenv()


app = FastAPI()

def save_to_backup(data):
    backup_file = "backup.json"
    with open(backup_file, "a") as f:
        json.dump(data, f)
        f.write("\n")

@app.get("/")
def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}

@app.get("/api/Order/{id}/Shipments")
def get_shipment(request: Request, id: int):
    shipments_data = request.json()
    save_to_backup(shipments_data)

@app.post("/api/Order/{id}/Shipments/CreateShipment")
def create_shipment(request: Request, id: int):
    pass

@app.post("/api/Order/{id}/Shipments/CancelShipment")
def cancel_shipment(request: Request, id: int):
    pass



if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
