"""Analyzer for speech pace."""
from ..models.speech import PaceAnalysis


class PaceAnalyzer:
    """Analyzes the pace of speech."""
    
    # Optimal words per minute ranges
    OPTIMAL_WPM_MIN = 120
    OPTIMAL_WPM_MAX = 160
    
    def analyze(self, transcription: str, duration_seconds: float) -> PaceAnalysis:
        """
        Analyze the pace of speech.
        
        Args:
            transcription: The speech transcription
            duration_seconds: Duration of the speech in seconds
            
        Returns:
            PaceAnalysis with pace metrics and feedback
        """
        # Count words
        words = transcription.split()
        total_words = len(words)
        
        # Calculate words per minute
        duration_minutes = duration_seconds / 60
        wpm = total_words / duration_minutes if duration_minutes > 0 else 0
        
        # Determine pace rating
        if wpm < self.OPTIMAL_WPM_MIN:
            pace_rating = "too_slow"
            feedback = (
                f"Your speaking pace is {round(wpm)} words per minute, which is slower than optimal. "
                f"Try to speak slightly faster to maintain audience engagement. "
                f"Aim for {self.OPTIMAL_WPM_MIN}-{self.OPTIMAL_WPM_MAX} WPM."
            )
        elif wpm > self.OPTIMAL_WPM_MAX:
            pace_rating = "too_fast"
            feedback = (
                f"Your speaking pace is {round(wpm)} words per minute, which is faster than optimal. "
                f"Slow down to ensure clarity and give your audience time to absorb your points. "
                f"Aim for {self.OPTIMAL_WPM_MIN}-{self.OPTIMAL_WPM_MAX} WPM."
            )
        else:
            pace_rating = "optimal"
            feedback = (
                f"Excellent! Your speaking pace is {round(wpm)} words per minute, "
                f"which is in the optimal range of {self.OPTIMAL_WPM_MIN}-{self.OPTIMAL_WPM_MAX} WPM. "
                "This pace helps maintain audience engagement while ensuring clarity."
            )
        
        return PaceAnalysis(
            words_per_minute=round(wpm, 2),
            total_words=total_words,
            total_duration_seconds=round(duration_seconds, 2),
            pace_rating=pace_rating,
            feedback=feedback
        )
