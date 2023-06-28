from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username = Column(String(100), unique=True, nullable=False)
    is_admin = Column(Boolean)
    announcement = relationship('Announcement', cascade='delete')