from typing import Optional
from pydantic import BaseModel


class Attemp(BaseModel):
    test_id: str
    user_id: str
    answers: list
    score: int
    start_time: str
    time_remaining: Optional[int] = 0