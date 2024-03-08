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