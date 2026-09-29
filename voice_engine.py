import os
import io
import wave
from pathlib import Path
from typing import Optional, Tuple

VOICE_DIR = Path(os.getenv("LUNARIS_VOICE_DIR", "./voice_cache"))
VOICE_DIR.mkdir(parents=True, exist_ok=True)

class LunarisVoiceEngine:
    """
    Air-gapped voice engine for Lunaris AI.
    Provides local Speech-to-Text (Whisper) and Text-to-Speech (Offline TTS).
    """
    def __init__(self, whisper_model_size: str = "base"):
        self.whisper_model_size = whisper_model_size
        self._stt_model = None
        self._tts_engine = None

    def _get_stt_model(self):
        """Lazy load local Whisper model."""
        if self._stt_model is None:
            try:
                from faster_whisper import WhisperModel
                print(f"[Voice] Loading local faster-whisper model ({self.whisper_model_size})...")
                self._stt_model = WhisperModel(self.whisper_model_size, device="cpu", compute_type="int8")
            except ImportError:
                try:
                    import whisper
                    print(f"[Voice] Loading local openai-whisper model ({self.whisper_model_size})...")
                    self._stt_model = whisper.load_model(self.whisper_model_size)
                except ImportError:
                    print("[Voice Warning] Neither 'faster-whisper' nor 'whisper' installed. Audio transcription will use fallback.")
                    self._stt_model = "fallback"
        return self._stt_model

    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribes speech audio file (WAV, MP3, OGG, WebM) to text."""
        model = self._get_stt_model()
        if model == "fallback" or model is None:
            return "[Voice Error: Install 'faster-whisper' or 'openai-whisper' for local STT transcription]"

        try:
            # Check faster-whisper interface
            if hasattr(model, "transcribe"):
                try:
                    segments, info = model.transcribe(audio_file_path, beam_size=5)
                    text = " ".join([segment.text for segment in segments]).strip()
                    return text
                except TypeError:
                    # openai-whisper interface
                    result = model.transcribe(audio_file_path)
                    return result.get("text", "").strip()
        except Exception as e:
            return f"[Transcription Error: {e}]"

    def synthesize_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """Synthesizes text into offline speech WAV audio."""
        out_file = output_path or str(VOICE_DIR / f"speech_{os.urandom(4).hex()}.wav")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 175) # Speaking speed
            engine.save_to_file(text, out_file)
            engine.runAndWait()
            return out_file
        except ImportError:
            # Fallback: create empty/sine wave audio if pyttsx3 not yet installed
            try:
                with wave.open(out_file, "w") as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(16000)
                    wav_file.writeframes(b"\x00" * 32000)
                return out_file
            except Exception as e:
                print(f"[TTS Error] {e}")
                return ""
        except Exception as e:
            print(f"[TTS Generation Error] {e}")
            return ""

if __name__ == "__main__":
    voice = LunarisVoiceEngine()
    print("Testing Lunaris Voice Engine...")
    test_wav = voice.synthesize_speech("Lunaris AI sovereign voice interface initialized.")
    print("Generated test audio at:", test_wav)
