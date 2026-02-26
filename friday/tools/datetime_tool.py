"""
Friday AI Agent — Date & Time Tool
"""

from datetime import datetime
from langchain_core.tools import tool


@tool
def get_current_datetime() -> str:
    """Get the current date and time in a human-readable format.
    Use this when the user asks about the current time, date, or day.
    """
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_12 = now.strftime("%I:%M:%S %p")
    time_24 = now.strftime("%H:%M:%S")
    return f"Date: {date_str}\nTime: {time_12}\n24h: {time_24}"
