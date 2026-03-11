from langchain_community.tools import DuckDuckGoSearchRun

# Create the tool instance with specific name to match prompts
web_search = DuckDuckGoSearchRun(
    name="web_search",
    description="Search the web for current information, news, facts, or anything you're not sure about."
)

# The variable name 'web_search' is used in agent.py imports.
