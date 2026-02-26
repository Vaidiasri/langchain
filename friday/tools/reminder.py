"""
Friday AI Agent — Reminder Tool (in-memory)
"""

import threading
from langchain_core.tools import tool

# Store active reminders for display
_active_reminders: list[dict] = []


def _reminder_callback(message: str):
    """Called when a reminder fires."""
    print(f"\n\n🔔 ━━━ REMINDER ━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   {message}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


@tool
def set_reminder(message: str, minutes: int) -> str:
    """Set a reminder that will alert after the specified number of minutes.
    The reminder will print a notification in the console.

    Args:
        message: The reminder message (e.g., 'Call Mom', 'Meeting starts').
        minutes: Number of minutes from now to trigger the reminder.
    """
    if minutes <= 0:
        return "Error: Minutes must be a positive number."
    if minutes > 1440:
        return "Error: Maximum reminder time is 24 hours (1440 minutes)."

    seconds = minutes * 60
    timer = threading.Timer(seconds, _reminder_callback, args=[message])
    timer.daemon = True  # Don't keep the program alive just for reminders
    timer.start()

    _active_reminders.append({"message": message, "minutes": minutes})

    if minutes == 1:
        return f'⏰ Reminder set! I\'ll remind you in 1 minute: "{message}"'
    else:
        return f'⏰ Reminder set! I\'ll remind you in {minutes} minutes: "{message}"'
