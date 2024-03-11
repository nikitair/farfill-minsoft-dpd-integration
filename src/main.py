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
@app.post("/api/test/Order/Shipments/CreateShipment")
async def create_shipment_test(request: Request):
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


@app.post("/api/Order/Shipments/CreateShipment")
async def create_shipment(request: Request):
    logger.info(f"{create_shipment.__name__} -- CREATE SHIPMENT ENDPOINT TRIGGERED")

    payload = None
    
    try:
        payload = await request.json()
        logger.info(f"{create_shipment.__name__} -- RECEIVED PAYLOAD - {payload}")
    except Exception:
        logger.exception(f"{create_shipment.__name__} -- ! BAD PAYLOAD ERROR")
        raise HTTPException(status_code=422, detail={"message": "Unprocessable Payload"})

    if payload:
        response = create_shipment_view(payload)  # Pass the payload to the function in view.py
        print(response)
        return response



@app.delete("/api/test/mintsoft/live/CancelShipment")
async def cancel_shipment_test(request: Request):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT TEST ENDPOINT TRIGGERED")
    return {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }



@app.delete("/api/mintsoft/live/CancelShipment")
async def cancel_shipment(request: Request):
    logger.info(f"{cancel_shipment.__name__} -- CANCEL SHIPMENT ENDPOINT TRIGGERED")
    return {
        "Success": True,
        "ErrorMessages": [ "Already Shipped", "Another message" ]
        }



if __name__ =="__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
    test_payload = {
    "AccountNo": "an",
    "Password": "pw",
    "ShipmentId": "260692",
    "ServiceName": "Service 01",
    "ServiceCode": "SC01",
    "DeliveryNotes": "Please leave in a safe place",
    "Client": "Mintsoft",
    "Warehouse": "Main Warehouse",
    "OrderNumber": "ON123456",
    "ExternalOrderReference": "EXT123456",
    "Channel": "Manual Input",
    "ShipFrom": {
        "Email": "shipper@mintsoft.co.uk",
        "Phone": "01234 567890",
        "Name": "firstname lastname",
        "AddressLine1": "Mintsoft Ltd",
        "AddressLine2": "Office 9, The Aquarium",
        "AddressLine3": "101 Lower Anchor Street, Chelmsford",
        "Town": "Essex",
        "County": "Essex",
        "PostCode": " TE1 1ST",
        "CountryCode": "GB",
        "VATNumber": "VATNo1234",
        "EORINumber": "EORINo123",
        "IOSSNumber": "IOSSNo"
    },
    "ShipTo": {
        "Email": "consignee@delivery.co.uk",
        "Phone": "07912345678",
        "Name": "firstname lastname",
        "AddressLine1": "27A The Nook",
        "AddressLine2": None,
        "AddressLine3": None,
        "Town": "Whissendine",
        "County": "Rutland",
        "PostCode": "TE1 1ST",
        "CountryCode": "UK",
        "VATNumber": "VATNo5678",
        "EORINumber": "EORINo567"
    },
    "Parcels": [
        {
            "ParcelNo": 1,
            "UnitOfLength": "CM",
            "Length": 10.0,
            "Width": 10.0,
            "Height": 10.0,
            "UnitOfWeight": "kg",
            "Weight": 2.500,
            "Cost": {
                "Currency": "GBP",
                "Amount": 27.50
            },
            "ParcelItems": [
                {
                    "Title": "SKU02-name",
                    "SKU": "SKU02",
                    "Quantity": 1,
                    "UnitWeight": 0.45,
                    "UnitPrice": {
                        "Currency": "GBP",
                        "Amount": 5.00
                    },
                    "CommodityCode": "CC-SKU02",
                    "CustomsDescription": "Customs-SKU02",
                    "CountryOfManufacture ": "UK"
                },
                {
                    "Title": "SKU01-name",
                    "SKU": "SKU01",
                    "Quantity": 1,
                    "UnitWeight": 0.45,
                    "UnitPrice": {
                        "Currency": "GBP",
                        "Amount": 5.00
                    },
                    "CommodityCode": "SKU01-name",
                    "CustomsDescription": "Customs-SKU01",
                    "CountryOfManufacture ": "UK"
                }
            ]
        },
        {
            "ParcelNo": 2,
            "UnitOfLength": "CM",
            "Length": 10.0,
            "Width": 10.0,
            "Height": 10.0,
            "UnitOfWeight": "kg",
            "Weight": 2.500,
            "Cost": {
                "Currency": "GBP",
                "Amount": 27.50
            },
            "ParcelItems": [
                {
                    "Title": "SKU08-name",
                    "Quantity": 1,
                    "UnitWeight": 0.45,
                    "UnitPrice": {
                        "Currency": "GBP",
                        "Amount": 5.00
                    },
                    "CommodityCode": "SKU08-name",
                    "CustomsDescription": "Customs-SKU08",
                    "CountryOfManufacture ": "UK"
                }
            ]
        }
    ]
}
    test_result = create_shipment_view(test_payload)
    print(test_result)
    