"""
🤖 Friday — Your Bilingual AI Assistant
Speaks Hindi & English | Executes Tasks | Powered by Gemini + LangChain

Usage:
    python friday.py              # Text mode (default)
    python friday.py --mode voice # Voice mode (requires mic)
    python friday.py --mode hybrid  # Type input, get voice output
"""

import argparse
import sys
import os

# Ensure the friday package directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import create_friday_agent, build_messages, process_response
from config import AGENT_NAME, WHISPER_MODEL
from langchain_core.messages import HumanMessage, AIMessage


# ── Banner ────────────────────────────────────────────────────
BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗            ║
║     ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝            ║
║     █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝             ║
║     ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝              ║
║     ██║     ██║  ██║██║██████╔╝██║  ██║   ██║               ║
║     ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝               ║
║                                                              ║
║     🤖 Your Bilingual AI Assistant                           ║
║     🗣️  Hindi + English | 🔧 Task Execution                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
Commands:
  /exit, /quit  — Exit Friday
  /reset        — Clear conversation history
  /voice        — Switch to voice input mode
  /text         — Switch to text input mode
  /tools        — List available tools
  /help         — Show this help message
"""


def list_tools_info():
    """Display available tools."""
    print("\n🔧 Available Tools:")
    print("  1. 🌐 web_search     — Search the web (DuckDuckGo)")
    print("  2. 📄 read_file      — Read file contents")
    print("  3. ✏️  write_file     — Create/write files")
    print("  4. 📁 list_directory — List folder contents")
    print("  5. 💻 run_command    — Execute shell commands")
    print("  6. 🔢 calculator     — Math calculations")
    print("  7. 📅 get_current_datetime — Current date & time")
    print("  8. ⏰ set_reminder   — Set timed reminders")
    print()


def get_voice_input() -> str:
    """Get input via voice (microphone + Whisper)."""
    try:
        from voice.stt import listen_and_transcribe, is_whisper_available

        if not is_whisper_available():
            print("  ⚠️  Voice dependencies not installed.")
            print("  Run: pip install openai-whisper SpeechRecognition PyAudio")
            return ""

        text, lang = listen_and_transcribe(WHISPER_MODEL)
        if text:
            print(f"  📝 You said: {text}")
            if lang != "en":
                print(f"  🌐 Language: {lang}")
        return text

    except Exception as e:
        print(f"  ❌ Voice error: {e}")
        return ""


def speak_response(text: str):
    """Speak the response aloud using TTS."""
    try:
        from voice.tts import speak

        speak(text)
    except ImportError:
        print("  ⚠️  TTS requires: pip install edge-tts pygame langdetect")
    except Exception as e:
        print(f"  ❌ TTS error: {e}")


def main():
    """Main entry point for Friday."""
    parser = argparse.ArgumentParser(description="Friday — Bilingual AI Assistant")
    parser.add_argument(
        "--mode",
        choices=["text", "voice", "hybrid"],
        default="text",
        help="Input mode: text (default), voice (mic input + voice output), hybrid (text input + voice output)",
    )
    args = parser.parse_args()

    # Show banner
    print(BANNER)
    print(f"  Mode: {args.mode.upper()} | Type /help for commands\n")

    # Initialize the agent
    try:
        llm_with_tools, tools = create_friday_agent()
    except SystemExit as e:
        print(f"\n{e}")
        return 1

    print(f"  ✅ {AGENT_NAME} is ready! Let's go.\n")

    # Conversation history
    chat_history: list = []
    current_mode = args.mode

    # Main loop
    while True:
        try:
            # Get input based on mode
            if current_mode == "voice":
                user_input = get_voice_input()
                if not user_input:
                    continue
            else:
                user_input = input(f"You: ").strip()

        except (EOFError, KeyboardInterrupt):
            print(f"\n\n👋 Bye! — {AGENT_NAME}")
            return 0

        if not user_input:
            continue

        # Handle commands
        cmd = user_input.lower().strip()
        if cmd in {"/exit", "/quit"}:
            print(f"\n👋 Bye! — {AGENT_NAME}")
            return 0
        elif cmd == "/reset":
            chat_history.clear()
            print("  🔄 Conversation history cleared.\n")
            continue
        elif cmd == "/voice":
            current_mode = "voice"
            print("  🎤 Switched to VOICE mode. Speak into your mic!\n")
            continue
        elif cmd == "/text":
            current_mode = "text"
            print("  ⌨️  Switched to TEXT mode.\n")
            continue
        elif cmd == "/hybrid":
            current_mode = "hybrid"
            print("  🔀 Switched to HYBRID mode (text in, voice out).\n")
            continue
        elif cmd == "/tools":
            list_tools_info()
            continue
        elif cmd == "/help":
            print(HELP_TEXT)
            continue

        # Build messages and get response
        messages = build_messages(chat_history, user_input)

        try:
            print(f"\n{AGENT_NAME}: ", end="", flush=True)
            response_text = process_response(llm_with_tools, messages, tools)
            print(response_text)

            # Update chat history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response_text))

            # Speak response in voice or hybrid mode
            if current_mode in ("voice", "hybrid") and response_text:
                speak_response(response_text)

        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            # Don't add failed exchanges to history

        print()  # Blank line between exchanges


if __name__ == "__main__":
    raise SystemExit(main())
