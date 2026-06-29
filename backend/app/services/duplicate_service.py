from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.expense import Expense


class DuplicateService:

    def check_duplicate(
        self,
        db: Session,
        merchant_name: str,
        amount: float,
        expense_date
    ):

        expense = (

            db.query(Expense)

            .filter(
                Expense.merchant_name == merchant_name
            )

            .filter(
                Expense.amount == amount
            )

            .filter(
                Expense.expense_date == expense_date
            )

            .first()

        )

        return expense