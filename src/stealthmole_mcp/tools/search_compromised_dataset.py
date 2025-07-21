from typing import Any, Dict

from ._request import _make_request


async def search_compromised_dataset(indicator: str, limit: int = 50) -> Dict[str, Any]:
    """Search compromised data set information."""
    endpoint = "/v2/cds/search"
    params = {"query": indicator, "limit": limit}
    return await _make_request(endpoint, params)
