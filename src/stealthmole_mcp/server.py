"""StealthMole MCP Server implementation using FastMCP."""

import os
import sys
from contextlib import asynccontextmanager
from typing import Annotated, Literal, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

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
    TELEGRAM_INDICATORS_LIST,
)
from .prompts import STEALTHMOLE_DEFAULT_PROMPT
from .tools._request import init_config
from .utils.client import StealthMoleClient
from .utils.config import StealthMoleConfig

load_dotenv()

# Build indicator description strings
DARKWEB_INDICATOR_DESC = f"Indicator type to search. Valid values: {', '.join(DARKWEB_INDICATORS_LIST)}"
TELEGRAM_INDICATOR_DESC = f"Indicator type to search. Valid values: {', '.join(TELEGRAM_INDICATORS_LIST)}"

# Global client instance
_client: Optional[StealthMoleClient] = None


def get_client() -> StealthMoleClient:
    """Dependency that provides the StealthMole client."""
    if _client is None:
        raise RuntimeError("StealthMole client not initialized. Please check your API credentials.")
    return _client


@asynccontextmanager
async def lifespan(mcp: FastMCP):
    """Initialize and cleanup StealthMole client."""
    global _client

    print("Starting StealthMole MCP server...", file=sys.stderr)

    access_key = os.getenv("STEALTHMOLE_ACCESS_KEY")
    secret_key = os.getenv("STEALTHMOLE_SECRET_KEY")

    print(f"Access key: {'SET' if access_key else 'NOT SET'}", file=sys.stderr)
    print(f"Secret key: {'SET' if secret_key else 'NOT SET'}", file=sys.stderr)

    if not access_key or not secret_key:
        print(
            "Warning: STEALTHMOLE_ACCESS_KEY and STEALTHMOLE_SECRET_KEY environment variables not set",
            file=sys.stderr,
        )
        print("MCP server will start but tools will not function", file=sys.stderr)
        _client = None
    else:
        try:
            config = StealthMoleConfig(access_key=access_key, secret_key=secret_key)
            print("StealthMole config created", file=sys.stderr)

            init_config(config)

            _client = StealthMoleClient(config)
            print("StealthMole client initialized", file=sys.stderr)

            try:
                quotas = await _client.get_user_quotas()
                print(f"API connection successful. Available quotas: {quotas}", file=sys.stderr)
            except Exception as api_error:
                print(f"Warning: API test failed: {api_error}", file=sys.stderr)
                print("Continuing with server startup...", file=sys.stderr)

        except Exception as e:
            print(f"Warning: Error creating StealthMole client: {e}", file=sys.stderr)
            print("MCP server will start but tools may not function properly", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            _client = None

    yield

    print("StealthMole MCP server stopped", file=sys.stderr)
    _client = None


mcp = FastMCP(
    name="stealthmole-mcp",
    version="0.2.0",
    instructions=STEALTHMOLE_DEFAULT_PROMPT,
    lifespan=lifespan,
)


# --- Prompts ---


@mcp.prompt(
    name="stealthmole_default_prompt",
    description="Default behavior guidelines for StealthMole MCP",
)
def stealthmole_prompt(context: str = "") -> str:
    """Return the default StealthMole prompt."""
    return STEALTHMOLE_DEFAULT_PROMPT


# --- Search Tools ---


@mcp.tool
async def search_darkweb(
    text: Annotated[str, Field(description="Search keyword or data to find. Supports AND, OR, NOT operators (max 3 OR, 5 total operators)")],
    indicator: Annotated[str, Field(description=DARKWEB_INDICATOR_DESC)] = "keyword",
    target: Annotated[str, Field(description="Target type to search. Use comma-separated values for multiple targets")] = DEFAULT_TARGET,
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    order_type: Annotated[str, Field(description="Ordering type: createDate or value")] = DEFAULT_ORDER_TYPE_SEARCH,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search dark web content for indicators like domains, IPs, emails, etc."""
    return await client.search_darkweb(
        indicator=indicator,
        text=text,
        target=target,
        limit=limit,
        order_type=order_type,
        order=order,
    )


@mcp.tool
async def search_telegram(
    text: Annotated[str, Field(description="Search keyword or data to find. Supports AND, OR, NOT operators (max 3 OR, 5 total operators)")],
    indicator: Annotated[str, Field(description=TELEGRAM_INDICATOR_DESC)] = "keyword",
    target: Annotated[str, Field(description="Target type to search. Use comma-separated values for multiple targets")] = DEFAULT_TARGET,
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    order_type: Annotated[str, Field(description="Ordering type: createDate or value")] = DEFAULT_ORDER_TYPE_SEARCH,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search Telegram content for indicators."""
    return await client.search_telegram(
        indicator=indicator,
        text=text,
        target=target,
        limit=limit,
        order_type=order_type,
        order=order,
    )


@mcp.tool
async def search_credentials(
    indicator: Annotated[str, Field(description="Search query - can use indicators like 'domain:example.com', 'email:user@domain.com', 'id:username', 'password:pass123', 'after:2023-01', 'before:2024-01' or plain keywords")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    cursor: Annotated[int, Field(ge=0, description="Pagination cursor")] = DEFAULT_CURSOR,
    order_type: Annotated[str, Field(description="Order type: LeakedDate, domain, email, password, or LeakedFrom")] = DEFAULT_ORDER_TYPE_CREDENTIALS,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    start: Annotated[Optional[int], Field(description="Filter data added to the system after start time (UTC timestamp)")] = None,
    end: Annotated[Optional[int], Field(description="Filter data added to the system before end time (UTC timestamp)")] = None,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search for leaked credentials using keywords or specific indicators."""
    return await client.search_credentials(
        indicator=indicator,
        limit=limit,
        cursor=cursor,
        order_type=order_type,
        order=order,
        start=start,
        end=end,
    )


@mcp.tool
async def search_ransomware(
    indicator: Annotated[str, Field(description="Search query - use 'torurl:site.onion' to search ransomware sites or 'domain:victim.com' to search victim websites. Leave empty for recent list.")] = "",
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    cursor: Annotated[int, Field(ge=0, description="Pagination cursor")] = DEFAULT_CURSOR,
    order_type: Annotated[str, Field(description="Order type: detectionTime, victim, or attackGroup")] = DEFAULT_ORDER_TYPE_RANSOMWARE,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search ransomware monitoring data using torurl: or domain: indicators."""
    return await client.search_ransomware(
        indicator=indicator,
        limit=limit,
        cursor=cursor,
        order_type=order_type,
        order=order,
    )


@mcp.tool
async def search_compromised_dataset(
    indicator: Annotated[str, Field(description="The indicator to search for")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search compromised data set information."""
    return await client.search_compromised_dataset(
        indicator=indicator,
        limit=limit,
    )


@mcp.tool
async def search_combo_binder(
    indicator: Annotated[str, Field(description="The indicator to search for")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search leaked ID/Password combo information."""
    return await client.search_combo_binder(
        indicator=indicator,
        limit=limit,
    )


@mcp.tool
async def search_ulp_binder(
    indicator: Annotated[str, Field(description="The indicator to search for")],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search URL-Login-Password combination information."""
    return await client.search_ulp_binder(
        indicator=indicator,
        limit=limit,
    )


@mcp.tool
async def search_government_monitoring(
    indicator: Annotated[str, Field(description="Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.")] = "",
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    cursor: Annotated[int, Field(ge=0, description="Pagination cursor")] = DEFAULT_CURSOR,
    order_type: Annotated[str, Field(description="Order type: detectionTime, title, or author")] = DEFAULT_ORDER_TYPE_MONITORING,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search government sector threat monitoring data using url: or id: indicators."""
    return await client.search_government_monitoring(
        indicator=indicator,
        limit=limit,
        cursor=cursor,
        order_type=order_type,
        order=order,
    )


@mcp.tool
async def search_leaked_monitoring(
    indicator: Annotated[str, Field(description="Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.")] = "",
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    cursor: Annotated[int, Field(ge=0, description="Pagination cursor")] = DEFAULT_CURSOR,
    order_type: Annotated[str, Field(description="Order type: detectionTime, title, or author")] = DEFAULT_ORDER_TYPE_MONITORING,
    order: Annotated[str, Field(description="Sort order: asc or desc")] = DEFAULT_ORDER,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Search enterprise sector threat monitoring data using url: or id: indicators."""
    return await client.search_leaked_monitoring(
        indicator=indicator,
        limit=limit,
        cursor=cursor,
        order_type=order_type,
        order=order,
    )


@mcp.tool
async def search_pagination(
    service: Annotated[Literal["dt", "tt"], Field(description="Service type (dt or tt)")],
    search_id: Annotated[str, Field(description="Search ID from previous search")],
    cursor: Annotated[int, Field(ge=0, description="Pagination cursor")] = DEFAULT_CURSOR,
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum number of results (1-50)")] = DEFAULT_LIMIT,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Pagination search using search ID for dt or tt service."""
    return await client.search_pagination(
        service=service,
        search_id=search_id,
        cursor=cursor,
        limit=limit,
    )


# --- Export Tools ---


@mcp.tool
async def export_data(
    service: Annotated[str, Field(description="Service type (dt, tt, cl, rm, etc.)")],
    indicator: Annotated[str, Field(description="The indicator to export data for")],
    format: Annotated[Literal["json", "csv"], Field(description="Export format")] = "json",
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Export search results in specified format."""
    return await client.export_data(
        service=service,
        indicator=indicator,
        format=format,
    )


@mcp.tool
async def export_compromised_dataset(
    indicator: Annotated[str, Field(description="The indicator to export data for")],
    format: Annotated[Literal["json", "csv"], Field(description="Export format")] = "json",
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Export compromised data set as CSV/JSON."""
    return await client.export_compromised_dataset(
        indicator=indicator,
        format=format,
    )


@mcp.tool
async def export_combo_binder(
    indicator: Annotated[str, Field(description="The indicator to export data for")],
    format: Annotated[Literal["json", "csv"], Field(description="Export format")] = "json",
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Export combo binder data as CSV/JSON."""
    return await client.export_combo_binder(
        indicator=indicator,
        format=format,
    )


@mcp.tool
async def export_ulp_binder(
    indicator: Annotated[str, Field(description="The indicator to export data for")],
    format: Annotated[Literal["json", "csv"], Field(description="Export format")] = "json",
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Export ULP binder data as CSV/JSON."""
    return await client.export_ulp_binder(
        indicator=indicator,
        format=format,
    )


# --- Utility Tools ---


@mcp.tool
async def get_node_details(
    service: Annotated[str, Field(description="Service type (dt, tt, cl, rm, etc.)")],
    node_id: Annotated[str, Field(description="Node ID to get details for")],
    pid: Annotated[Optional[str], Field(description="Parent node ID")] = None,
    data_from: Annotated[bool, Field(description="Import data source list")] = False,
    include_url: Annotated[bool, Field(description="Import included URL list")] = False,
    include_contents: Annotated[bool, Field(description="Include HTML source contents for torurl, i2purl, url")] = True,
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Get detailed information about a specific node."""
    return await client.get_node_details(
        service=service,
        node_id=node_id,
        pid=pid,
        data_from=data_from,
        include_url=include_url,
        include_contents=include_contents,
    )


@mcp.tool
async def get_targets(
    service: Annotated[str, Field(description="Service type (dt, tt, cl, rm, etc.)")],
    indicator: Annotated[str, Field(description="The indicator type")],
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Get available search targets for a service and indicator."""
    return await client.get_targets(
        service=service,
        indicator=indicator,
    )


@mcp.tool
async def get_compromised_dataset_node(
    node_id: Annotated[str, Field(description="Node ID to get details for")],
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Get detailed compromised data set node information (Cyber Security Edition required)."""
    return await client.get_compromised_dataset_node(
        node_id=node_id,
    )


@mcp.tool
async def download_file(
    service: Annotated[Literal["dt", "tt"], Field(description="Service type (dt or tt)")],
    file_hash: Annotated[str, Field(description="File hash to download")],
    client: StealthMoleClient = Depends(get_client),
) -> str:
    """Download file by hash from dt or tt service."""
    file_content = await client.download_file(
        service=service,
        file_hash=file_hash,
    )
    return f"Downloaded file {file_hash} from {service} service. File size: {len(file_content)} bytes"


@mcp.tool
async def get_user_quotas(
    client: StealthMoleClient = Depends(get_client),
) -> dict:
    """Get API usage quotas by service."""
    return await client.get_user_quotas()


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
