from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.chat import ChatRequest

from app.services.chat_service import ChatService


router = APIRouter()

service = ChatService()

@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends( get_db)
):

    return service.chat(
        db,
        request.message
    )