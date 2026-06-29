from pydantic import BaseModel
from datetime import date
from typing import Optional

# This is purely for OpenAI to look at and understand your JSON structure
class ExpenseExtraction(BaseModel):
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    expense_date: Optional[date] = None
    category: Optional[str] = None
    tax_amount: Optional[float] = None
    confidence: Optional[float] = None
