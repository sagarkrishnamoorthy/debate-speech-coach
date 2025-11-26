"""OpenAI provider implementation."""
import json
from openai import OpenAI
from loguru import logger
from typing import Dict, Any

from .base import BaseAIProvider
from ..models.speech import ArgumentStructure, WordChoiceAnalysis, SpeechScore
from ..config import settings


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider for speech analysis."""
    
    def __init__(self, api_key: str = None):
        """Initialize OpenAI provider."""
        api_key = api_key or settings.openai_api_key
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = settings.openai_model
        logger.info(f"Initialized OpenAI provider with model: {self.model}")
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from AI response."""
        try:
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
    
    def _call_api(self, prompt: str) -> str:
        """Make API call to OpenAI."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert speech coach and analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def analyze_argument_structure(self, transcription: str) -> ArgumentStructure:
        """Analyze argument structure using OpenAI."""
        prompt = self._create_analysis_prompt(transcription, "structure")
        
        try:
            response_text = self._call_api(prompt)
            data = self._parse_json_response(response_text)
            
            return ArgumentStructure(
                has_clear_thesis=data.get("has_clear_thesis", False),
                has_supporting_points=data.get("has_supporting_points", False),
                has_conclusion=data.get("has_conclusion", False),
                logical_flow_score=data.get("logical_flow_score", 5),
                feedback=data.get("feedback", ""),
                suggestions=data.get("suggestions", [])
            )
        except Exception as e:
            logger.error(f"OpenAI structure analysis failed: {e}")
            raise
    
    def analyze_word_choice(self, transcription: str) -> WordChoiceAnalysis:
        """Analyze word choice using OpenAI."""
        prompt = self._create_analysis_prompt(transcription, "word_choice")
        
        try:
            response_text = self._call_api(prompt)
            data = self._parse_json_response(response_text)
            
            return WordChoiceAnalysis(
                weak_words=data.get("weak_words", []),
                repetitive_words=data.get("repetitive_words", []),
                vocabulary_richness_score=data.get("vocabulary_richness_score", 5),
                feedback=data.get("feedback", "")
            )
        except Exception as e:
            logger.error(f"OpenAI word choice analysis failed: {e}")
            raise
    
    def generate_score(
        self,
        transcription: str,
        pace_score: int,
        filler_word_rate: float,
        structure_analysis: ArgumentStructure,
        word_choice_analysis: WordChoiceAnalysis
    ) -> SpeechScore:
        """Generate overall score using OpenAI."""
        
        # Calculate scores (same logic as Gemini)
        if filler_word_rate < 2:
            clarity_score = 25
        elif filler_word_rate < 5:
            clarity_score = 20
        elif filler_word_rate < 10:
            clarity_score = 15
        else:
            clarity_score = max(5, 25 - int(filler_word_rate * 1.5))
        
        structure_score = int((structure_analysis.logical_flow_score / 10) * 25)
        vocabulary_score = int((word_choice_analysis.vocabulary_richness_score / 10) * 25)
        total_score = pace_score + clarity_score + structure_score + vocabulary_score
        
        prompt = f"""Score explanation for speech:

Pace Score: {pace_score}/25
Clarity Score: {clarity_score}/25 (Filler word rate: {filler_word_rate}/min)
Structure Score: {structure_score}/25
Vocabulary Score: {vocabulary_score}/25
Total: {total_score}/100

Speech: {transcription[:500]}...

Provide JSON: {{"explanation": "...", "strengths": [...], "areas_for_improvement": [...]}}"""
        
        try:
            response_text = self._call_api(prompt)
            data = self._parse_json_response(response_text)
            
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
            logger.error(f"OpenAI scoring failed: {e}")
            return SpeechScore(
                total_score=total_score,
                pace_score=pace_score,
                clarity_score=clarity_score,
                structure_score=structure_score,
                vocabulary_score=vocabulary_score,
                explanation=f"Score breakdown: {total_score}/100",
                strengths=["Analysis completed"],
                areas_for_improvement=["Detailed analysis unavailable"]
            )
