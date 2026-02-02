"""Telegram search tool."""

from typing import Any, Dict

from ..constants import TELEGRAM_INDICATORS
from ._request import _make_request


async def search_telegram(
    indicator: str,
    text: str,
    target: str = "all",
    limit: int = 50,
    order_type: str = "createDate",
    order: str = "desc",
) -> Dict[str, Any]:
    """Search Telegram content.

    Args:
        indicator: The indicator type to search for
        text: Search keyword or data to find
        target: Target type to search (default: 'all')
        limit: Maximum number of results (default: 50)
        order_type: Ordering type (default: 'createDate')
        order: Sort order (default: 'desc')

    Returns:
        Search results from the API
    """
    if indicator not in TELEGRAM_INDICATORS:
        raise ValueError(
            f"Invalid indicator type: {indicator}. "
            f"Valid types: {', '.join(sorted(TELEGRAM_INDICATORS))}"
        )

    if target == "all":
        endpoint = f"/v2/tt/search/{indicator}/target/all"
    else:
        endpoint = f"/v2/tt/search/{indicator}/target"
        params = {
            "targets": target,
            "text": text,
            "limit": limit,
            "orderType": order_type,
            "order": order,
        }
        return await _make_request(endpoint, params)

    params = {
        "text": text,
        "limit": limit,
        "orderType": order_type,
        "order": order,
    }
    return await _make_request(endpoint, params)
