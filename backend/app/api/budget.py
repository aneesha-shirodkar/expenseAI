from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.db.dependencies import get_db
from app.models.budget import Budget
from app.schemas.budgets import BudgetCreate
from datetime import datetime
from app.models.expense import Expense
from app.services.insights_service import InsightsService


router = APIRouter()
service = InsightsService()

@router.post("/")
def create_budget(

    budget: BudgetCreate,

    db: Session = Depends(get_db)

):

    new_budget = Budget(

        category=budget.category,

        monthly_limit=budget.monthly_limit

    )

    db.add(new_budget)

    db.commit()

    db.refresh(new_budget)

    return new_budget


@router.get("/")
def get_budgets(

    db: Session = Depends(get_db)

):

    return db.query(
        Budget
    ).all()


@router.get("/insights")
def get_budget_insights(db: Session = Depends(get_db)):

    now = datetime.now()
    month = now.month
    year = now.year

    return service.get_budget_insights(db, month, year, now)