from pydantic import BaseModel


class ReceiptQuestion(
    BaseModel):

    question: str