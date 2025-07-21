from ._request import _download_file


async def download_file(service: str, file_hash: str) -> bytes:
    """Download file by hash from dt or tt service with extended timeout."""
    return await _download_file(service, file_hash)
