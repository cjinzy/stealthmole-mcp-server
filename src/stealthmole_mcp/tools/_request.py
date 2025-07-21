import asyncio
import time
import uuid
from typing import Any, Dict, Optional

import httpx
import jwt

from ..utils.config import StealthMoleConfig


async def _make_request(endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated request to StealthMole API with retry logic."""
    config = StealthMoleConfig()
    url = f"{config.base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=config.timeout) as client:
        for attempt in range(config.max_retries):
            try:
                headers = _get_headers(config)
                response = await client.get(url, headers=headers, params=params or {})
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == config.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"Request timed out after {config.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(config.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < config.max_retries - 1:
                    await asyncio.sleep(config.retry_delay * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("Request failed after all retry attempts")


async def _download_file(service: str, file_hash: str) -> bytes:
    """Download file by hash from dt or tt service with extended timeout."""
    config = StealthMoleConfig()
    url = f"{config.base_url}/v2/api/file/{service}/f/{file_hash}"

    async with httpx.AsyncClient(timeout=config.download_timeout) as client:
        for attempt in range(config.max_retries):
            try:
                headers = _get_headers(config)
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == config.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"File download timed out after {config.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(config.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < config.max_retries - 1:
                    await asyncio.sleep(config.retry_delay * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("File download failed after all retry attempts")


def _generate_jwt_token(config: StealthMoleConfig) -> str:
    """Generate JWT token for authentication."""
    payload = {
        "access_key": config.access_key,
        "nonce": str(uuid.uuid4()),
        "iat": int(time.time()),
    }
    return jwt.encode(payload, config.secret_key, algorithm="HS256")


def _get_headers(config: StealthMoleConfig) -> Dict[str, str]:
    """Get headers with JWT authentication."""
    token = _generate_jwt_token(config)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
