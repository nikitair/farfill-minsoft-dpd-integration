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

    country_code = result["ShipTo"]["CountryCode"]
    post_code = result["ShipTo"]["PostCode"]



    url = "http://api.dpd.co.uk/shipping/network/"

    # Параметри запиту

    params = {
        "businessUnit": "0",
        "deliveryDirection": "1",
        "numberOfParcels": "1",
        "shipmentType": "0",
        "totalWeight": "1.0",
        "deliveryDetails.address.countryCode": country_code,
        "deliveryDetails.address.countryName": "",
        "deliveryDetails.address.locality": "",
        "deliveryDetails.address.organisation": "",
        "deliveryDetails.address.postcode": post_code,
        "deliveryDetails.address.property": "",
        "deliveryDetails.address.street": "",
        "deliveryDetails.address.town": "",
        "deliveryDetails.address.county": "",
        "collectionDetails.address.countryCode": country_code,
        "collectionDetails.address.countryName": "",
        "collectionDetails.address.locality": "",
        "collectionDetails.address.organisation": "",
        "collectionDetails.address.postcode": post_code,
        "collectionDetails.address.property": "",
        "collectionDetails.address.street": "",
        "collectionDetails.address.town": "",
        "collectionDetails.address.county": ""
    }       
    headers = {
    "Accept": "application/json",
    "GeoClient": "account/118990",
    "GeoSession": geo_session
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
    # try:
    #     response = requests.get(endpoint, params=payload, headers=headers)
    #     response.raise_for_status() 
    # except requests.RequestException as e:
    #     logger.error("send_dpd_request -- Error sending request to DPD API:", exc_info=True)






    return result


def cancel_shipment_view(data):
    ...