from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_admin, current_user
from app.models.announcement import Announcement, Complaint
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintDB
from app.util.filter import filter_for_complaint, parametr_filter_for_complaint
from app.util.pagination import parameters_for_pagination
from app.util.sort import sort_query

router = APIRouter(tags=['Complaint'])


@router.post(
    '/announcement/{announcement_id}/create-complaint',
    response_model=ComplaintDB,
)
async def create_complaint(
    comment: ComplaintCreate,
    announcement_id: int = Path(gte=1),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    obj_in_data = comment.dict()
    obj_in_data['user_id'] = user.id
    obj_in_data['announcement_id'] = announcement_id
    db_obj = Complaint(**obj_in_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@router.get(
    '/announcement/{announcement_id}/list-complaint',
    response_model=list[ComplaintDB],
    dependencies=[Depends(current_admin)]
)
async def list_complaint_for_concrete_announcement(
    pagination: Annotated[dict, Depends(parameters_for_pagination)],
    filter: Annotated[dict, Depends(parametr_filter_for_complaint)],
    announcement_id: int = Path(gte=1),
    session: AsyncSession = Depends(get_async_session),
    sort: str = None,
):
    query = (
        select(Complaint).
        join(Announcement).
        where(Announcement.id == announcement_id).
        offset(pagination['skip']).
        limit(pagination['limit'])
    )
    query = filter_for_complaint(query, filter, Complaint)
    db_objs = await session.execute(query)
    query = db_objs.scalars().all()
    if sort:
        query = sort_query(sort, query)
    return query


@router.delete(
    '/delete-complaint/{complaint_id}',
    dependencies=[Depends(current_admin)]
)
async def delete_complaint(
    complaint_id: int = Path(gte=1),
    session: AsyncSession = Depends(get_async_session),
):
    complaint = await session.execute(
        select(Complaint).where(Complaint.id == complaint_id)
    )
    complaint = complaint.scalars().first()
    await session.delete(complaint)
    await session.commit()
    return complaint
