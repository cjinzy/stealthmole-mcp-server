"""StealthMole MCP Server implementation."""

import asyncio
import os
import sys
from typing import Any, Optional

from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)
from pydantic import AnyUrl

from .handlers import get_handler
from .schemas import TOOL_SCHEMAS
from .tools._request import init_config
from .utils.client import StealthMoleClient
from .utils.config import StealthMoleConfig

load_dotenv()

# Global client instance
client: Optional[StealthMoleClient] = None

# StealthMole Prompts based on prompt-eng.md
STEALTHMOLE_PROMPTS = """# Default Prompt

## Role

- Assistant for profilers to help analyze search results

## Default Behavior

- When limit is not specified, set it to 10
- Ask whether to search the next page and provide search results
- Provide results in markdown format
- Do not call API if there is no quota allocation
- Do not generate additional information such as evaluation, status, and recommendations
- Provide results organized in an easy-to-read format

# Each Function Prompt

## search_darkweb

- When searching in indicator:query format, search for various indicators in the dark web and provide results
- If the user does not specify an indicator, search with keyword
- All content searches use keyword
- Use indicator only for domain, file hash, and email format
- From the search results, conduct detailed node searches for all categories and analyze to provide answers to the user

## search_telegram

- When searching in indicator:query format, search for various indicators in Telegram and provide results
- If the user does not specify an indicator, search with keyword
- All content searches use keyword
- Use indicator only for domain, file hash, and email format
- From the search results, conduct detailed node searches for all categories and analyze to provide answers to the user

## Credential Leak Search

- search_credentials, search_compromised_dataset, search_combo_binder, search_ulp_binder

## Monitoring

- search_government_monitoring, search_leaked_monitoring, search_ransomware

## export_*

- If response_code is 422, guide the user to make a direct request

## get_user_quotas

- Only provide quota information to the user when the allowed value is greater than 0
- Do not provide quota information unrelated to API calls (SO, FF)
- Provide quota information in the following format:
  ```
  | service-name | Quota | Usage | Remaining |
  |--------------|-------|-------|-----------|
  | service-name | 1000  | 100 (10%) | 900 (90%) |
  ```
  """

server: Server = Server(
    "stealthmole-mcp",
    "250715",
)


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return []


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    raise ValueError(f"Unknown resource: {uri}")


@server.list_prompts()
async def handle_list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="stealthmole_default_prompt",
            description="Default behavior guidelines for StealthMole MCP",
            arguments=[
                PromptArgument(
                    name="context",
                    description="Current search context",
                    required=False,
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    """Get a specific prompt."""
    if name == "stealthmole_default_prompt":
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="assistant",
                    content=TextContent(type="text", text=STEALTHMOLE_PROMPTS),
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available StealthMole tools."""
    try:
        print("Returning StealthMole tools list", file=sys.stderr)
        return [Tool(**schema) for schema in TOOL_SCHEMAS]
    except Exception as e:
        print(f"Error in handle_list_tools: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return []


def apply_default_behavior(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Apply default behavior rules to tool arguments."""
    # Always set limit to maximum value
    if "limit" in arguments:
        arguments["limit"] = 50

    # Handle indicator defaults for search tools
    if name in ["search_darkweb", "search_telegram"]:
        if "indicator" not in arguments or not arguments["indicator"]:
            arguments["indicator"] = "keyword"

    return arguments


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls with default behavior applied."""
    global client

    if client is None:
        return [
            TextContent(
                type="text",
                text="Error: StealthMole client not initialized. Please check your API credentials.",
            )
        ]

    # Apply default behavior rules
    arguments = apply_default_behavior(name, arguments)

    try:
        # Get the handler for this tool
        handler = get_handler(name)
        if handler is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        # Special handling for download_file which returns bytes
        if name == "download_file":
            file_content = await handler(client, arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Downloaded file {arguments['file_hash']} from {arguments['service']} service. File size: {len(file_content)} bytes",
                )
            ]

        # Execute the handler
        result = await handler(client, arguments)

        # Format response
        response_text = f"StealthMole API Results:{result}"
        return [TextContent(type="text", text=response_text)]

    except asyncio.TimeoutError:
        return [
            TextContent(
                type="text",
                text="Request timed out. The API request took too long to complete.",
            )
        ]
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return [
                TextContent(
                    type="text",
                    text=f"Timeout error: {error_msg}. Try reducing the result limit or check your network connection.",
                )
            ]
        return [
            TextContent(
                type="text",
                text=f"Error calling StealthMole API: {error_msg}",
            )
        ]


async def run_server():
    """Run the MCP server."""
    global client

    try:
        print("Starting StealthMole MCP server...", file=sys.stderr)

        # Initialize StealthMole client
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
        else:
            try:
                config = StealthMoleConfig(access_key=access_key, secret_key=secret_key)
                print("StealthMole config created", file=sys.stderr)

                # Initialize the config singleton for _request module
                init_config(config)

                client = StealthMoleClient(config)
                print("StealthMole client initialized", file=sys.stderr)

                # API connection test
                try:
                    quotas = await client.get_user_quotas()
                    print(
                        f"API connection successful. Available quotas: {quotas}",
                        file=sys.stderr,
                    )
                except Exception as api_error:
                    print(f"Warning: API test failed: {api_error}", file=sys.stderr)
                    print("Continuing with server startup...", file=sys.stderr)

            except Exception as e:
                print(
                    f"Warning: Error creating StealthMole client: {e}", file=sys.stderr
                )
                print(
                    "MCP server will start but tools may not function properly",
                    file=sys.stderr,
                )
                import traceback

                traceback.print_exc(file=sys.stderr)

        print("Creating stdio server...", file=sys.stderr)
        async with stdio_server() as (read_stream, write_stream):
            print("Starting MCP server...", file=sys.stderr)
            try:
                await server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="stealthmole-mcp",
                        server_version="0.1.0",
                        capabilities=server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
                print("MCP server completed normally", file=sys.stderr)
            except Exception as e:
                print(f"Error in MCP server.run: {e}", file=sys.stderr)
                import traceback

                traceback.print_exc(file=sys.stderr)
                raise
    except Exception as e:
        print(f"Error in run_server: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)


def main():
    """Main entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
