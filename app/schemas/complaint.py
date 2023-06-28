from typing import Optional

from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    text: str


class ComplaintDB(ComplaintCreate):
    id: int
    user_id: Optional[int]
    announcement_id: Optional[int]

    class Config:
        orm_mode = True
