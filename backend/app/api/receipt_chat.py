from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
import uuid

from app.db.dependencies import get_db

from app.schemas.receipt_chat import (
    ReceiptQuestion
)

from app.services.receipt_chat_service import (
    ReceiptChatService
)


router = APIRouter()

service = ReceiptChatService()

@router.post("/{expense_id}")
def ask_receipt(
    expense_id: uuid.UUID,
    request: ReceiptQuestion,
    db: Session = Depends(get_db)
):

    return service.ask_question(db,expense_id,request.question)

