from typing import Any, Dict

from ._request import _make_request


async def search_combo_binder(indicator: str, limit: int = 50) -> Dict[str, Any]:
    """Search leaked ID/Password combo information."""
    endpoint = "/v2/cb/search"
    params = {"query": indicator, "limit": limit}
    return await _make_request(endpoint, params)
