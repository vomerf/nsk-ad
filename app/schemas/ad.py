from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CategoryEnum(str, Enum):
    sale = 'sale'
    buy = 'buy'
    service = 'service'


class AdCreate(BaseModel):
    text: str
    category: CategoryEnum


class AdUpdate(BaseModel):
    category: CategoryEnum


class AdDB(AdCreate):
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True
