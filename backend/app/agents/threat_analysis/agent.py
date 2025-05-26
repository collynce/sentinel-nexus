import asyncio
import logging
from google.adk.agents import SequentialAgent, ParallelAgent
from app.services.adk_service import ADKService
from .sub_agents.discoverer.agent import create_discoverer_agent
from .sub_agents.scrape_website.agent import create_scrape_website_agent
from .sub_agents.search_news.agent import create_search_news_agent
from .sub_agents.monitor_social_media.agent import create_monitor_social_media_agent
from .sub_agents.synthesizer.agent import create_synthesizer_agent
from .sub_agents.threat_analysis.agent import create_threat_analysis_agent
from app.agents.threat_analysis.utils.mcp_init import (
    wait_for_initialization, 
    initialize_mcp_tools,
    get_agent_tools
)

MODEL = ADKService().get_litellm_model()

collector_agents = [
    create_scrape_website_agent(),
    create_search_news_agent(),
    create_monitor_social_media_agent(),
]

MCP_INIT_MSGS = [
    "Initializing discoverer tools. Please try your request again in a few moments.",
    "Initializing web scraping tools. Please try your request again in a few moments.",
    "Initializing news search tools. Please try your request again in a few moments.",
    "Initializing social media monitoring tools. Please try your request again in a few moments.",
]

async def run_with_mcp_retry(agent, ctx, max_retries=2):
    """Run agent with retry logic for MCP initialization."""
    for attempt in range(max_retries):
        # Ensure tools are assigned before running
        if hasattr(agent, 'tools'):
            agent_tools = get_agent_tools(agent.name)
            if not agent_tools:
                logging.warning(f"[MCP] No tools found for {agent.name}, waiting for initialization...")
                await wait_for_initialization()
                agent_tools = get_agent_tools(agent.name)
            agent.tools = agent_tools
            logging.info(f"[MCP] Assigned tools to {agent.name}: {[t.name for t in agent_tools]}")

        found_init_msg = False
        async for event in agent.run_async(ctx):
            content = getattr(event, 'content', None)
            if hasattr(event, "content") and isinstance(event.content, dict):
                if event.content.get("error") == "forbidden":
                    logging.warning(f"[MCP] Skipped forbidden/proxy-restricted site: {event.content.get('details')}")
                    continue
            if content and any(msg in str(content) for msg in MCP_INIT_MSGS):
                found_init_msg = True
                logging.info(f"[MCP] Found initialization message for {agent.name}, waiting for tools...")
                break
            yield event
        
        if found_init_msg:
            await wait_for_initialization()
            # Reassign tools after initialization
            if hasattr(agent, 'tools'):
                agent.tools = get_agent_tools(agent.name)
            continue
        break  # No init message, done
    else:
        raise RuntimeError(f"MCP tools did not initialize after {max_retries} retries for {agent.name}.")

class MCPSequentialAgent(SequentialAgent):
    """Sequential agent with MCP tool support."""
    
    async def _run_async_impl(self, ctx):
        """Run sub-agents sequentially with MCP tool support."""
        # Initialize tools for all agents first
        await ensure_tools_assigned(self)
        
        for sub_agent in self.sub_agents:
            if getattr(sub_agent, "name", "").endswith("Agent"):
                async for event in run_with_mcp_retry(sub_agent, ctx):
                    yield event
            else:
                async for event in sub_agent.run_async(ctx):
                    yield event

async def ensure_tools_assigned(root_agent):
    """Ensure all agents have their appropriate tools assigned."""
    try:
        tools = await initialize_mcp_tools()
        if not tools:
            raise RuntimeError("Failed to initialize MCP tools")
            
        logging.info(f"[TOOLS] Initialized {len(tools)} tools: {[t.name for t in tools]}")
        
        # Assign tools to each agent based on their name
        for agent in root_agent.sub_agents:
            if hasattr(agent, 'tools'):
                agent_tools = get_agent_tools(agent.name)
                if not agent_tools:
                    logging.warning(f"[TOOLS] No tools found for {agent.name}")
                    continue
                agent.tools = agent_tools
                logging.info(f"[TOOLS] Assigned tools to {agent.name}: {[t.name for t in agent_tools]}")
    except Exception as e:
        logging.error(f"[TOOLS] Error assigning tools: {str(e)}")
        raise

collector_parallel_agent = ParallelAgent(
    name="CollectorFanout",
    description="Runs all collectors in parallel with discoverer output.",
    sub_agents=[
        create_scrape_website_agent(),
        create_search_news_agent(),
        create_monitor_social_media_agent()
    ]
)

root_agent = MCPSequentialAgent(
    name="DataCollectionPipeline",
    description="Discovers, collects, and synthesizes web, news, and social media data for threat intelligence.",
    sub_agents=[
        create_discoverer_agent(),
        collector_parallel_agent,
        create_synthesizer_agent(),
        create_threat_analysis_agent()
    ]
) 

