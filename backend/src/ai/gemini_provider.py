"""Gemini AI provider implementation."""
import json
import google.generativeai as genai
from loguru import logger
from typing import Dict, Any

from .base import BaseAIProvider
from ..models.speech import ArgumentStructure, WordChoiceAnalysis, SpeechScore
from ..config import settings


class GeminiProvider(BaseAIProvider):
    """Gemini AI provider for speech analysis."""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini provider."""
        api_key = api_key or settings.gemini_api_key
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        logger.info(f"Initialized Gemini provider with model: {settings.gemini_model}")
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling markdown code blocks."""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}\nResponse: {response_text}")
            raise ValueError(f"Invalid JSON response from AI: {e}")
    
    def analyze_argument_structure(self, transcription: str) -> ArgumentStructure:
        """Analyze argument structure using Gemini."""
        prompt = self._create_analysis_prompt(transcription, "structure")
        
        try:
            response = self.model.generate_content(prompt)
            data = self._parse_json_response(response.text)
            
            return ArgumentStructure(
                has_clear_thesis=data.get("has_clear_thesis", False),
                has_supporting_points=data.get("has_supporting_points", False),
                has_conclusion=data.get("has_conclusion", False),
                logical_flow_score=data.get("logical_flow_score", 5),
                feedback=data.get("feedback", ""),
                suggestions=data.get("suggestions", [])
            )
        except Exception as e:
            logger.error(f"Gemini structure analysis failed: {e}")
            raise
    
    def analyze_word_choice(self, transcription: str) -> WordChoiceAnalysis:
        """Analyze word choice using Gemini."""
        prompt = self._create_analysis_prompt(transcription, "word_choice")
        
        try:
            response = self.model.generate_content(prompt)
            data = self._parse_json_response(response.text)
            
            return WordChoiceAnalysis(
                weak_words=data.get("weak_words", []),
                repetitive_words=data.get("repetitive_words", []),
                vocabulary_richness_score=data.get("vocabulary_richness_score", 5),
                feedback=data.get("feedback", "")
            )
        except Exception as e:
            logger.error(f"Gemini word choice analysis failed: {e}")
            raise
    
    def generate_score(
        self,
        transcription: str,
        pace_score: int,
        filler_word_rate: float,
        structure_analysis: ArgumentStructure,
        word_choice_analysis: WordChoiceAnalysis
    ) -> SpeechScore:
        """Generate overall score using Gemini."""
        
        # Calculate clarity score based on filler word rate
        if filler_word_rate < 2:
            clarity_score = 25
        elif filler_word_rate < 5:
            clarity_score = 20
        elif filler_word_rate < 10:
            clarity_score = 15
        else:
            clarity_score = max(5, 25 - int(filler_word_rate * 1.5))
        
        # Calculate structure score
        structure_score = int((structure_analysis.logical_flow_score / 10) * 25)
        
        # Calculate vocabulary score
        vocabulary_score = int((word_choice_analysis.vocabulary_richness_score / 10) * 25)
        
        # Total score
        total_score = pace_score + clarity_score + structure_score + vocabulary_score
        
        # Generate detailed explanation
        prompt = f"""You are scoring a speech. Here are the component scores:

Pace Score: {pace_score}/25
Clarity Score: {clarity_score}/25 (Filler word rate: {filler_word_rate} per minute)
Structure Score: {structure_score}/25 (Logical flow: {structure_analysis.logical_flow_score}/10)
Vocabulary Score: {vocabulary_score}/25 (Richness: {word_choice_analysis.vocabulary_richness_score}/10)

Total Score: {total_score}/100

Speech excerpt: {transcription[:500]}...

Provide:
1. A detailed explanation of why this score was given (2-3 sentences)
2. A list of 3-5 specific strengths
3. A list of 3-5 specific areas for improvement

Respond in JSON format with keys: explanation (string), strengths (list of strings), areas_for_improvement (list of strings)."""
        
        try:
            response = self.model.generate_content(prompt)
            data = self._parse_json_response(response.text)
            
            return SpeechScore(
                total_score=total_score,
                pace_score=pace_score,
                clarity_score=clarity_score,
                structure_score=structure_score,
                vocabulary_score=vocabulary_score,
                explanation=data.get("explanation", ""),
                strengths=data.get("strengths", []),
                areas_for_improvement=data.get("areas_for_improvement", [])
            )
        except Exception as e:
            logger.error(f"Gemini scoring failed: {e}")
            # Return basic score without detailed explanation
            return SpeechScore(
                total_score=total_score,
                pace_score=pace_score,
                clarity_score=clarity_score,
                structure_score=structure_score,
                vocabulary_score=vocabulary_score,
                explanation=f"Score breakdown: Pace={pace_score}, Clarity={clarity_score}, Structure={structure_score}, Vocabulary={vocabulary_score}",
                strengths=["Analysis completed"],
                areas_for_improvement=["Detailed analysis unavailable"]
            )
