from typing import Any, Dict

from ._request import _make_request


async def search_leaked_monitoring(
    indicator: str,
    limit: int = 50,
    cursor: int = 0,
    orderType: str = "detectionTime",
    order: str = "desc",
) -> Dict[str, Any]:
    """Search enterprise sector threat monitoring data."""
    endpoint = "/v2/lm/search"
    params = {
        "query": indicator,
        "limit": limit,
        "cursor": cursor,
        "orderType": orderType,
        "order": order,
    }
    return await _make_request(endpoint, params)
