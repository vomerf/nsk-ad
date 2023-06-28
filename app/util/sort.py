def sort_query(sort: str, query: list):
    reverse = False
    if sort.startswith("-"):
        reverse = True
        sort = sort[1:]
    query = sorted(query, key=lambda x: getattr(x, sort), reverse=reverse)
    return query
