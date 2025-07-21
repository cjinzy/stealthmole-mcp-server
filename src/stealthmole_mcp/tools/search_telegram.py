from typing import Any, Dict

from ._request import _make_request


async def search_telegram(
    indicator: str,
    text: str,
    target: str = "all",
    limit: int = 50,
    orderType: str = "createDate",
    order: str = "desc",
) -> Dict[str, Any]:
    """Search Telegram content."""
    valid_indicators = {
        "band",
        "bitcoin",
        "creditcard",
        "cve",
        "discord",
        "document",
        "domain",
        "email",
        "ethereum",
        "exefile",
        "facebook",
        "filehosting",
        "googledrive",
        "gps",
        "hash",
        "hashstring",
        "i2p",
        "i2purl",
        "id",
        "image",
        "instagram",
        "ip",
        "kakaotalk",
        "keyword",
        "kssn",
        "line",
        "monero",
        "otherfile",
        "pastebin",
        "pgp",
        "tel",
        "session",
        "shorten",
        "telegram",
        "telegram.channel",
        "telegram.message",
        "telegram.user",
        "tor",
        "torurl",
        "tox",
        "twitter",
        "url",
    }

    if indicator not in valid_indicators:
        raise ValueError(
            f"Invalid indicator type: {indicator}. Valid types: {', '.join(sorted(valid_indicators))}"
        )

    if target == "all":
        endpoint = f"/v2/tt/search/{indicator}/target/all"
    else:
        endpoint = f"/v2/tt/search/{indicator}/target"
        params = {
            "targets": target,
            "text": text,
            "limit": limit,
            "orderType": orderType,
            "order": order,
        }
        return await _make_request(endpoint, params)
    params = {"text": text, "limit": limit, "orderType": orderType, "order": order}
    return await _make_request(endpoint, params)
