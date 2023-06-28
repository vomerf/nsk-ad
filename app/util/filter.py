from typing import Union

from app.models.announcement import Announcement


async def parametr_filter_for_ad(
    q: Union[str, None] = None, category: Union[str, None] = None
) -> dict:
    return {"q": q, "category": category}


async def parametr_filter_for_comment(q: Union[str, None] = None) -> dict:
    return {"q": q}


async def parametr_filter_for_complaint(q: Union[str, None] = None) -> dict:
    return {"q": q}


def filter_for_text(q, filter, model):
    if filter['q']:
        query = q.filter(model.text.like(f"%{filter['q']}%"))
        return query
    return q


def filter_for_ad(query, filter, model):
    query = filter_for_text(query, filter, model)
    if filter['category']:
        query = query.filter(Announcement.category == filter['category'])
    return query


def filter_for_comment(query, filter, model):
    query = filter_for_text(query, filter, model)
    return query


def filter_for_complaint(query, filter, model):
    query = filter_for_text(query, filter, model)
    return query
