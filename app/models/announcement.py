
import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Announcement(Base):

    class Category(str, enum.Enum):
        SERVICE = 'service'
        BUY = 'buy'
        SALE = 'sale'

    text = Column(Text, nullable=False)
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_announcement_user_id_user')
    )
    category = Column(
        Enum(Category), nullable=False,
    )
    comments = relationship(
        'Comment', cascade='delete', backref='announcement'
    )
    complaints = relationship(
        'Complaint', cascade='delete', backref='announcement'
    )


class Comment(Base):
    text = Column(String(500), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_comment_user_id_user'), nullable=False
    )
    announcement_id = Column(
        Integer,
        ForeignKey(
            'announcement.id',
            name='fk_comment_announcement_id_announcement'
        ),
        nullable=False
    )


class Complaint(Base):
    text = Column(String(1000), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_complaint_user_id_user'), nullable=False
    )
    announcement_id = Column(
        Integer,
        ForeignKey(
            'announcement.id',
            name='fk_complaint_announcement_id_announcement'
        ),
        nullable=False
    )
