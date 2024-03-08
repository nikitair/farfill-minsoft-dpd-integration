from typing import Optional, List, Union

class CreateShipmentRequest:
    account_no: str
    password: str
    shipment_id: str
    service_name: str
    service_code: str
    delivery_notes: str
    client: str
    warehouse: str
    order_number: str
    external_order_reference: str
    channel: str

    class ShipFrom:
        email: str
        phone: str
        name: str
        address_line1: str
        address_line2: Optional[str] = None
        address_line3: Optional[str] = None
        town: str
        county: str
        post_code: str
        country_code: str
        vat_number: Optional[str] = None
        eorinumber: Optional[str] = None
        iossnumber: Optional[str] = None

    class ShipTo:
        email: str
        phone: str
        name: str
        address_line1: str
        address_line2: Optional[str] = None
        address_line3: Optional[str] = None
        town: str
        county: str
        post_code: str
        country_code: str
        vat_number: Optional[str] = None
        eorinumber: Optional[str] = None

    ship_from: ShipFrom
    ship_to: ShipTo

    class Parcel:
        parcel_no: int
        unit_of_length: str
        length: Union[int, float]  # Use Union for flexibility
        width: Union[int, float]
        height: Union[int, float]
        unit_of_weight: str
        weight: Union[int, float]

        class Cost:
            currency: str
            amount: str  # Assuming string for amount (modify if needed)

        cost: Cost

        class ParcelItem:
            title: str
            sku: str
            quantity: int
            unit_weight: Union[int, float]

            class UnitPrice:
                currency: str
                amount: str  # Assuming string for amount (modify if needed)

            unit_price: UnitPrice
            commodity_code: str
            customs_description: str
            country_of_manufacture: str

        parcels: List[Parcel]

    parcels: List[Parcel]


class CancelShipmentRequest:
    account_no: str
    password: str
    tracking_number: str
    comment: Optional[str] = None
