"""Credentials search tool."""

from typing import Any, Dict, Optional

from ._request import _make_request


async def search_credentials(
    indicator: str,
    limit: int = 50,
    cursor: int = 0,
    order_type: str = "LeakedDate",
    order: str = "desc",
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for leaked credentials.

    Args:
        indicator: Search query with optional indicators
        limit: Maximum number of results (default: 50)
        cursor: Pagination cursor (default: 0)
        order_type: Order type (default: 'LeakedDate')
        order: Sort order (default: 'desc')
        start: Filter data after start time (UTC timestamp)
        end: Filter data before end time (UTC timestamp)

    Returns:
        Search results from the API
    """
    endpoint = "/v2/cl/search"
    params: Dict[str, Any] = {
        "query": indicator,
        "limit": limit,
        "cursor": cursor,
        "orderType": order_type,
        "order": order,
    }
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end
    return await _make_request(endpoint, params)
