"""Shared constants for StealthMole MCP Server."""

from typing import FrozenSet, List

# Dark web search indicator types
DARKWEB_INDICATORS: FrozenSet[str] = frozenset([
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
])

# Telegram search indicator types
TELEGRAM_INDICATORS: FrozenSet[str] = frozenset([
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
])

# Convert to sorted lists for schema enum usage
DARKWEB_INDICATORS_LIST: List[str] = sorted(DARKWEB_INDICATORS)
TELEGRAM_INDICATORS_LIST: List[str] = sorted(TELEGRAM_INDICATORS)

# Order type options
ORDER_TYPES_SEARCH = ["createDate", "value"]
ORDER_TYPES_CREDENTIALS = ["LeakedDate", "domain", "email", "password", "LeakedFrom"]
ORDER_TYPES_RANSOMWARE = ["detectionTime", "victim", "attackGroup"]
ORDER_TYPES_MONITORING = ["detectionTime", "title", "author"]

# Sort order options
SORT_ORDERS = ["asc", "desc"]

# Service types
SERVICES_DT_TT = ["dt", "tt"]
EXPORT_FORMATS = ["json", "csv"]

# Default values
DEFAULT_LIMIT = 50
DEFAULT_CURSOR = 0
DEFAULT_TARGET = "all"
DEFAULT_ORDER = "desc"
DEFAULT_ORDER_TYPE_SEARCH = "createDate"
DEFAULT_ORDER_TYPE_CREDENTIALS = "LeakedDate"
DEFAULT_ORDER_TYPE_RANSOMWARE = "detectionTime"
DEFAULT_ORDER_TYPE_MONITORING = "detectionTime"
