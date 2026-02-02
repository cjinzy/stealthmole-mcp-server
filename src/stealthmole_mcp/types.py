"""Type definitions for StealthMole MCP Server."""

from typing import Any, Dict, List, Optional, TypedDict


class SearchResult(TypedDict, total=False):
    """Generic search result structure."""
    response_code: int
    message: str
    data: List[Dict[str, Any]]
    total: int
    cursor: int
    search_id: str


class NodeDetails(TypedDict, total=False):
    """Node details response structure."""
    response_code: int
    message: str
    data: Dict[str, Any]


class QuotaInfo(TypedDict):
    """Quota information for a service."""
    allowed: int
    used: int
    remaining: int


class UserQuotas(TypedDict, total=False):
    """User quotas response structure."""
    response_code: int
    message: str
    data: Dict[str, QuotaInfo]


class ExportResult(TypedDict, total=False):
    """Export result structure."""
    response_code: int
    message: str
    data: Any  # Can be list or string depending on format


class TargetsResult(TypedDict, total=False):
    """Targets result structure."""
    response_code: int
    message: str
    data: List[str]


# Type alias for API responses
APIResponse = Dict[str, Any]
