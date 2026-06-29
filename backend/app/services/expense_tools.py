from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from calendar import month_name
from datetime import datetime
from app.models.expense import Expense

def total_by_category(
    db: Session,
    category: str
):

    total = (

        db.query(
            func.sum(
                Expense.amount
            )
        )

        .filter(
            Expense.category == category
        )

        .scalar()

    )

    return float(total or 0)

def biggest_purchases(
    db: Session
):

    expenses = (

        db.query(Expense)

        .order_by(
            Expense.amount.desc()
        )

        .limit(5)

        .all()

    )

    return [

        {
            "merchant":
                e.merchant_name,

            "amount":
                float(e.amount)
        }

        for e in expenses
    ]

# def spending_by_merchant(
#     db: Session,
#     merchant: str
# ):

#     total = (

#         db.query(
#             func.sum(
#                 Expense.amount
#             )
#         )

#         .filter(
#             Expense.merchant_name
#             .ilike(
#                 f"%{merchant}%"
#             )
#         )

#         .scalar()

#     )

#     return float(total or 0)

def spending_by_merchant(
    db,
    merchant: str,
    period: str | None = None
):

    query = db.query(Expense).filter(
        Expense.merchant_name.ilike(
            f"%{merchant}%"
        )
    )

    now = datetime.now()

    if period == "this_month":

        query = query.filter(
            extract(
                "month",
                Expense.expense_date
            ) == now.month
        ).filter(
            extract(
                "year",
                Expense.expense_date
            ) == now.year
        )

    elif period == "last_month":

        month = now.month - 1
        year = now.year

        if month == 0:
            month = 12
            year -= 1

        query = query.filter(
            extract(
                "month",
                Expense.expense_date
            ) == month
        ).filter(
            extract(
                "year",
                Expense.expense_date
            ) == year
        )

    elif period == "this_year":

        query = query.filter(
            extract(
                "year",
                Expense.expense_date
            ) == now.year
        )

    total = sum(
        float(expense.amount)
        for expense in query.all()
    )

    return total

def compare_months(
    db,
    category,
    month_1,
    month_2
):

    month_lookup = {

        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12

    }

    m1 = month_lookup[
        month_1.lower()
    ]

    m2 = month_lookup[
        month_2.lower()
    ]

    total_1 = (

        db.query(
            func.sum(
                Expense.amount
            )
        )

        .filter(
            Expense.category == category
        )

        .filter(
            extract(
                "month",
                Expense.expense_date
            ) == m1
        )

        .scalar()

    ) or 0

    total_2 = (

        db.query(
            func.sum(
                Expense.amount
            )
        )

        .filter(
            Expense.category == category
        )

        .filter(
            extract(
                "month",
                Expense.expense_date
            ) == m2
        )

        .scalar()

    ) or 0

    difference = total_2 - total_1

    return (

        f"{category} spending was "
        f"${float(total_1):.2f} in {month_1.title()} "
        f"and ${float(total_2):.2f} in {month_2.title()}.\n"
        f"Difference: ${float(difference):.2f}"

    )