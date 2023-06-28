from typing import Optional

from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str


class CommentDB(CommentCreate):
    id: int
    user_id: Optional[int]
    announcement_id: Optional[int]

    class Config:
        orm_mode = True
