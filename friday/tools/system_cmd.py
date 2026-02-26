"""
Friday AI Agent — System Command Tool
"""

import subprocess
from langchain_core.tools import tool

# Import from a relative path — config is one level up
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import BLOCKED_COMMANDS, COMMAND_TIMEOUT


@tool
def run_command(command: str) -> str:
    """Run a shell command on the system and return its output.
    Use this for system tasks like checking disk space, opening apps,
    listing processes, or any other terminal command.

    SAFETY: Destructive commands are blocked automatically.

    Args:
        command: The shell command to run (e.g., 'dir', 'ipconfig', 'python --version').
    """
    # Safety check — block destructive commands
    cmd_lower = command.lower().strip()
    for blocked in BLOCKED_COMMANDS:
        if blocked.lower() in cmd_lower:
            return f"🚫 Blocked: The command contains '{blocked}' which is not allowed for safety reasons."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
            cwd=os.path.expanduser("~"),
        )

        output = ""
        if result.stdout:
            output += result.stdout.strip()
        if result.stderr:
            if output:
                output += "\n\n--- STDERR ---\n"
            output += result.stderr.strip()

        if not output:
            output = "(Command completed with no output)"

        # Truncate very long output
        if len(output) > 3000:
            output = output[:3000] + "\n\n... (output truncated)"

        return output

    except subprocess.TimeoutExpired:
        return f"⏰ Command timed out after {COMMAND_TIMEOUT} seconds."
    except Exception as e:
        return f"Error running command: {e}"
