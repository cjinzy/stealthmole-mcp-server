from typing import Any, Dict

from ._request import _make_request


async def search_ulp_binder(indicator: str, limit: int = 50) -> Dict[str, Any]:
    """Search URL-Login-Password combination information."""
    endpoint = "/v2/ub/search"
    params = {"query": indicator, "limit": limit}
    return await _make_request(endpoint, params)
