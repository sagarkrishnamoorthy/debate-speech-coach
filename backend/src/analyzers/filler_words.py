"""Analyzer for detecting filler words in speech."""
import re
from typing import List, Dict
from ..models.speech import FillerWord, FillerWordAnalysis


class FillerWordAnalyzer:
    """Analyzes speech for filler words and provides feedback."""
    
    # Common filler words to detect
    FILLER_WORDS = {
        'um', 'uh', 'er', 'ah',
        'like', 'you know', 'i mean', 'basically', 'actually',
        'literally', 'so', 'well', 'right', 'okay', 'yeah'
    }
    
    def analyze(self, transcription: str, duration_seconds: float) -> FillerWordAnalysis:
        """
        Analyze transcription for filler words.
        
        Args:
            transcription: The speech transcription
            duration_seconds: Duration of the speech in seconds
            
        Returns:
            FillerWordAnalysis with detected fillers and feedback
        """
        text_lower = transcription.lower()
        detected_fillers: List[FillerWord] = []
        total_count = 0
        
        # Detect each filler word
        for filler in self.FILLER_WORDS:
            # Use word boundaries for accurate detection
            pattern = r'\b' + re.escape(filler) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            count = len(matches)
            
            if count > 0:
                detected_fillers.append(FillerWord(
                    word=filler,
                    count=count,
                    timestamps=[]  # Would need audio analysis for precise timestamps
                ))
                total_count += count
        
        # Sort by count (most frequent first)
        detected_fillers.sort(key=lambda x: x.count, reverse=True)
        
        # Calculate filler word rate (per minute)
        duration_minutes = duration_seconds / 60
        filler_rate = total_count / duration_minutes if duration_minutes > 0 else 0
        
        # Generate feedback
        feedback = self._generate_feedback(total_count, filler_rate, detected_fillers)
        
        return FillerWordAnalysis(
            total_filler_words=total_count,
            filler_words=detected_fillers,
            filler_word_rate=round(filler_rate, 2),
            feedback=feedback
        )
    
    def _generate_feedback(
        self,
        total_count: int,
        rate: float,
        fillers: List[FillerWord]
    ) -> str:
        """Generate feedback based on filler word analysis."""
        if rate < 2:
            feedback = "Excellent! Your speech has minimal filler words, showing strong confidence and preparation."
        elif rate < 5:
            feedback = "Good job! You maintain relatively clean speech with acceptable filler word usage."
        elif rate < 10:
            feedback = "Your filler word usage is moderate. Focus on pausing instead of using fillers."
        else:
            feedback = "High filler word usage detected. Practice pausing and being comfortable with silence."
        
        if fillers:
            top_fillers = ", ".join([f"'{f.word}' ({f.count}x)" for f in fillers[:3]])
            feedback += f" Most common fillers: {top_fillers}."
        
        return feedback
