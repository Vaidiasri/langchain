"""
Friday AI Agent — Text-to-Speech using Edge-TTS (free, high quality)
"""

import asyncio
import os
import tempfile

# Import config from parent
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import TTS_VOICE_HINDI, TTS_VOICE_ENGLISH, TTS_RATE


def detect_language(text: str) -> str:
    """Detect whether text is Hindi or English.

    Returns:
        'hi' for Hindi, 'en' for English.
    """
    try:
        from langdetect import detect

        lang = detect(text)
        return "hi" if lang == "hi" else "en"
    except Exception:
        return "en"


async def _generate_speech(text: str, voice: str, output_path: str):
    """Generate speech audio file using Edge-TTS.

    Args:
        text: The text to speak.
        voice: The Edge-TTS voice name.
        output_path: Path to save the audio file.
    """
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=TTS_RATE)
    await communicate.save(output_path)


def speak(text: str, force_language: str = None):
    """Convert text to speech and play it.

    Args:
        text: The text to speak aloud.
        force_language: Force 'hi' or 'en'. If None, auto-detects.
    """
    try:
        import edge_tts
    except ImportError:
        print("  ⚠️  TTS requires: pip install edge-tts")
        return

    # Detect language and pick appropriate voice
    lang = force_language or detect_language(text)
    voice = TTS_VOICE_HINDI if lang == "hi" else TTS_VOICE_ENGLISH

    # Generate audio to temp file
    tmp_path = os.path.join(tempfile.gettempdir(), "friday_tts.mp3")

    try:
        asyncio.run(_generate_speech(text, voice, tmp_path))
    except RuntimeError:
        # If there's already an event loop (e.g., in Jupyter), use nest_asyncio pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_generate_speech(text, voice, tmp_path))
        loop.close()

    # Play the audio
    _play_audio(tmp_path)


def _play_audio(file_path: str):
    """Play an audio file using pygame or playsound as fallback."""
    try:
        import pygame

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
    except ImportError:
        try:
            from playsound import playsound

            playsound(file_path)
        except ImportError:
            print("  ⚠️  Audio playback requires: pip install pygame")
    except Exception as e:
        print(f"  ❌ Audio playback error: {e}")
    finally:
        # Clean up temp file
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass
