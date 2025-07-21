from typing import Any, Dict

from ._request import _make_request


async def get_compromised_dataset_node(node_id: str) -> Dict[str, Any]:
    """Get detailed compromised data set node information

    Args:
        node_id (str): node id

    Returns:
        Dict[str, Any]: node information
    """
    endpoint = "/v2/cds/node"
    params = {"id": node_id}
    return await _make_request(endpoint, params)
