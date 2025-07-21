from typing import Any, Dict

from ._request import _make_request


async def export_combo_binder(indicator: str, format: str = "json") -> Dict[str, Any]:
    """Export combo binder data as CSV/JSON."""
    endpoint = "/v2/cb/export"
    params = {"query": indicator, "exportType": format}
    return await _make_request(endpoint, params)
