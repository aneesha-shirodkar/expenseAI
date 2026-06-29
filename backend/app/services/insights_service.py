from datetime import datetime
from collections import defaultdict
import json

from sqlalchemy.orm import Session
from sqlalchemy import extract,func

from openai import AzureOpenAI

from app.models.expense import Expense
from app.core.config import settings
from app.services.foundry_service import create_client
from app.models.budget import Budget


SYSTEM_PROMPT = """
You are an AI financial assistant.

Generate exactly 3 insights.

Rules:

1. One sentence per insight.

2. Maximum 20 words.

3. No financial advice.

4. Focus on changes,
patterns,
increases,
decreases,
largest categories.

Return JSON:

{
    "insights": [
        "...",
        "...",
        "..."
    ]
}
"""
class InsightsService:

    def __init__(self):
        self.client = create_client()

    def get_month_summary(self, db: Session,month: int,year: int):

        expenses = (

            db.query(Expense)

            .filter(
                extract(
                    "month",
                    Expense.expense_date
                ) == month
            )

            .filter(
                extract(
                    "year",
                    Expense.expense_date
                ) == year
            )

            .all()

        )

        summary = defaultdict(float)

        for expense in expenses:

            summary[
                expense.category
            ] += float(
                expense.amount
            )

        return dict(summary)
    
    def generate(self,current_data,previous_data):
        user_prompt = f"""
        Current Month:{current_data}
        Previous Month:{previous_data}
        """

        response = (

            self.client.chat.completions.create(

                model=settings.azure_openai_deployment,

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ],

                response_format={
                    "type": "json_object"
                }

            )

        )

        content= response.choices[0].message.content
        return json.loads(content)
    
    def get_budget_insights(self,db: Session, month, year, now):
    
        budgets = db.query(Budget).all()
     
        results = []
        
        for b in budgets:
            
            spent_s= (
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.category == b.category)
            .filter(extract("month", Expense.expense_date) == month)
            .filter(extract("year", Expense.expense_date) == year)
            .scalar()
            )
            
            day_of_month = now.day if hasattr(now, 'day') else int(now)
            days_remaining = max(0, 30 - day_of_month) 
            
          
            spent = float(spent_s or 0)
            budget_limit = float(b.monthly_limit)

            prompt = f"""
                Budget Category: {b.category}
                Monthly Budget: {budget_limit}
                Spent so far: {spent}
                Days remaining in month: {days_remaining}

                Give a short, clear financial advice in 2-3 sentences.
                Focus on risk, overspending, and actionable suggestion.
                """
            print("PROMPT:", prompt)
            try:
                response = self.client.chat.completions.create(
                    model=settings.azure_openai_deployment,
                    messages=[
                        {
                        "role": "system",
                        "content": "You are a strict but helpful personal finance advisor."
                        },
                        {
                        "role": "user",
                        "content": prompt
                        }
                    ],
                    temperature=0.4
                )

                insight = response.choices[0].message.content
                

            except Exception as e:
                print(f"Error generating insight for category {b.category}: {e}")
                insight = "Insight temporarily unavailable."

            remaining = budget_limit - spent

            results.append({
                "category": b.category,
                "budget": b.monthly_limit,
                "spent": spent,
                "remaining": remaining,
                "insight": insight
            })
        return results