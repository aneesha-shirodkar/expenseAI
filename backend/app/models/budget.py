from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric

from app.db.database import Base


class Budget(Base):

    __tablename__ = "budgets"

    id = Column(
        Integer,
        primary_key=True
    )

    category = Column(
        String,
        unique=True
    )

    monthly_limit = Column(
        Numeric(10, 2)
    )