# Tools for Data Collection Agent

from app.services.adk_service import ADKService

adk_service = ADKService()
scrape_website_tool = adk_service._scrape_website_tool
search_news_tool = adk_service._search_news_tool
monitor_social_media_tool = adk_service._monitor_social_media_tool
