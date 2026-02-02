"""Tool schema definitions for StealthMole MCP Server."""

from typing import Any, Dict, List

from .constants import (
    DARKWEB_INDICATORS_LIST,
    DEFAULT_CURSOR,
    DEFAULT_LIMIT,
    DEFAULT_ORDER,
    DEFAULT_ORDER_TYPE_CREDENTIALS,
    DEFAULT_ORDER_TYPE_MONITORING,
    DEFAULT_ORDER_TYPE_RANSOMWARE,
    DEFAULT_ORDER_TYPE_SEARCH,
    DEFAULT_TARGET,
    EXPORT_FORMATS,
    ORDER_TYPES_CREDENTIALS,
    ORDER_TYPES_MONITORING,
    ORDER_TYPES_RANSOMWARE,
    ORDER_TYPES_SEARCH,
    SERVICES_DT_TT,
    SORT_ORDERS,
    TELEGRAM_INDICATORS_LIST,
)


def _create_search_schema(
    indicators: List[str],
    order_types: List[str],
    default_order_type: str,
) -> Dict[str, Any]:
    """Create a standard search input schema."""
    return {
        "type": "object",
        "properties": {
            "indicator": {
                "type": "string",
                "description": "The indicator type to search for",
                "enum": indicators,
            },
            "text": {
                "type": "string",
                "description": "Search keyword or data to find. Supports AND, OR, NOT operators (max 3 OR, 5 total operators)",
            },
            "target": {
                "type": "string",
                "description": f"Target type to search (default: '{DEFAULT_TARGET}'). Use comma-separated values for multiple targets",
                "default": DEFAULT_TARGET,
            },
            "limit": {
                "type": "integer",
                "description": f"Maximum number of results (default: {DEFAULT_LIMIT})",
                "default": DEFAULT_LIMIT,
                "minimum": 1,
                "maximum": 50,
            },
            "orderType": {
                "type": "string",
                "description": "Ordering type",
                "enum": order_types,
                "default": default_order_type,
            },
            "order": {
                "type": "string",
                "description": "Sort order",
                "enum": SORT_ORDERS,
                "default": DEFAULT_ORDER,
            },
        },
        "required": ["indicator", "text"],
    }


def _create_paginated_schema(
    indicator_description: str,
    order_types: List[str],
    default_order_type: str,
) -> Dict[str, Any]:
    """Create a paginated search input schema."""
    return {
        "type": "object",
        "properties": {
            "indicator": {
                "type": "string",
                "description": indicator_description,
            },
            "limit": {
                "type": "integer",
                "description": f"Maximum number of results (default: {DEFAULT_LIMIT})",
                "default": DEFAULT_LIMIT,
                "minimum": 1,
                "maximum": 50,
            },
            "cursor": {
                "type": "integer",
                "description": f"Pagination cursor (default: {DEFAULT_CURSOR})",
                "default": DEFAULT_CURSOR,
                "minimum": 0,
            },
            "orderType": {
                "type": "string",
                "description": "Order type",
                "enum": order_types,
                "default": default_order_type,
            },
            "order": {
                "type": "string",
                "description": "Sort order",
                "enum": SORT_ORDERS,
                "default": DEFAULT_ORDER,
            },
        },
        "required": ["indicator"],
    }


def _create_simple_search_schema(indicator_description: str) -> Dict[str, Any]:
    """Create a simple search input schema with indicator and limit."""
    return {
        "type": "object",
        "properties": {
            "indicator": {
                "type": "string",
                "description": indicator_description,
            },
            "limit": {
                "type": "integer",
                "description": f"Maximum number of results (default: {DEFAULT_LIMIT})",
                "default": DEFAULT_LIMIT,
                "minimum": 1,
                "maximum": 50,
            },
        },
        "required": ["indicator"],
    }


def _create_export_schema(indicator_description: str) -> Dict[str, Any]:
    """Create an export input schema."""
    return {
        "type": "object",
        "properties": {
            "indicator": {
                "type": "string",
                "description": indicator_description,
            },
            "format": {
                "type": "string",
                "description": "Export format (json or csv)",
                "enum": EXPORT_FORMATS,
                "default": "json",
            },
        },
        "required": ["indicator"],
    }


# Tool schema definitions
TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "search_darkweb",
        "description": "Search dark web content for indicators like domains, IPs, emails, etc.",
        "inputSchema": _create_search_schema(
            DARKWEB_INDICATORS_LIST,
            ORDER_TYPES_SEARCH,
            DEFAULT_ORDER_TYPE_SEARCH,
        ),
    },
    {
        "name": "search_telegram",
        "description": "Search Telegram content for indicators",
        "inputSchema": _create_search_schema(
            TELEGRAM_INDICATORS_LIST,
            ORDER_TYPES_SEARCH,
            DEFAULT_ORDER_TYPE_SEARCH,
        ),
    },
    {
        "name": "search_credentials",
        "description": "Search for leaked credentials using keywords or specific indicators (domain:, email:, id:, password:, after:, before:)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "indicator": {
                    "type": "string",
                    "description": "Search query - can use indicators like 'domain:example.com', 'email:user@domain.com', 'id:username', 'password:pass123', 'after:2023-01', 'before:2024-01' or plain keywords",
                },
                "limit": {
                    "type": "integer",
                    "description": f"Maximum number of results (default: {DEFAULT_LIMIT})",
                    "default": DEFAULT_LIMIT,
                    "minimum": 1,
                    "maximum": 50,
                },
                "cursor": {
                    "type": "integer",
                    "description": f"Pagination cursor (default: {DEFAULT_CURSOR})",
                    "default": DEFAULT_CURSOR,
                    "minimum": 0,
                },
                "orderType": {
                    "type": "string",
                    "description": "Order type",
                    "enum": ORDER_TYPES_CREDENTIALS,
                    "default": DEFAULT_ORDER_TYPE_CREDENTIALS,
                },
                "order": {
                    "type": "string",
                    "description": "Sort order",
                    "enum": SORT_ORDERS,
                    "default": DEFAULT_ORDER,
                },
                "start": {
                    "type": "integer",
                    "description": "Filter data added to the system after start time (UTC timestamp)",
                },
                "end": {
                    "type": "integer",
                    "description": "Filter data added to the system before end time (UTC timestamp)",
                },
            },
            "required": ["indicator"],
        },
    },
    {
        "name": "search_ransomware",
        "description": "Search ransomware monitoring data using torurl: or domain: indicators",
        "inputSchema": _create_paginated_schema(
            "Search query - use 'torurl:site.onion' to search ransomware sites or 'domain:victim.com' to search victim websites. Leave empty for recent list.",
            ORDER_TYPES_RANSOMWARE,
            DEFAULT_ORDER_TYPE_RANSOMWARE,
        ),
    },
    {
        "name": "get_node_details",
        "description": "Get detailed information about a specific node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service type (dt, tt, cl, rm, etc.)",
                },
                "node_id": {
                    "type": "string",
                    "description": "Node ID to get details for",
                },
                "pid": {
                    "type": "string",
                    "description": "Parent node ID (optional)",
                },
                "data_from": {
                    "type": "boolean",
                    "description": "Import data source list (default: False)",
                    "default": False,
                },
                "include_url": {
                    "type": "boolean",
                    "description": "Import included URL list (default: False)",
                    "default": False,
                },
                "include_contents": {
                    "type": "boolean",
                    "description": "Include HTML source contents for torurl, i2purl, url (default: True)",
                    "default": True,
                },
            },
            "required": ["service", "node_id"],
        },
    },
    {
        "name": "get_targets",
        "description": "Get available search targets for a service and indicator",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service type (dt, tt, cl, rm, etc.)",
                },
                "indicator": {
                    "type": "string",
                    "description": "The indicator type",
                },
            },
            "required": ["service", "indicator"],
        },
    },
    {
        "name": "export_data",
        "description": "Export search results in specified format",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service type (dt, tt, cl, rm, etc.)",
                },
                "indicator": {
                    "type": "string",
                    "description": "The indicator to export data for",
                },
                "format": {
                    "type": "string",
                    "description": "Export format (json or csv)",
                    "enum": EXPORT_FORMATS,
                    "default": "json",
                },
            },
            "required": ["service", "indicator"],
        },
    },
    {
        "name": "search_compromised_dataset",
        "description": "Search compromised data set information",
        "inputSchema": _create_simple_search_schema("The indicator to search for"),
    },
    {
        "name": "export_compromised_dataset",
        "description": "Export compromised data set as CSV/JSON",
        "inputSchema": _create_export_schema("The indicator to export data for"),
    },
    {
        "name": "get_compromised_dataset_node",
        "description": "Get detailed compromised data set node information (Cyber Security Edition required)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node_id": {
                    "type": "string",
                    "description": "Node ID to get details for",
                },
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "search_combo_binder",
        "description": "Search leaked ID/Password combo information",
        "inputSchema": _create_simple_search_schema("The indicator to search for"),
    },
    {
        "name": "export_combo_binder",
        "description": "Export combo binder data as CSV/JSON",
        "inputSchema": _create_export_schema("The indicator to export data for"),
    },
    {
        "name": "search_ulp_binder",
        "description": "Search URL-Login-Password combination information",
        "inputSchema": _create_simple_search_schema("The indicator to search for"),
    },
    {
        "name": "export_ulp_binder",
        "description": "Export ULP binder data as CSV/JSON",
        "inputSchema": _create_export_schema("The indicator to export data for"),
    },
    {
        "name": "search_government_monitoring",
        "description": "Search government sector threat monitoring data using url: or id: indicators",
        "inputSchema": _create_paginated_schema(
            "Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.",
            ORDER_TYPES_MONITORING,
            DEFAULT_ORDER_TYPE_MONITORING,
        ),
    },
    {
        "name": "search_leaked_monitoring",
        "description": "Search enterprise sector threat monitoring data using url: or id: indicators",
        "inputSchema": _create_paginated_schema(
            "Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.",
            ORDER_TYPES_MONITORING,
            DEFAULT_ORDER_TYPE_MONITORING,
        ),
    },
    {
        "name": "download_file",
        "description": "Download file by hash from dt or tt service",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service type (dt or tt)",
                    "enum": SERVICES_DT_TT,
                },
                "file_hash": {
                    "type": "string",
                    "description": "File hash to download",
                },
            },
            "required": ["service", "file_hash"],
        },
    },
    {
        "name": "search_pagination",
        "description": "Pagination search using search ID for dt or tt service",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service type (dt or tt)",
                    "enum": SERVICES_DT_TT,
                },
                "search_id": {
                    "type": "string",
                    "description": "Search ID from previous search",
                },
                "cursor": {
                    "type": "integer",
                    "description": f"Pagination cursor (default: {DEFAULT_CURSOR})",
                    "default": DEFAULT_CURSOR,
                    "minimum": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": f"Maximum number of results (default: {DEFAULT_LIMIT})",
                    "default": DEFAULT_LIMIT,
                    "minimum": 1,
                    "maximum": 50,
                },
            },
            "required": ["service", "search_id"],
        },
    },
    {
        "name": "get_user_quotas",
        "description": "Get API usage quotas by service",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# Build a name-to-schema mapping for quick lookup
TOOL_SCHEMA_MAP: Dict[str, Dict[str, Any]] = {
    schema["name"]: schema for schema in TOOL_SCHEMAS
}
