from typing import Any, Dict, Optional

from ._request import _make_request


async def get_node_details(
    service: str,
    node_id: str,
    pid: Optional[str] = None,
    data_from: bool = False,
    include_url: bool = False,
    include_contents: bool = True,
) -> Dict[str, Any]:
    """Get detailed information about a specific node."""
    endpoint = f"/v2/{service}/node"
    params = {
        "id": node_id,
        "data_from": data_from,
        "include_url": include_url,
        "include_contents": include_contents,
    }
    if pid is not None:
        params["pid"] = pid
    return await _make_request(endpoint, params)
