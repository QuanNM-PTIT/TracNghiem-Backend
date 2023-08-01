from pydantic import BaseModel


class PermissionBase(BaseModel):
    test_id: str
    user_id: str