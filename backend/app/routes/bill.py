from fastapi import APIRouter, Depends, Body, HTTPException

from app.deps import check_auth
from app.dao.base import (
    get_student_repo,
    BaseRepository,
    get_bill_repo,
    get_receipt_repo,
)
from app.models.bill import (
    MyResponse,
    BillFetchRequest,
    ReceiptRes,
    ReceiptReq,
)
from app.models.base import StudentInDB
import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

bill = APIRouter(prefix="", dependencies=[Depends(check_auth)])


def get_month_ends(date):
    startOfCurrentMonth = datetime.datetime(
        date.year, date.month, 1, hour=0, minute=0, second=0
    )
    this_or_next_year = date.year if date.month < 12 else date.year + 1
    next_month = (date.month + 1) % 12
    endOfCurrentMonth = datetime.datetime(
        this_or_next_year, next_month, 1, hour=23, minute=59, second=59
    )
    endOfCurrentMonth = endOfCurrentMonth - datetime.timedelta(days=1)
    return startOfCurrentMonth, endOfCurrentMonth


@bill.post(
    "/fetch",
    response_model=MyResponse,
    dependencies=[Depends(check_auth)],
    response_model_exclude_none=True,
)
async def fetch(
    student_repo: BaseRepository = Depends(get_student_repo),
    bill_repo: BaseRepository = Depends(get_bill_repo),
    receipt_repo: BaseRepository = Depends(get_receipt_repo),
    bill_fetch: BillFetchRequest = Body(...),
):
    # error = HTTPException(400, detail="Incorrect Enrollment Number")
    enrollmentNumber = None
    for ci in bill_fetch.customerIdentifiers:
        if ci.attributeName == "EnrollmentNumber":
            enrollmentNumber = ci.attributeValue
    if not enrollmentNumber:
        raise HTTPException(400, detail="Enrollment Number not provided")

    student: StudentInDB = student_repo.get(enrollmentNumber)
    if not student:
        raise HTTPException(400, detail="Incorrect Enrollment Number")
    logger.info(f"Student: {str(student.dict())}")
    today = datetime.datetime.today()
    start, end = get_month_ends(today)
    logger.info(f"date range: {start.isoformat()} - {end.isoformat()}")
    bill = bill_repo.find_one(
        {
            "customerAccount": {"id": student.enrollmentNumber},
            # filter on generatedOn is not working fix this
            "generatedOn": {
                "$gte": start,
                "$lte": end,
            },
        }
    )
    logger.debug(f"bill for student {student}: {bill is not None}")
    if bill is None:
        logger.debug(f"creating bill for student {student}")
        bill = {
            "aggregates": {
                "total": {
                    "amount": {"value": student.fees},
                    "displayName": "School Fees",
                },
            },
            "amountExactness": "EXACT",
            "billerBillID": uuid.uuid4().hex,
            "customerAccount": {"id": student.enrollmentNumber},
            "generatedOn": datetime.datetime.now(),
            "platformFee": {
                "aggregates": {"total": {"value": 10000}},
                "displayName": "Platform Fee",
            },
            "recurrence": "MONTHLY",
        }
        inserted_id = bill_repo.insert_one(bill)
        bill = bill_repo.get(inserted_id)

    logger.debug(bill)
    logger.debug(bill.billerBillID)
    receipt = receipt_repo.find_one({"billerBillID": bill.billerBillID})
    logger.debug(receipt)
    if receipt:
        bill = None

    return {
        "data": {
            "billDetails": {
                "billFetchStatus": "AVAILABLE" if bill else "NO_OUTSTANDING",
                "bills": [bill] if bill else [],
            },
            "customer": {"name": student.name},
        },
        "status": 200,
        "success": True,
    }


@bill.post(
    "/fetchReceipt",
    response_model=ReceiptRes,
    dependencies=[Depends(check_auth)],
)
async def fetch_receipt(
    receipt_repo: BaseRepository = Depends(get_receipt_repo),
    receipt: ReceiptReq = Body(...),
):
    # receipt => billerBillID='1234' paymentDetails=PaymentDetails(additionalInfo=None, amountPaid=Amount(currencyCode='', value=50000), billAmount=Amount(currencyCode='INR', value=50000), campaignID='', instrument='UPI', transactionNote='', uniquePaymentRefID='32ff32f7-6c9d-4204-b631-341ad159273e') platformBillID='1048273469449438241'
    # just save this to
    _receipt = receipt_repo.find_one({"billerBillID": receipt.billerBillID})

    if not _receipt:
        receipt_dict = receipt.dict()
        receipt_dict["date"] = datetime.datetime.now()

        receipt_repo.insert_one(receipt_dict)
        _receipt = receipt_repo.find_one({"billerBillID": receipt.billerBillID})

    logger.debug(_receipt)

    receipt = {
        "date": _receipt.date,
        "id": str(_receipt.id),
    }
    return {
        "success": True,
        "status": 200,
        "data": {"receipt": receipt},
    }
