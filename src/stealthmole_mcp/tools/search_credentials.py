from typing import Any, Dict, Optional

from ._request import _make_request


async def search_credentials(
    indicator: str,
    limit: int = 50,
    cursor: int = 0,
    orderType: str = "leakedDate",
    order: str = "desc",
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for leaked credentials."""
    endpoint = "/v2/cl/search"
    params = {
        "query": indicator,
        "limit": limit,
        "cursor": cursor,
        "orderType": orderType,
        "order": order,
    }
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end
    return await _make_request(endpoint, params)
