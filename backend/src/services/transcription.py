"""Speech-to-text transcription service."""
import speech_recognition as sr
from pathlib import Path
from typing import Tuple
from loguru import logger
import subprocess
import tempfile


class TranscriptionService:
    """Service for converting audio to text."""
    
    def __init__(self):
        """Initialize the transcription service."""
        self.recognizer = sr.Recognizer()
    
    def _convert_to_wav(self, audio_path: Path) -> Path:
        """
        Convert audio file to WAV format if needed.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Path to WAV file
        """
        if audio_path.suffix.lower() == '.wav':
            return audio_path
        
        # Create temporary WAV file
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav_path = Path(temp_wav.name)
        
        try:
            # Use ffmpeg to convert (with -y to auto-overwrite)
            subprocess.run([
                'ffmpeg', '-y', '-i', str(audio_path),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                str(temp_wav_path)
            ], check=True, capture_output=True, timeout=60)
            
            return temp_wav_path
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg conversion timed out")
            raise RuntimeError("Audio conversion timed out after 60 seconds")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert audio: {e}")
            raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}")
    
    def transcribe(self, audio_path: Path) -> Tuple[str, float]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Tuple of (transcription_text, duration_in_seconds)
        """
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Convert to WAV if needed
            wav_path = self._convert_to_wav(audio_path)
            
            # Load audio file
            with sr.AudioFile(str(wav_path)) as source:
                # Get duration
                duration = source.DURATION
                
                # Record the audio
                audio_data = self.recognizer.record(source)
            
            # Clean up temp file if we created one
            if wav_path != audio_path:
                wav_path.unlink()
            
            # Transcribe using Google Speech Recognition
            try:
                # Add timeout to prevent hanging (max 60 seconds)
                text = self.recognizer.recognize_google(audio_data, show_all=False)
                logger.info(f"Transcription successful: {len(text)} characters")
                return text, duration
            except sr.UnknownValueError:
                logger.error("Could not understand audio")
                raise RuntimeError("Could not understand the audio. Please ensure clear speech.")
            except sr.RequestError as e:
                logger.error(f"Transcription service error: {e}")
                raise RuntimeError(f"Transcription service error: {e}")
            except Exception as e:
                logger.error(f"Unexpected transcription error: {e}")
                raise RuntimeError(f"Transcription failed: {e}")
                
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
