from openai import AzureOpenAI

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.core.config import settings
from app.services.foundry_service import create_client


SYSTEM_PROMPT = """
You are a receipt analysis assistant.

Answer ONLY using the receipt text.

Rules:

1. Never invent items.

2. If information is unavailable, say:
"I cannot determine that from this receipt."

3. Use bullet points when listing products.

4. Keep responses concise.

Examples:

Question:
What did I buy?

Answer:
• Milk
• Eggs
• Bread

Question:
Did I buy dairy?

Answer:
Yes.
The receipt contains milk and cheese products.
"""


class ReceiptChatService:

    def __init__(self):

        self.client = create_client()

    def ask_question(
        self,
        db: Session,
        expense_id: int,
        question: str
    ):

        expense = (

            db.query(Expense)

            .filter(
                Expense.id == expense_id
            )

            .first()

        )

        if not expense:

            return {
                "answer":
                "Receipt not found."
            }

        prompt = f"""
Merchant:
{expense.merchant_name}

Date:
{expense.expense_date}

Amount:
{expense.amount}


Receipt Text:

{expense.raw_receipt_text}


Question:

{question}
"""

        response = (

            self.client.chat.completions.create(

                model=settings.azure_openai_deployment,

                temperature=0,

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )

        )

        return {

            "answer":

                response
                .choices[0]
                .message
                .content

        }