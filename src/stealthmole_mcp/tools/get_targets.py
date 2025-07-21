from typing import Any, Dict

from ._request import _make_request


async def get_targets(service: str, indicator: str) -> Dict[str, Any]:
    """Get available targets for a service and indicator."""
    endpoint = f"/v2/{service}/search/{indicator}/targets"
    return await _make_request(endpoint)
