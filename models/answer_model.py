from pydantic import BaseModel


class Answer(BaseModel):
    answer_content: str
    question_id: int
    is_correct: bool


class AnswerDetail(BaseModel):
    answer_content: str
    is_correct: bool
