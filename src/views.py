import json
from logs.logging_config import logger
import requests


login_endpoint = "https://api.dpd.co.uk/user/?action=login"
login_headers = {
    "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(login_endpoint, headers=login_headers)
response.raise_for_status()  # Перевіряємо, чи немає помилки у відповіді

# Отримуємо значення geoSession з відповіді
login_data = response.json()["data"]
geo_session = login_data["geoSession"]



def create_shipment_view(payload):
    endpoint = "https://api.dpd.co.uk/shipping/network/"
    headers = {
        "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
        "Accept": "application/json",
        "GeoSession": geo_session,
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

    
    try:
        response = requests.get(endpoint, params=payload, headers=headers)
        response.raise_for_status() 
    except requests.RequestException as e:
        logger.error("send_dpd_request -- Error sending request to DPD API:", exc_info=True)
    return parsed_data






def cancel_shipment_view(data):
    ...