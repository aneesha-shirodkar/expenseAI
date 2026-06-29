from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.document_intelligence import OCRService

router = APIRouter()

ocr_service = OCRService()


@router.post("/extract")

async def extract_receipt(
    file: UploadFile = File(...)
):

    content = await file.read()

    text = ocr_service.extract_text(
        content
    )

    return {
        "text": text
    }