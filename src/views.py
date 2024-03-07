from logs.logging_config import logger
from main import create_shipment
import requests

def create_shipment_view(payload):
    endpoint = "https://api.dpd.co.uk/shipping/network/"
    headers = {
        "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
        "Accept": "application/json",
        "GeoSession": "a7edb4d4-16e1-4fa8-9741-bc72791722e0",
        "GeoClient": "account/118990"
    }

    try:
        response = requests.get(endpoint, params=payload, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        # Handle request exceptions
        logger.error("send_dpd_request -- Error sending request to DPD API:", exc_info=True)
        return None



def cancel_shipment_view(data):
    ...