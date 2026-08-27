import os
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load .env
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
load_dotenv(dotenv_path=current_dir / ".env")
load_dotenv(dotenv_path=root_dir / ".env")
load_dotenv()


def search_with_tavily(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Searches using the Tavily AI Search API (designed for LLM grounding).
    """
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key or api_key.startswith("your_"):
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "max_results": max_results,
    }

    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code == 200:
            data = response.json()
            sources = []
            for item in data.get("results", []):
                sources.append({
                    "title": item.get("title", "No Title"),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", "")[:350],  # Keep concise for prompt
                })
            return sources
    except Exception as e:
        print(f"[Warning] Tavily search error: {e}")

    return []


def search_with_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Free fallback search using DuckDuckGo (no API key required).
    """
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))
            sources = []
            for r in raw_results:
                sources.append({
                    "title": r.get("title", "Web Source"),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:350],
                })
            return sources
    except Exception as e:
        print(f"[Warning] DuckDuckGo search fallback error: {e}")

    return []


def search_with_wikipedia(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Reliable Wikipedia REST API search fallback for encyclopedia facts.
    """
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&utf8=&format=json"
        headers = {"User-Agent": "FactCheckingApp/1.0 (hackathon-project)"}
        resp = requests.get(search_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            search_items = data.get("query", {}).get("search", [])[:max_results]
            sources = []
            for item in search_items:
                title = item.get("title", "")
                pageid = item.get("pageid", "")
                snippet = item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                sources.append({
                    "title": f"Wikipedia: {title}",
                    "url": f"https://en.wikipedia.org/?curid={pageid}",
                    "snippet": snippet,
                })
            return sources
    except Exception as e:
        print(f"[Warning] Wikipedia search fallback error: {e}")

    return []


def search_evidence(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Main evidence retrieval function.
    Order of priority:
    1. Tavily API (if TAVILY_API_KEY is configured in .env)
    2. DuckDuckGo (free, live web results)
    3. Wikipedia Search API (encyclopedic fallback)
    """
    # 1. Try Tavily if configured
    sources = search_with_tavily(query, max_results=max_results)
    if sources:
        return sources

    # 2. Try DuckDuckGo
    sources = search_with_duckduckgo(query, max_results=max_results)
    if sources:
        return sources

    # 3. Try Wikipedia
    sources = search_with_wikipedia(query, max_results=max_results)
    if sources:
        return sources

    return []
