from fastapi import Query


def pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> dict[str, int]:
    skip = (page - 1) * page_size
    return {"page": page, "page_size": page_size, "skip": skip, "limit": page_size}
