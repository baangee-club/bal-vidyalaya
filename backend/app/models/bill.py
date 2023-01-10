from .base import BaseModel, MongoModel, OID
from enum import Enum
from typing import Optional
import datetime


class Recurrence(str, Enum):
    ONE_TIME = "ONE_TIME"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    FORTNIGHTLY = "FORTNIGHTLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    HALF_YEARLY = "HALF_YEARLY"
    YEARLY = "YEARLY"
    AS_PRESENTED = "AS_PRESENTED"


class ComputationMethod(str, Enum):
    PERCENT = "PERCENT"
    VALUE = "VALUE"


class Exactness(str, Enum):
    ANY = "ANY"
    EXACT = "EXACT"
    EXACT_UP = "EXACT_UP"
    EXACT_DOWN = "EXACT_DOWN"
    RANGE = "RANGE"


class BillStatus(str, Enum):
    NOT_SUPPORTED = "NOT_SUPPORTED"
    NO_OUTSTANDING = "NO_OUTSTANDING"
    AVAILABLE = "AVAILABLE"


class Attribute(BaseModel):
    attributeName: str
    attributeValue: str


class BillFetchRequest(BaseModel):
    customerIdentifiers: list[Attribute]


class Aggregates(BaseModel):
    discount: Optional[dict]
    fee: Optional[dict]
    itemQuantity: Optional[dict]
    subTotal: Optional[dict]
    tax: Optional[dict]
    total: dict


class AmountRange(BaseModel):
    minimum: int
    maximum: int


class Amount(BaseModel):
    currencyCode: Optional[str]
    value: int


class Account(BaseModel):
    id: str
    ifsc: str
    name: Optional[str]


class SourceAccount(BaseModel):
    ifsc: str
    number: str


class CustomerAccount(BaseModel):
    additionalInfo: Optional[dict]
    id: str


class ValidationRules(BaseModel):
    amount: Optional[AmountRange]
    sourceAccounts: Optional[list[SourceAccount]]


class Computation(BaseModel):
    currencyCode: Optional[str]
    method: ComputationMethod
    value: str


class Discount(BaseModel):
    amount: Amount
    code: Optional[str]
    computation: Optional[list[Computation]]
    reason: Optional[str]


class TaxComponent(BaseModel):
    amount: Amount
    computation: Optional[list[Computation]]
    displayName: str
    type: Optional[str]


class Tax(BaseModel):
    amount: Amount
    components: list[TaxComponent]


class Fees(BaseModel):
    aggregates: Aggregates
    description: Optional[str]
    discounts: Optional[list[Discount]]
    displayName: str
    quantity: Optional[int]
    taxes: Optional[list[Tax]]
    unitCost: Optional[Amount]


class BillItem(BaseModel):
    aggregates: list[Aggregates]


class Split(BaseModel):
    unit: str
    value: int


class SettlementPart(BaseModel):
    account: Account
    remarks: Optional[str]
    split: Optional[Split]


class Settlement(BaseModel):
    parts: Optional[list[SettlementPart]]
    primaryAccount: Account


class Bill(BaseModel):
    additionalInfo: Optional[dict]
    aggregates: Aggregates
    amountExactness: Exactness
    billerBillID: str
    customerAccount: CustomerAccount
    discounts: Optional[list[Discount]]
    dueDate: Optional[datetime.datetime]
    fees: Optional[list[Fees]]
    generatedOn: datetime.datetime
    items: Optional[BillItem]
    platformFee: Fees
    recurrence: Recurrence
    settlement: Optional[Settlement]
    taxes: Optional[list[Tax]]
    transactionNote: Optional[str]
    validationRules: Optional[ValidationRules]

class BillInDB(MongoModel, Bill):
    id: OID


class BillDetails(BaseModel):
    billFetchStatus: BillStatus
    bills: list[Bill]


class Customer(BaseModel):
    additionalInfo: Optional[dict]
    name: str


class BillData(BaseModel):
    billDetails: BillDetails
    customer: Customer


class MyResponse(BaseModel):
    data: BillData
    status: int
    success: bool


class Receipt(BaseModel):
    date: datetime.datetime
    id: str

    


class ReceiptData(BaseModel):
    receipt: Receipt


class ReceiptRes(BaseModel):
    data: ReceiptData
    status: int
    success: bool


class PaymentDetails(BaseModel):
    additionalInfo: Optional[dict]
    amountPaid: Amount
    billAmount: Amount
    campaignID: Optional[str]
    instrument: Optional[str]
    transactionNote: Optional[str]
    uniquePaymentRefID: Optional[str]


class ReceiptReq(BaseModel):
    billerBillID: str
    paymentDetails: PaymentDetails
    platformBillID: str

class ReceiptInDB(MongoModel, ReceiptReq):
    id: OID
    date: Optional[datetime.datetime]
