import base64
from io import BytesIO
import json
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


login_endpoint = "https://api.dpd.co.uk/user/?action=login"
login_headers = {
    "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(login_endpoint, headers=login_headers)
response.raise_for_status()


geo_session = response.json()["data"]["geoSession"] 




endpoint = "https://api.dpd.co.uk/shipping/network/"
headers = {
    "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
    "Accept": "application/json",
    "GeoSession": "f8a29d27-c2c6-4c11-afda-9177fcb22290",
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
    "PostCode": "75000",
    "CountryCode": "FR",
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
                        "SKU": "CC0002-002-M",
                        "Quantity": 1,
                        "UnitWeight": 0.45,
                        "UnitPrice": {
                            "Currency": "GBP",
                            "Amount": 5.00
                        },
                        "CommodityCode": "61052010",
                        "CustomsDescription": "Customs-SKU02",
                        "CountryOfManufacture ": "UNITED KINGDOM"
                    },
                    {
                        "Title": "SKU01-name",
                        "SKU": "CC0003-003-M",
                        "Quantity": 1,
                        "UnitWeight": 0.45,
                        "UnitPrice": {
                            "Currency": "GBP",
                            "Amount": 5.00
                        },
                        "CommodityCode": "61052010",
                        "CustomsDescription": "Customs-SKU01",
                        "CountryOfManufacture ": "UNITED KINGDOM"
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

# account_no = result["AccountNo"]
# password = result["Password"]
# shipment_id = result["ShipmentId"]
# service_name = result["ServiceName"]
# service_code = result["ServiceCode"]
# delivery_notes = result["DeliveryNotes"]
# client = result["Client"]
# warehouse = result["Warehouse"]
# order_number = result["OrderNumber"]
# external_order_reference = result["ExternalOrderReference"]
# channel = result["Channel"]

# ship_from_email = result["ShipFrom"]["Email"]
ship_from_phone = result["ShipFrom"]["Phone"]
ship_from_name = result["ShipFrom"]["Name"]
ship_from_address1 = result["ShipFrom"]["AddressLine1"]
ship_from_address2 = result["ShipFrom"]["AddressLine2"]
# ship_from_address3 = result["ShipFrom"]["AddressLine3"]
ship_from_town = result["ShipFrom"]["Town"]
ship_from_county = result["ShipFrom"]["County"]
ship_from_postcode = result["ShipFrom"]["PostCode"]
ship_from_country_code = result["ShipFrom"]["CountryCode"]
# ship_from_vat_number = result["ShipFrom"]["VATNumber"]
# ship_from_eori_number = result["ShipFrom"]["EORINumber"]
# ship_from_ioss_number = result["ShipFrom"]["IOSSNumber"]

ship_to_email = result["ShipTo"]["Email"]
ship_to_phone = result["ShipTo"]["Phone"]
ship_to_name = result["ShipTo"]["Name"]
ship_to_address1 = result["ShipTo"]["AddressLine1"]
ship_to_address2 = result["ShipTo"]["AddressLine2"]
# ship_to_address3 = result["ShipTo"]["AddressLine3"]
ship_to_town = result["ShipTo"]["Town"]
ship_to_county = result["ShipTo"]["County"]
ship_to_postcode = result["ShipTo"]["PostCode"]
ship_to_country_code = result["ShipTo"]["CountryCode"]
# ship_to_vat_number = result["ShipTo"]["VATNumber"]
# ship_to_eori_number = result["ShipTo"]["EORINumber"]

parcels_count = len(result["Parcels"])
parcels = result["Parcels"]
total_weight = sum(parcel["Weight"] for parcel in result["Parcels"])

payload = {
"jobId": None,
"collectionOnDelivery": False,
"collectionDate": "2024-03-12T09:00:00",
"consolidate": False,
"consignment": [
    {
        "consignmentNumber": None,
        "consignmentRef": None,
        "parcel": parcels,
        "collectionDetails": {
            "contactDetails": {
                "contactName": ship_from_name,
                "telephone": ship_from_phone
            },
            "address": {
                "organisation": "",
                "countryCode": ship_from_country_code,
                "postcode": ship_from_postcode,
                "street": ship_from_address1,
                "locality": ship_from_address2,
                "town": ship_from_town,
                "county": ship_from_county
            }
        },
        "deliveryDetails": {
            "contactDetails": {
                "contactName": ship_to_name,
                "telephone": ship_to_phone
            },
            "address": {
                "organisation": "",
                "countryCode": ship_to_country_code,
                "postcode": ship_to_postcode,
                "street": ship_to_address1,
                "locality": ship_to_address2,
                "town": ship_to_town,
                "county": ship_to_county
                },
            "notificationDetails": {
                "email": ship_to_email,
                "mobile": ship_to_phone
            }
        },
        "returnDetails": {
            "contactDetails": {
                "contactName": ship_to_name,
                "telephone": ship_to_phone,
                "email": ship_to_email,
            },
            "address": {
                "organisation": "",
                "countryCode": ship_to_country_code,
                "postcode": ship_to_postcode,
                "street": ship_to_address1,
                "locality": ship_to_address2,
                "town": ship_to_town,
                "county": ship_to_county
            }
        },
        "networkCode": "1^19",
        "numberOfParcels": parcels_count,
        "totalWeight": total_weight,
        "shippingRef1": "shippingRef1",
        "shippingRef2": "shippingRef2",
        "shippingRef3": "shippingRef3",
        "customsValue": 15,
        "deliveryInstructions": "Delivery Instructions",
        "parcelDescription": "Women’s Dress",
        "liabilityValue": None,
        "liability": False,
        "preCleared": True
    }
]
}
payload_parses = payload["consignment"][0]["parcel"]
print(payload_parses)
