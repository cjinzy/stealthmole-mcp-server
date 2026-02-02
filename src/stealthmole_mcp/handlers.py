"""Tool call dispatch handlers for StealthMole MCP Server."""

from typing import Any, Awaitable, Callable, Dict, Optional

from .constants import (
    DEFAULT_CURSOR,
    DEFAULT_LIMIT,
    DEFAULT_ORDER,
    DEFAULT_ORDER_TYPE_CREDENTIALS,
    DEFAULT_ORDER_TYPE_MONITORING,
    DEFAULT_ORDER_TYPE_RANSOMWARE,
    DEFAULT_ORDER_TYPE_SEARCH,
    DEFAULT_TARGET,
)
from .utils.client import StealthMoleClient

# Type alias for handler functions
HandlerFunc = Callable[[StealthMoleClient, Dict[str, Any]], Awaitable[Any]]


async def _handle_search_darkweb(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_darkweb tool call."""
    return await client.search_darkweb(
        indicator=args["indicator"],
        text=args["text"],
        target=args.get("target", DEFAULT_TARGET),
        limit=args.get("limit", DEFAULT_LIMIT),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_SEARCH),
        order=args.get("order", DEFAULT_ORDER),
    )


async def _handle_search_telegram(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_telegram tool call."""
    return await client.search_telegram(
        indicator=args["indicator"],
        text=args["text"],
        target=args.get("target", DEFAULT_TARGET),
        limit=args.get("limit", DEFAULT_LIMIT),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_SEARCH),
        order=args.get("order", DEFAULT_ORDER),
    )


async def _handle_search_credentials(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_credentials tool call."""
    return await client.search_credentials(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
        cursor=args.get("cursor", DEFAULT_CURSOR),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_CREDENTIALS),
        order=args.get("order", DEFAULT_ORDER),
        start=args.get("start"),
        end=args.get("end"),
    )


async def _handle_search_ransomware(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_ransomware tool call."""
    return await client.search_ransomware(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
        cursor=args.get("cursor", DEFAULT_CURSOR),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_RANSOMWARE),
        order=args.get("order", DEFAULT_ORDER),
    )


async def _handle_get_node_details(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle get_node_details tool call."""
    return await client.get_node_details(
        service=args["service"],
        node_id=args["node_id"],
        pid=args.get("pid"),
        data_from=args.get("data_from", False),
        include_url=args.get("include_url", False),
        include_contents=args.get("include_contents", True),
    )


async def _handle_get_targets(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle get_targets tool call."""
    return await client.get_targets(
        service=args["service"],
        indicator=args["indicator"],
    )


async def _handle_export_data(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle export_data tool call."""
    return await client.export_data(
        service=args["service"],
        indicator=args["indicator"],
        format=args.get("format", "json"),
    )


async def _handle_search_compromised_dataset(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_compromised_dataset tool call."""
    return await client.search_compromised_dataset(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
    )


async def _handle_export_compromised_dataset(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle export_compromised_dataset tool call."""
    return await client.export_compromised_dataset(
        indicator=args["indicator"],
        format=args.get("format", "json"),
    )


async def _handle_get_compromised_dataset_node(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle get_compromised_dataset_node tool call."""
    return await client.get_compromised_dataset_node(
        node_id=args["node_id"],
    )


async def _handle_search_combo_binder(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_combo_binder tool call."""
    return await client.search_combo_binder(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
    )


async def _handle_export_combo_binder(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle export_combo_binder tool call."""
    return await client.export_combo_binder(
        indicator=args["indicator"],
        format=args.get("format", "json"),
    )


async def _handle_search_ulp_binder(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_ulp_binder tool call."""
    return await client.search_ulp_binder(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
    )


async def _handle_export_ulp_binder(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle export_ulp_binder tool call."""
    return await client.export_ulp_binder(
        indicator=args["indicator"],
        format=args.get("format", "json"),
    )


async def _handle_search_government_monitoring(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_government_monitoring tool call."""
    return await client.search_government_monitoring(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
        cursor=args.get("cursor", DEFAULT_CURSOR),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_MONITORING),
        order=args.get("order", DEFAULT_ORDER),
    )


async def _handle_search_leaked_monitoring(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_leaked_monitoring tool call."""
    return await client.search_leaked_monitoring(
        indicator=args["indicator"],
        limit=args.get("limit", DEFAULT_LIMIT),
        cursor=args.get("cursor", DEFAULT_CURSOR),
        order_type=args.get("orderType", DEFAULT_ORDER_TYPE_MONITORING),
        order=args.get("order", DEFAULT_ORDER),
    )


async def _handle_download_file(
    client: StealthMoleClient, args: Dict[str, Any]
) -> bytes:
    """Handle download_file tool call."""
    return await client.download_file(
        service=args["service"],
        file_hash=args["file_hash"],
    )


async def _handle_search_pagination(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle search_pagination tool call."""
    return await client.search_pagination(
        service=args["service"],
        search_id=args["search_id"],
        cursor=args.get("cursor", DEFAULT_CURSOR),
        limit=args.get("limit", DEFAULT_LIMIT),
    )


async def _handle_get_user_quotas(
    client: StealthMoleClient, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle get_user_quotas tool call."""
    return await client.get_user_quotas()


# Tool name to handler function mapping
TOOL_HANDLERS: Dict[str, HandlerFunc] = {
    "search_darkweb": _handle_search_darkweb,
    "search_telegram": _handle_search_telegram,
    "search_credentials": _handle_search_credentials,
    "search_ransomware": _handle_search_ransomware,
    "get_node_details": _handle_get_node_details,
    "get_targets": _handle_get_targets,
    "export_data": _handle_export_data,
    "search_compromised_dataset": _handle_search_compromised_dataset,
    "export_compromised_dataset": _handle_export_compromised_dataset,
    "get_compromised_dataset_node": _handle_get_compromised_dataset_node,
    "search_combo_binder": _handle_search_combo_binder,
    "export_combo_binder": _handle_export_combo_binder,
    "search_ulp_binder": _handle_search_ulp_binder,
    "export_ulp_binder": _handle_export_ulp_binder,
    "search_government_monitoring": _handle_search_government_monitoring,
    "search_leaked_monitoring": _handle_search_leaked_monitoring,
    "download_file": _handle_download_file,
    "search_pagination": _handle_search_pagination,
    "get_user_quotas": _handle_get_user_quotas,
}


def get_handler(tool_name: str) -> Optional[HandlerFunc]:
    """Get the handler function for a tool name."""
    return TOOL_HANDLERS.get(tool_name)
