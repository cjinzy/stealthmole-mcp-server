"""HTTP request utilities for StealthMole API."""

import asyncio
import time
import uuid
from typing import Any, Dict, Optional

import httpx
import jwt

from ..utils.config import StealthMoleConfig

# Module-level config singleton
_config: Optional[StealthMoleConfig] = None


def init_config(config: StealthMoleConfig) -> None:
    """Initialize the module-level config singleton."""
    global _config
    _config = config


def get_config() -> StealthMoleConfig:
    """Get the current config, creating a default if not initialized."""
    global _config
    if _config is None:
        _config = StealthMoleConfig()
    return _config


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


async def _make_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    config: Optional[StealthMoleConfig] = None,
) -> Dict[str, Any]:
    """Make authenticated request to StealthMole API with retry logic.

    Args:
        endpoint: API endpoint path
        params: Optional query parameters
        config: Optional config override; uses singleton if not provided
    """
    cfg = config or get_config()
    url = f"{cfg.base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=cfg.timeout) as client:
        for attempt in range(cfg.max_retries):
            try:
                headers = _get_headers(cfg)
                response = await client.get(url, headers=headers, params=params or {})
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == cfg.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"Request timed out after {cfg.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(cfg.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < cfg.max_retries - 1:
                    await asyncio.sleep(cfg.retry_delay * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("Request failed after all retry attempts")


async def _download_file(
    service: str,
    file_hash: str,
    config: Optional[StealthMoleConfig] = None,
) -> bytes:
    """Download file by hash from dt or tt service with extended timeout.

    Args:
        service: Service type (dt or tt)
        file_hash: File hash to download
        config: Optional config override; uses singleton if not provided
    """
    cfg = config or get_config()
    url = f"{cfg.base_url}/v2/api/file/{service}/f/{file_hash}"

    async with httpx.AsyncClient(timeout=cfg.download_timeout) as client:
        for attempt in range(cfg.max_retries):
            try:
                headers = _get_headers(cfg)
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == cfg.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"File download timed out after {cfg.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(cfg.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < cfg.max_retries - 1:
                    await asyncio.sleep(cfg.retry_delay * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("File download failed after all retry attempts")
