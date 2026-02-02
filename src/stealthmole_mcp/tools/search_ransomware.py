"""Ransomware search tool."""

from typing import Any, Dict

from ._request import _make_request


async def search_ransomware(
    indicator: str,
    limit: int = 50,
    cursor: int = 0,
    order_type: str = "detectionTime",
    order: str = "desc",
) -> Dict[str, Any]:
    """Search ransomware monitoring data.

    Args:
        indicator: Search query with optional indicators
        limit: Maximum number of results (default: 50)
        cursor: Pagination cursor (default: 0)
        order_type: Order type (default: 'detectionTime')
        order: Sort order (default: 'desc')

    Returns:
        Search results from the API
    """
    endpoint = "/v2/rm/search"
    params = {
        "query": indicator,
        "limit": limit,
        "cursor": cursor,
        "orderType": order_type,
        "order": order,
    }
    return await _make_request(endpoint, params)
