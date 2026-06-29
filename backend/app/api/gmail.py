# app/api/gmail.py

from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.services.gmail_service import GmailService


from app.db.dependencies import get_db

router = APIRouter()

service = GmailService()

@router.get("/connect")
def connect_gmail():
    return {    "url": service.get_auth_url()}

@router.get("/callback")
def google_callback(
    code: str
):

    service.exchange_code(code)

    return RedirectResponse(
        url="http://localhost:5176/"
    )

@router.post("/sync")
def sync_gmail(  db: Session = Depends(get_db)):
    return service.sync_receipts(
        db
    )


@router.get("/status")
def gmail_status():
    if not hasattr(service, "credentials"):
        return {
            "connected": False
        }

    return {
        "connected": True,
        "email": service.email,
        "last_sync":
            getattr(
                service,
                "last_sync",
                None
            ),

        "total_imported":
            getattr(
                service,
                "total_imported",
                0
            )
    }