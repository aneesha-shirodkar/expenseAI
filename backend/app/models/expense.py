import uuid
from datetime import date
from typing import Optional
from sqlalchemy import String, Text, Numeric, Date, Float, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    # Fully converted to modern 2.0 Mapped syntax
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    merchant_name: Mapped[Optional[str]] = mapped_column(String(255))
    merchant_address: Mapped[Optional[str]] = mapped_column(Text)
    amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    currency: Mapped[Optional[str]] = mapped_column(String(10))
    expense_date: Mapped[Optional[date]] = mapped_column(Date)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    tax_amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    receipt_url: Mapped[Optional[str]] = mapped_column(Text)
    raw_receipt_text: Mapped[Optional[str]] = mapped_column(Text)

class ExpenseExtraction(Base):
    __tablename__ = "expense_extractions"  # Added required tablename

    # Added required primary key column
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Fixed syntax: Optional goes INSIDE Mapped[...]
    merchant_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    merchant_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    expense_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tax_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
