import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from duckduckgo_search import DDGS


def web_search(query, max_results=3):
    """Search the web using DuckDuckGo and return results as text"""
    try:
        results_text = ""
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No web search results found."
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            body = result.get("body", "No content")
            href = result.get("href", "No link")
            results_text += f"\n**Result {i}: {title}**\n{body}\nSource: {href}\n"
        
        return results_text.strip()
    
    except Exception as e:
        return f"Web search failed: {str(e)}"


def should_use_web_search(query):
    """Decide if a query needs web search based on keywords"""
    try:
        web_keywords = [
            "latest", "recent", "current", "new", "today",
            "2024", "2025", "news", "update", "release",
            "who is", "what is happening", "trending"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in web_keywords)
    
    except Exception as e:
        return False