"""
Friday AI Agent — File Operations Tools
"""

import os
from langchain_core.tools import tool


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a file and return it as text.

    Args:
        file_path: Absolute or relative path to the file to read.
    """
    try:
        path = os.path.expanduser(file_path)
        if not os.path.exists(path):
            return f"Error: File '{file_path}' does not exist."
        if not os.path.isfile(path):
            return f"Error: '{file_path}' is not a file."

        # Limit to 10KB to avoid context overflow
        size = os.path.getsize(path)
        if size > 10240:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(10240)
            return f"(Showing first 10KB of {size} bytes)\n\n{content}"

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    except Exception as e:
        return f"Error reading file: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file. Creates the file if it doesn't exist.
    Creates parent directories if needed.

    Args:
        file_path: Absolute or relative path for the file.
        content: The text content to write into the file.
    """
    try:
        path = os.path.expanduser(file_path)
        # Create parent directories if they don't exist
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ Successfully wrote {len(content)} characters to '{file_path}'."

    except Exception as e:
        return f"Error writing file: {e}"


@tool
def list_directory(directory_path: str) -> str:
    """List all files and folders in a directory.

    Args:
        directory_path: Path to the directory to list. Use '.' for current directory.
    """
    try:
        path = os.path.expanduser(directory_path)
        if not os.path.exists(path):
            return f"Error: Directory '{directory_path}' does not exist."
        if not os.path.isdir(path):
            return f"Error: '{directory_path}' is not a directory."

        entries = sorted(os.listdir(path))
        if not entries:
            return f"Directory '{directory_path}' is empty."

        output_parts = []
        for entry in entries[:50]:  # Limit to 50 entries
            full = os.path.join(path, entry)
            if os.path.isdir(full):
                output_parts.append(f"📁 {entry}/")
            else:
                size = os.path.getsize(full)
                output_parts.append(f"📄 {entry} ({size} bytes)")

        result = "\n".join(output_parts)
        if len(entries) > 50:
            result += f"\n\n... and {len(entries) - 50} more items"
        return result

    except Exception as e:
        return f"Error listing directory: {e}"
