import base64
from io import BytesIO
import json
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from logs.logging_config import logger
from html2image import Html2Image
import img2pdf

login_endpoint = "https://api.dpd.co.uk/user/?action=login"
login_headers = {
    "Authorization": "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw==",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(login_endpoint, headers=login_headers)
response.raise_for_status()


geo_session = response.json()["data"]["geoSession"] 


def get_label(data):
    shipment_id = data['data']['shipmentId']
    label_endpoint = f"https://api.dpd.co.uk/shipping/shipment/{shipment_id}/label/"
    label_headers = {
        
        "Accept": "text/vnd.eltron-epl",
        "GeoSession": "f8a29d27-c2c6-4c11-afda-9177fcb22290",
        "GeoClient": "account/118990"
    }

    response = requests.get(label_endpoint, headers=label_headers)
    response_text = response.text


   
    return response_text


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
    if not payload.get("ShipmentId"):
        return {
        "Success": False,
        "ErrorMessages": ["Wrong payload"],
        "Shipment": {
            "MainTrackingNumber": None,
            "LabelFormat": "PNG",
            "CustomsDocumentFormat": "PDF",
            "Packages": []
        }
    }
        

#     payload = {
#     "AccountNo": "an",
#     "Password": "pw",
#     "ShipmentId": "260692",
#     "ServiceName": "Service 01",
#     "ServiceCode": "SC01",
#     "DeliveryNotes": "Please leave in a safe place",
#     "Client": "Mintsoft",
#     "Warehouse": "Main Warehouse",
#     "OrderNumber": "ON123456",
#     "ExternalOrderReference": "EXT123456",
#     "Channel": "Manual Input",
#     "ShipFrom": {
#         "Email": "shipper@mintsoft.co.uk",
#         "Phone": "01234 567890",
#         "Name": "firstname lastname",
#         "AddressLine1": "Mintsoft Ltd",
#         "AddressLine2": "Office 9, The Aquarium",
#         "AddressLine3": "101 Lower Anchor Street, Chelmsford",
#         "Town": "Essex",
#         "County": "Essex",
#         "PostCode": " TE1 1ST",
#         "CountryCode": "GB",
#         "VATNumber": "VATNo1234",
#         "EORINumber": "EORINo123",
#         "IOSSNumber": "IOSSNo"
#     },
#     "ShipTo": {
#         "Email": "consignee@delivery.co.uk",
#         "Phone": "07912345678",
#         "Name": "firstname lastname",
#         "AddressLine1": "27A The Nook",
#         "AddressLine2": None,
#         "AddressLine3": None,
#         "Town": "Whissendine",
#         "County": "Rutland",
#         "PostCode": "75000",
#         "CountryCode": "FR",
#         "VATNumber": "VATNo5678",
#         "EORINumber": "EORINo567"
#     },
#     "Parcels": [
#                 {
#                     "ParcelNo": 1,
#                     "UnitOfLength": "CM",
#                     "Length": 10.0,
#                     "Width": 10.0,
#                     "Height": 10.0,
#                     "UnitOfWeight": "kg",
#                     "Weight": 2.500,
#                     "Cost": {
#                         "Currency": "GBP",
#                         "Amount": 27.50
#                         },
#                     "ParcelItems": [
#                         {
#                             "Title": "SKU02-name",
#                             "SKU": "CC0002-002-M",
#                             "Quantity": 1,
#                             "UnitWeight": 0.45,
#                             "UnitPrice": {
#                                 "Currency": "GBP",
#                                 "Amount": 5.00
#                             },
#                             "CommodityCode": "61052010",
#                             "CustomsDescription": "Customs-SKU02",
#                             "CountryOfManufacture ": "UNITED KINGDOM"
#                         },
#                         {
#                             "Title": "SKU01-name",
#                             "SKU": "CC0003-003-M",
#                             "Quantity": 1,
#                             "UnitWeight": 0.45,
#                             "UnitPrice": {
#                                 "Currency": "GBP",
#                                 "Amount": 5.00
#                             },
#                             "CommodityCode": "61052010",
#                             "CustomsDescription": "Customs-SKU01",
#                             "CountryOfManufacture ": "UNITED KINGDOM"
#                         }
#                     ]
#                 },
#                 {
#                     "ParcelNo": 2,
#                     "UnitOfLength": "CM",
#                     "Length": 10.0,
#                     "Width": 10.0,
#                     "Height": 10.0,
#                     "UnitOfWeight": "kg",
#                     "Weight": 2.500,
#                     "Cost": {
#                         "Currency": "GBP",
#                         "Amount": 27.50
#                     },
#                     "ParcelItems": [
#                         {
#                             "Title": "SKU08-name",
#                             "Quantity": 1,
#                             "UnitWeight": 0.45,
#                             "UnitPrice": {
#                                 "Currency": "GBP",
#                                 "Amount": 5.00
#                             },
#                             "CommodityCode": "SKU08-name",
#                             "CustomsDescription": "Customs-SKU08",
#                             "CountryOfManufacture ": "UK"
#                         }
#                     ]
#                 }
#             ]
# }



    # account_no = payload["AccountNo"]
    # password = payload["Password"]
    # shipment_id = payload["ShipmentId"]
    # service_name = payload["ServiceName"]
    # service_code = payload["ServiceCode"]
    delivery_notes = payload["DeliveryNotes"]
    # client = payload["Client"]
    # warehouse = payload["Warehouse"]
    # order_number = payload["OrderNumber"]
    # external_order_reference = payload["ExternalOrderReference"]
    # channel = payload["Channel"]

    # ship_from_email = payload["ShipFrom"]["Email"]
    ship_from_phone = payload["ShipFrom"]["Phone"]
    ship_from_name = payload["ShipFrom"]["Name"]
    ship_from_address1 = payload["ShipFrom"]["AddressLine1"]
    ship_from_address2 = payload["ShipFrom"]["AddressLine2"]
    # ship_from_address3 = payload["ShipFrom"]["AddressLine3"]
    ship_from_town = payload["ShipFrom"]["Town"]
    ship_from_county = payload["ShipFrom"]["County"]
    ship_from_postcode = payload["ShipFrom"]["PostCode"]
    ship_from_country_code = payload["ShipFrom"]["CountryCode"]
    # ship_from_vat_number = payload["ShipFrom"]["VATNumber"]
    # ship_from_eori_number = payload["ShipFrom"]["EORINumber"]
    # ship_from_ioss_number = payload["ShipFrom"]["IOSSNumber"]

    ship_to_email = payload["ShipTo"]["Email"]
    ship_to_phone = payload["ShipTo"]["Phone"]
    ship_to_name = payload["ShipTo"]["Name"]
    ship_to_address1 = payload["ShipTo"]["AddressLine1"]
    ship_to_address2 = payload["ShipTo"]["AddressLine2"]
    # ship_to_address3 = payload["ShipTo"]["AddressLine3"]
    ship_to_town = payload["ShipTo"]["Town"]
    ship_to_county = payload["ShipTo"]["County"]
    ship_to_postcode = payload["ShipTo"]["PostCode"]
    ship_to_country_code = payload["ShipTo"]["CountryCode"]
    # ship_to_vat_number = payload["ShipTo"]["VATNumber"]
    # ship_to_eori_number = payload["ShipTo"]["EORINumber"]

    parcels_count = len(payload["Parcels"])
    parcels = payload["Parcels"]
    total_weight = sum(parcel["Weight"] for parcel in payload["Parcels"])
    current_time = datetime.datetime.now().isoformat()

    payload_dpd = {
    "jobId": None,
    "collectionOnDelivery": False,
    "collectionDate": current_time,#"2024-03-12T09:00:00"
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
                    "countryCode": "NL",
                    "postcode": "2988CK",
                    "street": "Rotterdam Distribution Center Schaapherderweg 24",
                    "locality": "Ridderkerk",
                    "town": "Rotterdam",
                    "county": "Netherlands"
                }
            },
            "networkCode": "1^19",
            "numberOfParcels": parcels_count,
            "totalWeight": total_weight,
            "shippingRef1": "shippingRef1",
            "shippingRef2": "shippingRef2",
            "shippingRef3": "shippingRef3",
            "customsValue": 15,
            "deliveryInstructions": delivery_notes,
            "parcelDescription": "GOODS",
            "liabilityValue": None,
            "liability": False,
            "preCleared": True
        }
    ]
}
    # payload_parses = payload_dpd["consignment"][0]["parcel"]

    url = "https://api.dpd.co.uk/shipping/shipment"
    params = {"test": "true"}
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "GeoClient": "account/118990",
    "GeoSession": geo_session
    }

    response = requests.post(url, json=payload_dpd, headers=headers)

    logger.info(response.status_code)
    logger.info(response.json())


    data = response.json()
    response_text = get_label(data)
    send_mintsoft = send_to_mintsoft(response_text)

    return send_mintsoft

def send_to_mintsoft(response_text):
    htmlimg = Html2Image()
    htmlimg.screenshot(html_str=response_text, save_as='label.png')


    image_path = 'label.png'
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
    except FileNotFoundError:
        print(f"Помилка: файл '{image_path}' не знайдено.")
        exit()


    LabelAsBase64 = base64.b64encode(img_data).decode('utf-8')


    pdf_path = 'label.pdf'
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(img2pdf.convert(img_data))


    with open(pdf_path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    CustomsPDFDocumentAsBase64 = base64.b64encode(pdf_data).decode('utf-8')



    dpd_to_mintsoft_response={
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
                "LabelAsBase64": LabelAsBase64,
                "CustomsDocumentName": "CN22",
                "CustomsPDFDocumentAsBase64": CustomsPDFDocumentAsBase64
                }
            ]
        }
    }
    return dpd_to_mintsoft_response


def cancel_shipment_view(data):
    # data = {
    #     "AccountNo": "an",
    #     "Password": "pw",
    #     "TrackingNumber": "TrackingNumber02",
    #     "Comment": None
    #     }
    
    user_name = data['AccountNo']
    password = data["Password"]
    shipment_id = data["TrackingNumber"]
    comment = data["Comment"]
    url = f"https://api.dpd.co.uk/shipping/shipment"
    headers = {
        "Content-type": "application/json; charset=utf-8"
    }
    body = {
    "userName": "farfill",
    "Password": "farfill@123",
    "TrackingNumber": "1127001855",
    "Comment": None
}
    response = requests.post(url, headers=headers, json=body)

    logger.info(f"{cancel_shipment_view.__name__} -- STATUS CODE - {response.status_code}")

    logger.error(f"{cancel_shipment_view.__name__} -- API ERROR - {response.text}")

    if response.status_code in (200, 201):
        logger.info(f"{cancel_shipment_view.__name__} -- DPD RESPONSE - {response.json()}")
        return response.json()
    else:
        return {  
            "Success": False,  
            "ErrorMessages": [ "Bad Request" ]  
            }  