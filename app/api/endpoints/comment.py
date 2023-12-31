from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_admin, current_user
from app.models.announcement import Announcement, Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentDB
from app.util.filter import filter_for_comment, parametr_filter_for_comment
from app.util.pagination import parameters_for_pagination
from app.util.sort import sort_query

router = APIRouter(tags=['Comment'])


@router.post(
    '/announcement/{announcement_id}/create-comment',
    response_model=CommentDB,
)
async def create_comment(
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
    announcement_id: int = Path(gte=1),
) -> Comment:
    obj_in_data = comment.dict()
    obj_in_data['user_id'] = user.id
    obj_in_data['announcement_id'] = announcement_id
    db_obj = Comment(**obj_in_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@router.get(
    '/announcement/{announcement_id}/list-comment',
    response_model=list[CommentDB],
    dependencies=[Depends(current_user)]
)
async def list_comment_for_concrete_announcement(
    pagination: Annotated[dict, Depends(parameters_for_pagination)],
    filter: Annotated[dict, Depends(parametr_filter_for_comment)],
    session: AsyncSession = Depends(get_async_session),
    announcement_id: int = Path(gte=1),
    sort: str = None,
) -> list[Comment]:
    query = (
        select(Comment).
        join(Announcement).
        where(Announcement.id == announcement_id).
        offset(pagination['skip']).
        limit(pagination['limit'])
    )
    query = filter_for_comment(query, filter, Comment)
    db_objs = await session.execute(query)
    query = db_objs.scalars().all()
    if sort:
        query = sort_query(sort, query)
    return query


@router.delete(
    '/delete-comment/{comment_id}',
    dependencies=[Depends(current_admin)],
    response_model=CommentDB,
)
async def delete_comment(
    comment_id: int = Path(gte=1),
    session: AsyncSession = Depends(get_async_session),
) -> Comment:
    ad = await session.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    ad = ad.scalars().first()
    await session.delete(ad)
    await session.commit()
    return ad
