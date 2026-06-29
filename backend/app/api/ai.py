from datetime import datetime

from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.services.insights_service import InsightsService


router = APIRouter()

service = InsightsService()

@router.get("/insights")
def get_insights(
    db: Session = Depends(get_db)
):

    now = datetime.now()

    month = now.month

    year = now.year

    previous_month = month - 1

    previous_year = year

    if previous_month == 0:

        previous_month = 12

        previous_year -= 1

    current_data = (

        service.get_month_summary(
            db,
            month,
            year
        )

    )

    previous_data = (

        service.get_month_summary(
            db,
            previous_month,
            previous_year
        )

    )

    return service.generate(
        current_data,
        previous_data
    )