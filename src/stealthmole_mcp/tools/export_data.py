import enum
from typing import Any, Dict

from ._request import _make_request

class ServiceEnum(enum.Enum):
    CL = "cl"
    CDS = "cds"
    CB = "cb"
    UB = "ub"


async def export_data(
    service: ServiceEnum, indicator: str, format: str = "json"
) -> Dict[str, Any]:
    """Export data in specified format.

    Args:
        service (ServiceEnum): service name
        indicator (str): search query
        format (str, optional): export format, default is json

    Returns:
        Dict[str, Any]: export data
    """
    if service not in ServiceEnum:
        raise ValueError(f"Invalid service: {service}")
    else:
        endpoint = f"/v2/{service.value}/export"
    
    params = {"query": indicator, "exportType": format}
    return await _make_request(endpoint, params)
