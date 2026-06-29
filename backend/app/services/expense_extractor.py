import json
from app.core.config import settings
from app.schemas.expense import ExpenseExtraction
from app.services.foundry_service import create_client


SYSTEM_PROMPT = """
You are an expense extraction AI.

Extract:

merchant_name
merchant_address
amount
currency
expense_date
category
tax_amount
confidence

Rules:

1. Amount must be final paid amount.
2. Date format YYYY-MM-DD.
3. Confidence between 0 and 1.

Allowed categories:

Food
Fuel
Shopping
Groceries
Travel
Entertainment
Lifestyle
Utilities
Healthcare
Other
"""


class ExpenseExtractor:

    def __init__(self):
       self.client = create_client()

    def extract(
        self,
        receipt_text: str
    ) -> ExpenseExtraction:

        response = self.client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": receipt_text
                }
            ],
            temperature=0,
        )

        raw_json = response.choices[0].message.content
        parsed_dict = json.loads(raw_json)

        return ExpenseExtraction(**parsed_dict)