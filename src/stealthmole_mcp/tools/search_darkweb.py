from typing import Any, Dict

from ._request import _make_request


async def search_darkweb(
    indicator: str,
    text: str,
    target: str = "all",
    limit: int = 50,
    orderType: str = "createDate",
    order: str = "desc",
) -> Dict[str, Any]:
    """Search dark web content."""
    valid_indicators = {
        "adsense",
        "analyticsid",
        "band",
        "bitcoin",
        "blueprint",
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
        "ioc",
        "ip",
        "kakaotalk",
        "keyword",
        "kssn",
        "leakedaudio",
        "leakedemailfile",
        "leakedvideo",
        "line",
        "linkedin",
        "malware",
        "monero",
        "otherfile",
        "pastebin",
        "pgp",
        "serverstatus",
        "session",
        "shorten",
        "sshkey",
        "sslkey",
        "tel",
        "telegram",
        "tor",
        "torurl",
        "twitter",
        "url",
        "iol",
    }

    if indicator not in valid_indicators:
        raise ValueError(
            f"Invalid indicator type: {indicator}. Valid types: {', '.join(sorted(valid_indicators))}"
        )

    endpoint = f"/v2/dt/search/{indicator}/target/all"
    params = {"text": text, "limit": limit, "orderType": orderType, "order": order}
    return await _make_request(endpoint, params)
