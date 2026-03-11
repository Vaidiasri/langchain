"""
Friday AI Agent — Custom Multiplication Tool
"""

from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together and return the result.
    
    Args:
        a: First number.
        b: Second number.
    """
    return a * b
