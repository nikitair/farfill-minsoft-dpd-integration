import os
from fastapi import FastAPI, Request
import uvicorn
from logs.logging_config import logger
from dotenv import load_dotenv


load_dotenv()


app = FastAPI()


@app.get("/")
def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"message": "Hello World!"}


@app.post("/api/Order/{id}/Shipments/CreateShipment")
def create_shipment(request: Request, id: int):
    pass


if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
