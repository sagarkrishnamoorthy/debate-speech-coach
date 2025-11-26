"""Base AI provider interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models.speech import ArgumentStructure, WordChoiceAnalysis, SpeechScore


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def analyze_argument_structure(self, transcription: str) -> ArgumentStructure:
        """
        Analyze the argument structure of the speech.
        
        Args:
            transcription: The speech transcription
            
        Returns:
            ArgumentStructure analysis
        """
        pass
    
    @abstractmethod
    def analyze_word_choice(self, transcription: str) -> WordChoiceAnalysis:
        """
        Analyze word choice and vocabulary.
        
        Args:
            transcription: The speech transcription
            
        Returns:
            WordChoiceAnalysis
        """
        pass
    
    @abstractmethod
    def generate_score(
        self,
        transcription: str,
        pace_score: int,
        filler_word_rate: float,
        structure_analysis: ArgumentStructure,
        word_choice_analysis: WordChoiceAnalysis
    ) -> SpeechScore:
        """
        Generate overall speech score with explanation.
        
        Args:
            transcription: The speech transcription
            pace_score: Score for pace (out of 25)
            filler_word_rate: Rate of filler words per minute
            structure_analysis: Argument structure analysis
            word_choice_analysis: Word choice analysis
            
        Returns:
            SpeechScore with breakdown and explanation
        """
        pass
    
    def _create_analysis_prompt(self, transcription: str, analysis_type: str) -> str:
        """Create a structured prompt for analysis."""
        if analysis_type == "structure":
            return f"""Analyze the following speech for its argument structure. Evaluate:
1. Does it have a clear thesis or main argument?
2. Are there supporting points that back up the thesis?
3. Is there a conclusion that ties things together?
4. Rate the logical flow from 1-10
5. Provide constructive feedback and specific suggestions

Speech:
{transcription}

Respond in JSON format with keys: has_clear_thesis (boolean), has_supporting_points (boolean), has_conclusion (boolean), logical_flow_score (1-10), feedback (string), suggestions (list of strings)."""

        elif analysis_type == "word_choice":
            return f"""Analyze the following speech for word choice and vocabulary. Identify:
1. Weak or vague words that could be replaced with stronger alternatives (max 5)
2. Repetitive words that are overused (max 5)
3. Rate vocabulary richness from 1-10
4. Provide feedback on overall word choice

Speech:
{transcription}

Respond in JSON format with keys: weak_words (list of {{"word": "x", "suggestion": "y"}}), repetitive_words (list of {{"word": "x", "count": n}}), vocabulary_richness_score (1-10), feedback (string)."""

        elif analysis_type == "scoring":
            return """You are scoring a speech on a scale of 1-100. Break down the score into four components (each out of 25):
1. Pace Score (already calculated): Consider the words per minute and clarity
2. Clarity Score (based on filler word rate): Fewer fillers = higher score
3. Structure Score (based on argument analysis): Logical flow and organization
4. Vocabulary Score (based on word choice): Richness and appropriateness

Provide a detailed explanation of the total score, list 3-5 strengths, and 3-5 areas for improvement."""
