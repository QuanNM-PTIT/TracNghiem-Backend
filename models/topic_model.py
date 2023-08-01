from pydantic import BaseModel


class Topic(BaseModel):
    topic_name: str
    topic_image: str