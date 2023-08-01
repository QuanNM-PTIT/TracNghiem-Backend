from typing import List
from pydantic import BaseModel


class TestDetail(BaseModel):
    test_id: str
    question_ids: List[str]