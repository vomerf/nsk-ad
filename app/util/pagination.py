async def parameters_for_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}