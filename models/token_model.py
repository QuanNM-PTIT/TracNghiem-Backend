from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: str | None = None
    email: str | None = None
    role: str | None = None