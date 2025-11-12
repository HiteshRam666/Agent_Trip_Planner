import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

class PlaceSearchTool:
    def __init__(self):
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools() 

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_attractions(place) 
            except Exception as e:
                return f"Cannot find details: {e}"
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of place"""
            try:
                tavily_result = self.tavily_search.tavily_search_activity(place) 
            except Exception as e:
                return f"Cannot find details: {e}"
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
            except Exception as e:
                return f"Cannot find details: {e}"

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
            except Exception as e:
                return f"Cannot find details: {e}"

        return [search_activities, search_transportation, search_attractions, search_restaurants]            