import enum
from typing import Any, Dict, Optional

from ._request import _make_request

class ServiceEnum(enum.Enum):
    DT= "dt"
    TT = "tt"

async def get_node_details(
    service: ServiceEnum,
    node_id: str,
    pid: Optional[str] = None,
    data_from: bool = False,
    include_url: bool = False,
    include_contents: bool = True,
) -> Dict[str, Any]:
    """Get detailed information about a specific node.

    Args:
        service (ServiceEnum): service name
        node_id (str): node id
        pid (str, optional): pid
        data_from (bool, optional): data_from
        include_url (bool, optional): include_url
        include_contents (bool, optional): include_contents

    Returns:
        Dict[str, Any]: node information
    """
    if service not in ServiceEnum.__members__:
        raise ValueError(f"Invalid service: {service}")
    else:
        endpoint = f"/v2/{service.value}/node"
    
    params = {
        "id": node_id,
        "data_from": data_from,
        "include_url": include_url,
        "include_contents": include_contents,
    }
    if pid is not None:
        params["pid"] = pid
    return await _make_request(endpoint, params)
