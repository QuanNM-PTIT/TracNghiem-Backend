from pydantic import BaseModel


class TopicDetail(BaseModel):
    topic_id: str
    test_id: str