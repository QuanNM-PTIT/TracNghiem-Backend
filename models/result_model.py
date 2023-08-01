from pydantic import BaseModel


class Result(BaseModel):
    user_id: str
    test_id: str
    score: int
    total_correct: int
    total_time: int