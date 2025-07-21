"""StealthMole API client."""

from typing import Any, Dict, Optional

from ..tools.download_file import download_file
from ..tools.export_combo_binder import export_combo_binder
from ..tools.export_compromised_dataset import export_compromised_dataset
from ..tools.export_data import export_data
from ..tools.export_ulp_binder import export_ulp_binder
from ..tools.get_compromised_dataset_node import get_compromised_dataset_node
from ..tools.get_node_details import get_node_details
from ..tools.get_targets import get_targets
from ..tools.get_user_quotas import get_user_quotas
from ..tools.search_combo_binder import search_combo_binder
from ..tools.search_compromised_dataset import search_compromised_dataset
from ..tools.search_credentials import search_credentials
from ..tools.search_darkweb import search_darkweb
from ..tools.search_government_monitoring import search_government_monitoring
from ..tools.search_leaked_monitoring import search_leaked_monitoring
from ..tools.search_pagination import search_pagination
from ..tools.search_ransomware import search_ransomware
from ..tools.search_telegram import search_telegram
from ..tools.search_ulp_binder import search_ulp_binder
from .config import StealthMoleConfig


class StealthMoleClient:
    """StealthMole API client that wraps all individual tool functions."""

    def __init__(self, config: StealthMoleConfig):
        """Initialize the client with configuration."""
        self.config = config

    async def search_darkweb(
        self,
        indicator: str,
        text: str,
        target: str = "all",
        limit: int = 50,
        orderType: str = "createDate",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search dark web content."""
        return await search_darkweb(indicator, text, target, limit, orderType, order)

    async def search_telegram(
        self,
        indicator: str,
        text: str,
        target: str = "all",
        limit: int = 50,
        orderType: str = "createDate",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search Telegram content."""
        return await search_telegram(indicator, text, target, limit, orderType, order)

    async def search_credentials(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "leakedDate",
        order: str = "desc",
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Search for leaked credentials."""
        return await search_credentials(
            indicator, limit, cursor, orderType, order, start, end
        )

    async def search_ransomware(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search ransomware monitoring data."""
        return await search_ransomware(indicator, limit, cursor, orderType, order)

    async def get_node_details(
        self,
        service: str,
        node_id: str,
        pid: Optional[str] = None,
        data_from: bool = False,
        include_url: bool = False,
        include_contents: bool = True,
    ) -> Dict[str, Any]:
        """Get detailed information about a specific node."""
        return await get_node_details(
            service, node_id, pid, data_from, include_url, include_contents
        )

    async def get_targets(
        self,
        service: str,
        indicator: str,
    ) -> Dict[str, Any]:
        """Get available search targets for a service and indicator."""
        return await get_targets(service, indicator)

    async def export_data(
        self,
        service: str,
        indicator: str,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Export search results in specified format."""
        return await export_data(service, indicator, format)

    async def search_compromised_dataset(
        self,
        indicator: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Search compromised data set information."""
        return await search_compromised_dataset(indicator, limit)

    async def export_compromised_dataset(
        self,
        indicator: str,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Export compromised data set as CSV/JSON."""
        return await export_compromised_dataset(indicator, format)

    async def get_compromised_dataset_node(
        self,
        node_id: str,
    ) -> Dict[str, Any]:
        """Get detailed compromised data set node information."""
        return await get_compromised_dataset_node(node_id)

    async def search_combo_binder(
        self,
        indicator: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Search leaked ID/Password combo information."""
        return await search_combo_binder(indicator, limit)

    async def export_combo_binder(
        self,
        indicator: str,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Export combo binder data as CSV/JSON."""
        return await export_combo_binder(indicator, format)

    async def search_ulp_binder(
        self,
        indicator: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Search URL-Login-Password combination information."""
        return await search_ulp_binder(indicator, limit)

    async def export_ulp_binder(
        self,
        indicator: str,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Export ULP binder data as CSV/JSON."""
        return await export_ulp_binder(indicator, format)

    async def search_government_monitoring(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search government sector threat monitoring data."""
        return await search_government_monitoring(
            indicator, limit, cursor, orderType, order
        )

    async def search_leaked_monitoring(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search enterprise sector threat monitoring data."""
        return await search_leaked_monitoring(
            indicator, limit, cursor, orderType, order
        )

    async def download_file(
        self,
        service: str,
        file_hash: str,
    ) -> bytes:
        """Download file by hash from dt or tt service."""
        return await download_file(service, file_hash)

    async def search_pagination(
        self,
        service: str,
        search_id: str,
        cursor: int = 0,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Pagination search using search ID for dt or tt service."""
        return await search_pagination(service, search_id, cursor, limit)

    async def get_user_quotas(self) -> Dict[str, Any]:
        """Get API usage quotas by service."""
        return await get_user_quotas()
