"""
Friday AI Agent — Speech-to-Text using OpenAI Whisper (local, offline)
"""

import os
import tempfile


def is_whisper_available() -> bool:
    """Check if Whisper and audio recording dependencies are available."""
    try:
        import whisper
        import speech_recognition as sr

        return True
    except ImportError:
        return False


def listen_and_transcribe(whisper_model_size: str = "base") -> tuple[str, str]:
    """Record audio from microphone and transcribe using Whisper.

    Args:
        whisper_model_size: Whisper model size (tiny, base, small, medium, large).

    Returns:
        A tuple of (transcribed_text, detected_language).
        Returns ("", "") if recording fails.
    """
    try:
        import whisper
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        # Adjust for ambient noise and record
        print("  🎤 Listening... (speak now, stay silent to stop)")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)

        print("  ⏳ Transcribing...")

        # Save audio to a temporary WAV file for Whisper
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio.get_wav_data())
            tmp_path = tmp.name

        try:
            # Load Whisper model (cached after first load)
            model = whisper.load_model(whisper_model_size)

            # Transcribe with language detection
            result = model.transcribe(tmp_path)
            text = result.get("text", "").strip()
            language = result.get("language", "en")

            return text, language
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except ImportError:
        print(
            "  ⚠️  Voice input requires: pip install openai-whisper SpeechRecognition PyAudio"
        )
        return "", ""
    except Exception as e:
        print(f"  ❌ Voice input error: {e}")
        return "", ""
