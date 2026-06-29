from fastapi import APIRouter,Depends, Query, HTTPException
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import extract, func

from app.db.dependencies import get_db
from app.models.expense import Expense

router = APIRouter()


@router.get("/")
def get_expenses(
    month: int | None = Query(None),
    year: int | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Expense)

    if month:
        query = query.filter(
            extract("month", Expense.expense_date) == month
        )

    if year:
        query = query.filter(
            extract("year", Expense.expense_date) == year
        )

    if category:
        query = query.filter(
            Expense.category == category
        )

    expenses = query.all()

    return expenses

@router.get("/summary")
def dashboard_summary(
    month: int | None = Query(None),
    year: int | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(
        Expense.category,
        func.sum(
            Expense.amount
        ).label("total")
    )

    if month:
        query = query.filter(
            extract("month", Expense.expense_date) == month
        )

    if year:
        query = query.filter(
            extract("year", Expense.expense_date) == year
        )

    if category:
        query = query.filter(
            Expense.category == category
        )

    results = (
        query
        .group_by(
            Expense.category
        )
        .all()
    )

    categories = {}

    total_spending = 0

    for category_name, amount in results:

        amount = float(amount) if amount is not None else 0.0

        categories[category_name] = amount

        total_spending += amount

    return {
        "total_spending": round(
            total_spending,
            2
        ),
        "categories": categories
    }


@router.get("/stats")
def dashboard_stats(
    month: int | None = Query(None),
    year: int | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Expense)

    if month:
        query = query.filter(
            extract("month", Expense.expense_date) == month
        )

    if year:
        query = query.filter(
            extract("year", Expense.expense_date) == year
        )

    if category:
        query = query.filter(
            Expense.category == category
        )

    expenses = query.all()

    total_expenses = len(expenses)

    total_spending = sum(
        float(e.amount) if e.amount is not None else 0.0
        for e in expenses
    )

    average_expense = (
        total_spending / total_expenses
        if total_expenses
        else 0
    )

    category_totals = {}

    for expense in expenses:

        category_totals[
            expense.category
        ] = (
            category_totals.get(
                expense.category,
                0
            )
            + float(expense.amount)if expense.amount is not None else 0.0
        )

    top_category = (
        max(
            category_totals,
            key=category_totals.get
        )
        if category_totals
        else None
    )

    return {
        "total_expenses": total_expenses,
        "total_spending": round(
            total_spending,
            2
        ),
        "average_expense": round(
            average_expense,
            2
        ),
        "top_category": top_category
    }

@router.get("/monthly-trend")
def monthly_trend(
    year: int,
    db: Session = Depends(get_db)
):

    results = (

        db.query(

            extract(
                "month",
                Expense.expense_date
            ).label("month"),

            func.sum(
                Expense.amount
            ).label("total")

        )

        .filter(
            extract(
                "year",
                Expense.expense_date
            ) == year
        )

        .group_by("month")

        .order_by("month")

        .all()
    )

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    return [

        {
            "month": month_names[int(month)],
            "amount": float(total)
        }

        for month, total in results

    ]

@router.get("/{expense_id}")
def get_expense(
    expense_id: uuid.UUID,
    db: Session = Depends(get_db)
):

    expense = (

        db.query(Expense)

        .filter(
            Expense.id == expense_id
        )

        .first()

    )

    if not expense:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense
