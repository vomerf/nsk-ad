from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models.announcement import Announcement
from app.models.user import User
from app.schemas.ad import AdCreate, AdDB, AdUpdate
from app.util.filter import filter_for_ad, parametr_filter_for_ad
from app.util.pagination import parameters_for_pagination
from app.util.sort import sort_query
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=['Announcement'])


@router.post(
    '/create-ad',
    response_model=AdDB,
)
async def create_ad(
    ad: AdCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    obj_in_data = ad.dict()
    if user is not None:
        obj_in_data['user_id'] = user.id
    db_obj = Announcement(**obj_in_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@router.get(
    '/list-ad',
    response_model=list[AdDB],
    dependencies=[Depends(current_user)]
)
async def list_ad(
    pagination: Annotated[dict, Depends(parameters_for_pagination)],
    filter: Annotated[dict, Depends(parametr_filter_for_ad)],
    session: AsyncSession = Depends(get_async_session),
    sort: str = None,
):
    query = (
        select(Announcement).
        offset(pagination['skip']).
        limit(pagination['limit'])
    )
    query = filter_for_ad(query, filter, Announcement)
    try:
        db_objs = await session.execute(query)
    except DBAPIError:
        raise HTTPException(
            status_code=400,
            detail='Проверьте правильность ввода категории'
        )
    query = db_objs.scalars().all()
    if sort:
        query = sort_query(sort, query)
    return query


@router.get('/detail-ad/{ad_id}',  dependencies=[Depends(current_user)])
async def detail_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    ad = await session.execute(
        select(Announcement).where(Announcement.id == ad_id)
    )
    ad = ad.scalars().first()
    return ad


@router.delete('/delete-ad/{ad_id}')
async def delete_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    ad = await session.execute(
        select(Announcement).
        where(Announcement.id == ad_id, Announcement.user_id == user.id)
    )
    ad = ad.scalars().first()
    if ad is None:
        raise HTTPException(
            status_code=404,
            detail=('Вы пытаетесь удалить не своё объявление,'
                    'либо несуществующее объявление.')
        )
    await session.delete(ad)
    await session.commit()
    return ad


@router.put(
    '/announcement/{announcement_id}/change-category/{new_category}',
    dependencies=[Depends(current_user)]
    )
async def change_category(

    obj_in: AdUpdate,
    announcement_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    '''Перемещение объявления из одной группы в другую'''
    ad = await session.execute(
        select(Announcement).where(Announcement.id == announcement_id)
    )
    ad = ad.scalars().first()
    if not ad:
        raise HTTPException(
            status_code=404,
            detail='Такого объявления не существует!'
        )
    obj_data = jsonable_encoder(ad)
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(ad, field, update_data[field])
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad
