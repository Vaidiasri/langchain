"""
Friday AI Agent — Core Agent Brain
Uses LangChain ReAct agent with Gemini Flash and custom tools.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from config import (
    MODEL_NAME,
    TEMPERATURE,
    API_KEY,
    AGENT_NAME,
    MEMORY_WINDOW,
    LLM_PROVIDER,
    GROQ_API_KEY,
)
from prompts import FRIDAY_SYSTEM_PROMPT

# Import all tools
from tools.web_search import web_search
from tools.file_ops import read_file, write_file, list_directory
from tools.system_cmd import run_command
from tools.calculator import calculator
from tools.datetime_tool import get_current_datetime
from tools.reminder import set_reminder


def get_all_tools():
    """Return a list of all available tools for the agent."""
    return [
        web_search,
        read_file,
        write_file,
        list_directory,
        run_command,
        calculator,
        get_current_datetime,
        set_reminder,
    ]


def create_friday_agent():
    """Create and return the Friday AI agent with all tools.

    Returns:
        A tuple of (llm, tools, chat_history) for the conversation loop.
    """
    tools = get_all_tools()

    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq

        if not GROQ_API_KEY:
            raise SystemExit(
                "❌ Missing GROQ_API_KEY! Get one from console.groq.com and set it in your .env file."
            )

        print(f"  🚀 Using Groq (Llama 3) - Model: {MODEL_NAME}")
        llm = ChatGroq(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            api_key=GROQ_API_KEY,
        )
    else:
        # Default to Gemini
        if not API_KEY:
            raise SystemExit(
                "❌ Missing GEMINI_API_KEY! Set GOOGLE_API_KEY or API_KEY in your .env file."
            )

        print(f"  ✨ Using Gemini - Model: {MODEL_NAME}")
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            api_key=API_KEY,
        )

    # Bind tools to the LLM so it can call them
    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools, tools


def build_messages(chat_history: list, user_input: str) -> list:
    """Build the messages list including system prompt, history, and new input.

    Args:
        chat_history: List of previous (HumanMessage, AIMessage) pairs.
        user_input: The current user message.

    Returns:
        List of messages to send to the LLM.
    """
    messages = [SystemMessage(content=FRIDAY_SYSTEM_PROMPT)]

    # Add chat history (limited to MEMORY_WINDOW messages)
    recent_history = chat_history[-(MEMORY_WINDOW * 2) :]
    messages.extend(recent_history)

    # Add current user message
    messages.append(HumanMessage(content=user_input))

    return messages


def _invoke_with_retry(llm, messages, max_retries=3):
    """Invoke LLM with retry logic for rate limits."""
    import time
    import re

    for attempt in range(max_retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                # Extract retry delay if available
                match = re.search(r"retryDelay.*?(\d+)", err_msg)
                wait_time = int(match.group(1)) if match else (10 * (attempt + 1))
                print(
                    f"  ⏳ Rate limited. Waiting {wait_time}s before retry ({attempt + 1}/{max_retries})..."
                )
                time.sleep(wait_time)
            else:
                raise
    # Final attempt without catching
    return llm.invoke(messages)


def process_response(llm_with_tools, messages: list, tools: list) -> str:
    """Send messages to the LLM, handle tool calls, and return final response.

    Args:
        llm_with_tools: The LLM with tools bound.
        messages: Full message list to send.
        tools: List of available tools.

    Returns:
        The final text response from the agent.
    """
    import time

    # Create a tool lookup dictionary
    tool_map = {t.name: t for t in tools}

    # First LLM call with retry for rate limits
    response = _invoke_with_retry(llm_with_tools, messages)

    # Keep processing while the LLM wants to call tools
    max_iterations = 10
    iteration = 0

    while response.tool_calls and iteration < max_iterations:
        iteration += 1

        # Add the AI response (with tool calls) to messages
        messages.append(response)

        # Execute each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"  🔧 Using tool: {tool_name}...")

            if tool_name in tool_map:
                try:
                    tool_result = tool_map[tool_name].invoke(tool_args)
                except Exception as e:
                    tool_result = f"Tool error: {e}"
            else:
                tool_result = f"Unknown tool: {tool_name}"

            # Add tool result as a ToolMessage
            from langchain_core.messages import ToolMessage

            messages.append(
                ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])
            )

        # Call LLM again with tool results
        response = _invoke_with_retry(llm_with_tools, messages)

    return _extract_text(response.content)


def _extract_text(content) -> str:
    """Extract plain text from LLM response content.

    Gemini with tool binding may return content as:
    - A plain string
    - A list of dicts like [{'type': 'text', 'text': '...'}, ...]
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts) if parts else str(content)
    return str(content)
