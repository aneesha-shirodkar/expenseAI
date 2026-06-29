from fastapi import FastAPI

from app.db.database import engine
from app.db.database import Base

from app.models.expense import Expense
from app.api.receipt import router as receipt_router
from app.api.ocr import router as ocr_router
from app.api.expense import router as expense_router
from fastapi.middleware.cors import CORSMiddleware 
from app.api.ai import router as ai_router
from app.api.chat import router as chat_router
from app.api.receipt_chat import router as receipt_chat_router
from app.api.gmail import router as gmail_router
from app.api.budget import router as budget_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

origins= [
      "http://localhost:5176",
    "http://127.0.0.1:5176",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows your React app to connect
    allow_credentials=True,
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],              # Allows all headers
)

app.include_router(
    receipt_router,
    prefix="/receipts",
    tags=["Receipts"]
)

app.include_router(
    ocr_router,
    prefix="/ocr",
    tags=["OCR"]
)

app.include_router(
    expense_router,
    prefix="/expenses",
    tags=["Expenses"]
)

app.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

app.include_router(
    receipt_chat_router,
     prefix="/receipt-chat",
    tags=["Receipt Chat"]
)
app.include_router(
    gmail_router,
    prefix="/gmail",
    tags=["Gmail"]
)

app.include_router(
    budget_router,
    prefix="/budgets",
    tags=["Budgets"]
)


@app.get("/")
def health():

    return {
        "message": "Expense AI Running"
    }