"""
Friday AI Agent — Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Settings ──────────────────────────────────────────────
# ── LLM Settings ──────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # 'gemini' or 'groq'
TEMPERATURE = 0.7

# Gemini Settings
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY = (
    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
)

# Groq Settings
GROQ_MODEL = "llama3-70b-8192"  # or "llama3-8b-8192" (faster)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Active Model Settings (Derived)
if LLM_PROVIDER == "groq":
    MODEL_NAME = GROQ_MODEL
    API_KEY = GROQ_API_KEY
else:
    MODEL_NAME = GEMINI_MODEL
    API_KEY = GEMINI_API_KEY

# ── Agent Settings ────────────────────────────────────────────
AGENT_NAME = "Friday"
MEMORY_WINDOW = 20  # number of past messages to keep in memory

# ── Voice Settings ────────────────────────────────────────────
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
TTS_VOICE_HINDI = "hi-IN-SwaraNeural"
TTS_VOICE_ENGLISH = "en-US-AriaNeural"
TTS_RATE = "+0%"  # Speech rate adjustment

# ── Safety Settings ───────────────────────────────────────────
# Commands that the system_cmd tool will NEVER execute
BLOCKED_COMMANDS = [
    "rm -rf",
    "format",
    "del /f /s /q",
    "mkfs",
    "dd if=",
    ":(){:|:&};:",
    "shutdown",
    "restart",
    "rmdir /s /q",
]

# Maximum time (seconds) a shell command can run
COMMAND_TIMEOUT = 30
