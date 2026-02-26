"""
Friday AI Agent — Web Search Tool (DuckDuckGo)
"""

from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the web for current information using DuckDuckGo.
    Use this for news, facts, weather, general knowledge, or anything
    you're not sure about. Returns top 3 results with snippets.

    Args:
        query: The search query string.
    """
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No results found for that query."

        output_parts = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            body = r.get("body", "No description")
            href = r.get("href", "")
            output_parts.append(f"{i}. **{title}**\n   {body}\n   🔗 {href}")

        return "\n\n".join(output_parts)

    except ImportError:
        return "Error: duckduckgo-search is not installed. Run: pip install duckduckgo-search"
    except Exception as e:
        return f"Search failed: {e}"
