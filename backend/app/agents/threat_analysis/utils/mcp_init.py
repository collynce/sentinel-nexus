import asyncio
import logging
from google.genai.errors import ServerError

async def call_with_retries(api_call_fn, *args, max_retries=3, base_delay=2, **kwargs):
    """
    Calls an async API function with retries and exponential backoff on ServerError.
    Args:
        api_call_fn: The async function to call (e.g., your Google GenAI API call)
        *args, **kwargs: Arguments to pass to the function
        max_retries: Maximum number of attempts
        base_delay: Initial delay (seconds) for exponential backoff
    Returns:
        The result of the API call if successful.
    Raises:
        The last ServerError if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            return await api_call_fn(*args, **kwargs)
        except ServerError as e:
            logging.warning(f"[GENAI] ServerError (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
            else:
                logging.error("[GENAI] Max retries exceeded. Raising error.")
                raise
        except Exception as e:
            # Handle non-server errors immediately
            logging.error(f"[GENAI] Unexpected error: {e}")
            raise

import asyncio
import logging
import atexit
from contextlib import AsyncExitStack
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseServerParams
from google.genai import types
from google.adk.models import LlmResponse
from app.core.config import settings

logging.basicConfig(
    filename="mcp.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Global state
_mcp_tools = None
_exit_stack = None
_initialized = False
_init_lock = asyncio.Lock()

# Tool name mapping
TOOL_NAME_MAP = {
    "discoverer_agent": "DiscovererAgent",
    "scrape_website_agent": "ScrapeWebsiteAgent",
    "search_news_agent": "SearchNewsAgent",
    "monitor_social_media_agent": "MonitorSocialMediaAgent",
}

# Agent to tool mapping
AGENT_TOOL_MAP = {
    "DiscovererAgent": ["discoverer_agent"],
    "ScrapeWebsiteAgent": ["scrape_website_agent"],
    "SearchNewsAgent": ["search_news_agent"],
    "MonitorSocialMediaAgent": ["monitor_social_media_agent"],
}


async def initialize_mcp_tools():
    """
    Initialize the MCP toolset once, ensuring proper async locking and cleanup.
    Returns a list of MCPTool instances.
    """
    global _mcp_tools, _exit_stack, _initialized
    common_exit_stack = AsyncExitStack()

    # Ensure single initialization
    async with _init_lock:
        if _initialized:
            logging.info("[MCP] Tools already initialized")
            return _mcp_tools

        # Prepare connection parameters
        # params = StdioServerParameters(
        #     command="npx",
        #     args=[
        #         "-y",
        #         "@smithery/cli@latest",
        #         "run",
        #         "@luminati-io/brightdata-mcp",
        #         "--key",
        #         "2a899f48-758d-4708-b9f8-f902b9c1d12d",
        #         "--profile",
        #         "creepy-mite-R4PydJ",
        #         "--config",
        #         "'{\"apiToken\": \"e1f91a59-1882-4423-aa9a-bb8ea5acf9ab\", \"browserAuth\": \"brd-customer-hl_8dd765c6-zone-scraping_browser1:vc8nqa5uzq3d\", \"webUnlockerZone\": \"unblocker\"}'",
        #     ],
        # )
        params = SseServerParams(
            url="http://127.0.0.1:6969/sse",
            env={
                "API_TOKEN": settings.BRIGHT_DATA_API_KEY,
                "WEB_UNLOCKER_ZONE": settings.WEB_UNLOCKER_ZONE,
                "BROWSER_AUTH": settings.BROWSER_AUTH
            },
            async_exit_stack=common_exit_stack
        )

        try:
            # Connect and obtain tools + exit stack
            tools, exit_stack = await MCPToolset.from_server(connection_params=params)

            # Verify all required tools are present
            tool_names = {t.name for t in tools}
            required_tools = set(TOOL_NAME_MAP.keys())
            missing_tools = required_tools - tool_names

            # if missing_tools:
            # raise RuntimeError(f"Missing required tools: {missing_tools}")

            logging.info(
                f"[MCP] Initialized {len(tools)} tools: {[t.name for t in tools]}"
            )

            # Register cleanup for exit_stack
            async def _cleanup():
                await common_exit_stack.aclose()
                logging.info("[MCP] Cleaned up MCP connection")

            # Ensure cleanup runs on process exit
            atexit.register(lambda: asyncio.run(_cleanup()))

            _mcp_tools = tools
            _exit_stack = common_exit_stack
            _initialized = True
            return _mcp_tools

        except Exception as e:
            logging.error(f"[MCP] Failed to initialize tools: {str(e)}")
            raise


async def wait_for_initialization():
    """Ensure MCP tools are initialized."""
    if not _initialized:
        await initialize_mcp_tools()
    return _initialized


def get_agent_tools(agent_name):
    """Get the specific tools for a given agent."""
    if not _initialized or not _mcp_tools:
        return []

    return _mcp_tools


def _create_checker(agent_name):
    def checker(callback_context, llm_request):
        global _mcp_tools, _initialized
        current = getattr(callback_context, "agent_name", None)
        agent = getattr(callback_context, "agent", None)

        if current == agent_name and not _initialized:
            asyncio.create_task(initialize_mcp_tools())
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text=f"Initializing {agent_name} tools. Try again shortly."
                        )
                    ],
                )
            )

        if _initialized and agent and agent.tools is None:
            # Get specific tools for this agent
            agent_tools = get_agent_tools(agent_name)
            if agent_tools:
                agent.tools = agent_tools
                logging.info(
                    f"[MCP] Assigned tools to {agent_name}: {[t.name for t in agent_tools]}"
                )

        return None

    return checker


check_mcp_tools = _create_checker(None)
check_scrape_website_tools = _create_checker("ScrapeWebsiteAgent")
check_search_news_tools = _create_checker("SearchNewsAgent")
check_monitor_social_media_tools = _create_checker("MonitorSocialMediaAgent")
check_discoverer_tools = _create_checker("DiscovererAgent")


from mcp.shared.exceptions import McpError

async def safe_tool_call(tool, *args, **kwargs):
    try:
        return await tool(*args, **kwargs)
    except McpError as e:
        msg = str(e)
        if any(keyword in msg for keyword in ["KYC", "Forbidden", "proxy_error"]):
            logging.warning(f"[MCP] Skipping forbidden site/tool: {msg}")
            return {
                "error": "forbidden",
                "message": "Site is restricted or requires special permissions (KYC/proxy). Skipping.",
                "details": msg,
            }
        raise

__all__ = [
    "initialize_mcp_tools",
    "wait_for_initialization",
    "safe_tool_call",
    "check_mcp_tools",
    "check_scrape_website_tools",
    "check_search_news_tools",
    "check_monitor_social_media_tools",
    "check_discoverer_tools",
    "get_agent_tools",
]
