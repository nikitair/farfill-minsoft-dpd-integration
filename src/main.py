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
@app.post("/api/test/Order/{id}/Shipments/CreateShipment")
async def create_shipment_test(request: Request, id: int):
    logger.info(f"{create_shipment_test.__name__} -- CREATE SHIPMENT TEST ENDPOINT TRIGGERED")
    return {
        "Success": True,
        "ErrorMessages": None,
        "Shipment": {
        "MainTrackingNumber": "TrackingNumber01",
        "LabelFormat": "PNG",
        "CustomsDocumentFormat": "PDF",
        "Packages": [
        {
        "TrackingNumber": "TrackingNumber01",
        "TrackingUrl": None,
        "ParcelNo": 1,
        "LabelAsBase64": "",
        "CustomsDocumentName": "",
        "CustomsPDFDocumentAsBase64": ""
        },
        {
        "TrackingNumber": "TrackingNumber02",
        "TrackingUrl": None,
        "ParcelNo": 3,
        "LabelAsBase64": "LabelAsBase64.....",
        "CustomsDocumentName": "CN22",
        "CustomsPDFDocumentAsBase64": "CustomsPDFDocumentAsBase64...."
        }
        ]
        }}


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
        
        shipment = response["Shipment"]
        main_tracking_number = shipment["MainTrackingNumber"]
        label_format = shipment["LabelFormat"]
        customs_document_format = shipment["CustomsDocumentFormat"]
        packages = shipment["Packages"]

        for package in packages:
            tracking_number = package["TrackingNumber"]
            tracking_url = package["TrackingUrl"]
            parcel_no = package["ParcelNo"]
            label_as_base64 = package["LabelAsBase64"]
            customs_document_name = package["CustomsDocumentName"]
            customs_pdf_document_as_base64 = package["CustomsPDFDocumentAsBase64"]
        return response


# @app.delete("/api/Order/{id}/Shipments/CancelShipment")
@app.delete("/api/mintsoft/test/CancelShipment")
async def cancel_shipment(request: Request, id: int):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")
    return {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }



if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
