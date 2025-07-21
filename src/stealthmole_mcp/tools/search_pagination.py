from typing import Any, Dict

from ._request import _make_request


async def search_pagination(
    service: str, search_id: str, cursor: int = 0, limit: int = 50
) -> Dict[str, Any]:
    """Pagination search using search ID for dt or tt service."""
    endpoint = f"/v2/{service}/search/{search_id}"
    params = {"cursor": cursor, "limit": limit}
    return await _make_request(endpoint, params)
