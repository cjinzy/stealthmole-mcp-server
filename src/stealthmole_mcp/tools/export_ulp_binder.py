from typing import Any, Dict

from ._request import _make_request


async def export_ulp_binder(indicator: str, format: str = "json") -> Dict[str, Any]:
    """Export ULP binder data as CSV/JSON."""
    endpoint = "/v2/ub/export"
    params = {"query": indicator, "exportType": format}
    return await _make_request(endpoint, params)
