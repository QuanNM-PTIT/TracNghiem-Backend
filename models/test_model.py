from pydantic import BaseModel


class Test(BaseModel):
    test_name: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    duration: int


class AddTest(BaseModel):
    test_name: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    duration: int
    topic_id: str
    selected_questions: list
