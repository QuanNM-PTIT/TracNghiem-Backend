from typing import List
from pydantic import BaseModel
from models.answer_model import AnswerDetail


class Question(BaseModel):
    question_content: str


class QuestionDetail(BaseModel):
    question_content: str
    answers: List[AnswerDetail]
