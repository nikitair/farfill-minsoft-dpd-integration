from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, PositiveInt, Float, Decimal


class CreateShipmentRequest(BaseModel):
    AccountNo: str
    Password: str
    ShipmentId: str
    ServiceName: str
    ServiceCode: str
    DeliveryNotes: str
    Client: str
    Warehouse: str
    OrderNumber: str
    ExternalOrderReference: str
    Channel: str

    class ShipFrom(BaseModel):
        Email: EmailStr
        Phone: str
        Name: str
        AddressLine1: str
        AddressLine2: str | None = None
        AddressLine3: str | None = None

        Town: str
        County: str
        PostCode: str
        CountryCode: str
        VATNumber: str | None = None
        EORINumber: str | None = None
        IOSSNumber: str | None = None

    class ShipTo(BaseModel):
        Email: EmailStr
        Phone: str
        Name: str
        AddressLine1: str
        AddressLine2: str | None = None
        AddressLine3: str | None = None
        Town: str
        County: str
        PostCode: str
        CountryCode: str
        VATNumber: str | None = None
        EORINumber: str | None = None

    ShipFrom: ShipFrom
    ShipTo: ShipTo

    class Parcel(BaseModel):
        ParcelNo: PositiveInt
        UnitOfLength: str
        Length: Float
        Width: Float
        Height: Float
        UnitOfWeight: str
        Weight: Float

        class Cost(BaseModel):
            Currency: str
            Amount: Decimal

        Cost: Cost

        class ParcelItem(BaseModel):
            Title: str
            SKU: str
            Quantity: PositiveInt
            UnitWeight: Float

            class UnitPrice(BaseModel):
                Currency: str
                Amount: Decimal

            UnitPrice: UnitPrice
            CommodityCode: str
            CustomsDescription: str
            CountryOfManufacture: str

        Parcels: list[Parcel]

    Parcels: list[Parcel]



class CancelShipmentRequest(BaseModel):
    AccountNo: str
    Password: str
    TrackingNumber: str
    Comment: str | None = None
