from fastapi import Query


async def parameters_for_pagination(
    skip: int = Query(0, gt=-1), limit: int = Query(10, gt=-1)
):
    return {"skip": skip, "limit": limit}
