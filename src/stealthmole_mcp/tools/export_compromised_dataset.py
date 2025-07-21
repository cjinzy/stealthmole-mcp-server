from typing import Any, Dict

from ._request import _make_request


async def export_compromised_dataset(
    indicator: str, format: str = "json"
) -> Dict[str, Any]:
    """Export compromised data set as CSV/JSON."""
    endpoint = "/v2/cds/export"
    params = {"query": indicator, "exportType": format}
    return await _make_request(endpoint, params)
