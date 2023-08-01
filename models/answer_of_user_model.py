from typing import List
from pydantic import BaseModel


class AnswerOfUser(BaseModel):
    attempt_id: str
    question_id: str
    answer: List[str]