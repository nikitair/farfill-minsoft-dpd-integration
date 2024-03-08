import json
from logs.logging_config import logger
import requests


def create_shipment_view(payload):
    with open("data/auth_data.json", "r") as file:
        data = json.load(file)
    geosession = data["geosession"]
    auth_token = data["auth_token"]

    endpoint = "https://api.dpd.co.uk/shipping/network/"
    headers = {
        "Authorization": auth_token,
        "Accept": "application/json",
        "GeoSession": geosession,
        "GeoClient": "account/118990"
    }

    result = {
        "Success": False,
        "ErrorMessages": None,
        "Shipment": {
            "MainTrackingNumber": "",
            "LabelFormat": "PNG",
            "CustomsDocumentFormat": "PDF",
            "Packages": [
                {
                    "TrackingNumber": "",
                    "TrackingUrl": None,
                    "ParcelNo": 1,
                    "LabelAsBase64": "",
                    "CustomsDocumentName": "",
                    "CustomsPDFDocumentAsBase64": ""
                },
                {
                    "TrackingNumber": "",
                    "TrackingUrl": None,
                    "ParcelNo": 3,
                    "LabelAsBase64": "",
                    "CustomsDocumentName": "",
                    "CustomsPDFDocumentAsBase64": ""
                }
            ]
        }
    }

    parsed_data = json.loads(result)
    shipment = parsed_data["Shipment"]
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

    try:
        response = requests.get(endpoint, params=payload, headers=headers)
        response.raise_for_status() 
    except requests.RequestException as e:
        logger.error("send_dpd_request -- Error sending request to DPD API:", exc_info=True)
    return result


def cancel_shipment_view(data):
    ...
