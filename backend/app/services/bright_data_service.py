import json
from typing import Dict, List, Optional, Any, Union
import asyncio
import aiohttp
from loguru import logger

from app.core.config import settings


class BrightDataService:
    """Service for interacting with Bright Data APIs"""
    
    def __init__(self):
        """Initialize the Bright Data service with API credentials"""
        self.api_key = settings.BRIGHT_DATA_API_KEY
        self.username = settings.BRIGHT_DATA_USERNAME
        self.password = settings.BRIGHT_DATA_PASSWORD
        self.base_url = "https://brightdata.com/api"
        
        # Check if credentials are configured
        if not self.api_key:
            logger.warning("Bright Data API key not configured")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Bright Data API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Add authentication headers
        _headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if headers:
            _headers.update(headers)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=_headers,
                    ssl=True,
                ) as response:
                    response_data = await response.json()
                    
                    if response.status >= 400:
                        logger.error(f"Bright Data API error: {response.status} - {response_data}")
                        return {"error": response_data, "status_code": response.status}
                    
                    return response_data
        except Exception as e:
            logger.error(f"Error making request to Bright Data API: {str(e)}")
            return {"error": str(e)}
    
    # Web Scraper API methods
    
    async def scrape_website(self, url: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Scrape a website using Bright Data's Web Scraper API"""
        endpoint = "web_scraper/scrape"
        
        data = {
            "url": url,
        }
        
        if options:
            data.update(options)
        
        return await self._make_request("POST", endpoint, data=data)
    
    async def get_pre_built_collector(self, domain: str) -> Dict[str, Any]:
        """Get information about a pre-built collector for a specific domain"""
        endpoint = f"web_scraper/collectors/{domain}"
        return await self._make_request("GET", endpoint)
    
    async def run_pre_built_collector(
        self, 
        domain: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run a pre-built collector for a specific domain"""
        endpoint = f"web_scraper/collectors/{domain}/run"
        return await self._make_request("POST", endpoint, data=params)
    
    # Web Unlocker API methods
    
    async def create_unlocker_session(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Web Unlocker session"""
        endpoint = "web_unlocker/sessions"
        return await self._make_request("POST", endpoint, data=options)
    
    async def navigate_with_unlocker(
        self, 
        session_id: str, 
        url: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Navigate to a URL using a Web Unlocker session"""
        endpoint = f"web_unlocker/sessions/{session_id}/navigate"
        
        data = {
            "url": url,
        }
        
        if options:
            data.update(options)
        
        return await self._make_request("POST", endpoint, data=data)
    
    # Proxy API methods
    
    async def get_proxy_session(self, zone: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a proxy session for a specific zone"""
        endpoint = f"proxy/{zone}/session"
        return await self._make_request("POST", endpoint, data=options)
    
    # MCP Server methods
    
    async def mcp_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a query on the MCP Server"""
        endpoint = "mcp/query"
        
        data = {
            "query": query,
        }
        
        if params:
            data["params"] = params
        
        return await self._make_request("POST", endpoint, data=data)
    
    # Convenience methods for specific data sources
    
    async def get_news_articles(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get news articles related to cybersecurity threats"""
        try:
            # Use pre-built news collectors
            news_sources = ["thehackernews", "bleepingcomputer", "threatpost"]
            results = []
            
            for source in news_sources:
                response = await self.run_pre_built_collector(source, {"query": query, "limit": limit})
                if "error" not in response:
                    results.extend(response.get("results", []))
            
            return results[:limit]
        except Exception as e:
            logger.error(f"Error fetching news articles: {str(e)}")
            return []
    
    async def get_social_media_posts(self, query: str, platform: str = "twitter", limit: int = 10) -> List[Dict[str, Any]]:
        """Get social media posts related to cybersecurity threats"""
        try:
            response = await self.run_pre_built_collector(platform, {"query": query, "limit": limit})
            if "error" not in response:
                return response.get("results", [])
            return []
        except Exception as e:
            logger.error(f"Error fetching social media posts: {str(e)}")
            return []
    
    async def get_dark_web_content(self, forum: str, query: str) -> List[Dict[str, Any]]:
        """Get content from dark web forums related to cybersecurity threats"""
        try:
            # Create a Web Unlocker session
            session_response = await self.create_unlocker_session({"browser": "chrome"})
            
            if "error" in session_response:
                return []
            
            session_id = session_response.get("session_id")
            
            # Navigate to the forum
            navigate_response = await self.navigate_with_unlocker(
                session_id, 
                f"http://{forum}.onion", 
                {"wait_for": "networkidle"}
            )
            
            if "error" in navigate_response:
                return []
            
            # This is a simplified example - in a real implementation, 
            # we would need to handle login, navigation, and content extraction
            
            # For now, return a placeholder
            return [{"source": forum, "content": "Example dark web content"}]
        except Exception as e:
            logger.error(f"Error fetching dark web content: {str(e)}")
            return []
