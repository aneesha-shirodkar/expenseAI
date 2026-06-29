import re

from sqlalchemy.orm import Session
from app.helper.chat_utils import extract_merchant_and_period
from app.services.expense_tools import (
    total_by_category,
    biggest_purchases,
    spending_by_merchant,
    compare_months
)


class ChatService:

    def chat(
        self,
        db: Session,
        message: str
    ):

        message = message.lower()

        # ------------------------
        # FOOD / CATEGORY
        # ------------------------

        categories = [
            "food",
            "fuel",
            "shopping",
            "groceries",
            "travel",
            "entertainment",
            "lifestyle",
            "utilities",
            "healthcare"
        ]

        for category in categories:

            if (
                category in message
                and "spend" in message
            ):

                total = total_by_category(
                    db,
                    category.title()
                )

                return {
                    "answer":
                    f"You spent ${total:.2f} on {category.title()}."
                }

        # ------------------------
        # BIGGEST PURCHASES
        # ------------------------

        if (
            "biggest" in message
            or "largest" in message
        ):

            expenses = biggest_purchases(db)

            text = "Your top 5 biggest purchases:\n\n"

            for expense in expenses:

                text += (
                    f"{expense['merchant']} "
                    f"- ${expense['amount']:.2f}\n"
                )

            return {
                "answer": text
            }

        # ------------------------
        # COSTCO / MERCHANT
        # ------------------------

        merchant, period = extract_merchant_and_period(message)

        if merchant:
            total = spending_by_merchant(db,merchant,period=period)
            period_text = f"for {period.replace('_', ' ')}" if period else ""
            return {
            "answer": f"You spent ${total:.2f} {period_text} at {merchant}. {period or 'all time'}"
            }

        # ------------------------
        # MONTH COMPARISON
        # ------------------------

        compare_match = re.search(

            r"compare (\w+) for (\w+) vs (\w+)",

            message

        )

        if compare_match:

            category = compare_match.group(1)

            month_1 = compare_match.group(2)

            month_2 = compare_match.group(3)

            result = compare_months(
                db,
                category.title(),
                month_1,
                month_2
            )

            return {
                "answer": result
            }

        # ------------------------
        # DEFAULT
        # ------------------------

        return {
            "answer":
            (
                "I can help with:\n"
                "- How much did I spend on Food?\n"
                "- Show my biggest purchases\n"
                "- How much did I spend at Costco?\n"
                "- Compare groceries for April vs May"
            )
        }