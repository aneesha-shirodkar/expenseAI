from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from app.models.expense import Expense
from app.schemas.expense import ExpenseExtraction as ExpenseSchema
from app.models.expense import Expense as ExpenseModel
from app.services.document_intelligence import OCRService
from app.services.expense_extractor import ExpenseExtractor
from app.db.database import get_db
from app.helper.compression import prepare_file_for_ocr
from app.services.duplicate_service import DuplicateService

router = APIRouter()


ocr_service = OCRService()
expense_extractor = ExpenseExtractor()
duplicate_service = DuplicateService()

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir( exist_ok=True)


@router.post("/upload")
async def upload_receipt(
    file: UploadFile = File(...)
):

    extension = file.filename.split(".")[-1]

    filename = (
        f"{uuid4()}.{extension}"
    )

    filepath = (
        UPLOAD_DIR / filename
    )

    content = await file.read()

    with open(
        filepath,
        "wb"
    ) as f:
        f.write(content)

    return {
        "message": "Uploaded",
        "filename": filename
    }

@router.post("/process")
async def process_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1]

    filename = f"{uuid4()}.{extension}"

    filepath = UPLOAD_DIR / filename

    file_content = await file.read()

    file_content = prepare_file_for_ocr(
    file_bytes=file_content,
    content_type=file.content_type
)

    with open(filepath, "wb") as f:
        f.write(file_content)

    # OCR

    receipt_text = ocr_service.extract_text(
        file_content
    )

    # GPT Extraction

    expense_data: ExpenseSchema = expense_extractor.extract(
        receipt_text
    )

    #check duplicate
    duplicate = duplicate_service.check_duplicate(

    db=db,

    merchant_name= expense_data.merchant_name,

    amount= expense_data.amount,

    expense_date=expense_data.expense_date

    )

    if duplicate:
        return{
             "id": str(duplicate.id),
        "merchant_name": duplicate.merchant_name,
        "amount": float(duplicate.amount),
        "currency": duplicate.currency,
        "expense_date": duplicate.expense_date,
        "category": duplicate.category,
        "confidence": duplicate.confidence,
        "duplicate" : True
        }

    # Save

    expense = ExpenseModel(
        merchant_name=expense_data.merchant_name,
        merchant_address=expense_data.merchant_address,
        amount=expense_data.amount,
        currency=expense_data.currency,
        expense_date=expense_data.expense_date,
        category=expense_data.category,
        tax_amount=expense_data.tax_amount,
        confidence=expense_data.confidence,
        receipt_url=f"uploads/{file.filename}",
        raw_receipt_text=receipt_text
    )

    db.add(expense)

    db.commit()

    db.refresh(expense)

    return {
        "id": str(expense.id),
        "merchant_name": expense.merchant_name,
        "amount": float(expense.amount),
        "currency": expense.currency,
        "expense_date": expense.expense_date,
        "category": expense.category,
        "confidence": expense.confidence,
        "duplicate": False
    }