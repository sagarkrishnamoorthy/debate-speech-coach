"""Data models for speech analysis."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class AIProvider(str, Enum):
    """Supported AI providers."""
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class FillerWord(BaseModel):
    """Represents a detected filler word."""
    word: str
    count: int
    timestamps: List[float] = Field(default_factory=list)


class PaceAnalysis(BaseModel):
    """Analysis of speech pace."""
    words_per_minute: float
    total_words: int
    total_duration_seconds: float
    pace_rating: str  # "too_slow", "optimal", "too_fast"
    feedback: str


class FillerWordAnalysis(BaseModel):
    """Analysis of filler words."""
    total_filler_words: int
    filler_words: List[FillerWord]
    filler_word_rate: float  # fillers per minute
    feedback: str


class ArgumentStructure(BaseModel):
    """Analysis of argument structure."""
    has_clear_thesis: bool
    has_supporting_points: bool
    has_conclusion: bool
    logical_flow_score: int = Field(ge=1, le=10)
    feedback: str
    suggestions: List[str]


class RepetitiveWord(BaseModel):
    """Represents a repetitive word with its count."""
    word: str
    count: int


class WeakWord(BaseModel):
    """Represents a weak word with a suggested alternative."""
    word: str
    suggestion: str


class WordChoiceAnalysis(BaseModel):
    """Analysis of word choice and vocabulary."""
    weak_words: List[WeakWord]
    repetitive_words: List[RepetitiveWord]
    vocabulary_richness_score: int = Field(ge=1, le=10)
    feedback: str


class SpeechScore(BaseModel):
    """Overall speech score with breakdown."""
    total_score: int = Field(ge=1, le=100)
    pace_score: int = Field(ge=1, le=25)
    clarity_score: int = Field(ge=1, le=25)
    structure_score: int = Field(ge=1, le=25)
    vocabulary_score: int = Field(ge=1, le=25)
    explanation: str
    strengths: List[str]
    areas_for_improvement: List[str]


class SpeechAnalysis(BaseModel):
    """Complete speech analysis result."""
    id: str
    filename: str
    analyzed_at: datetime = Field(default_factory=datetime.now)
    duration_seconds: float
    transcription: str
    
    # Analysis components
    pace_analysis: PaceAnalysis
    filler_word_analysis: FillerWordAnalysis
    argument_structure: ArgumentStructure
    word_choice_analysis: WordChoiceAnalysis
    
    # Overall score
    score: SpeechScore
    
    # AI provider used
    ai_provider: AIProvider
    
    # Raw AI feedback
    raw_ai_feedback: str


class AnalysisRequest(BaseModel):
    """Request for speech analysis."""
    audio_file_id: str
    ai_provider: Optional[AIProvider] = None


class AnalysisResponse(BaseModel):
    """Response containing analysis results."""
    analysis_id: str
    status: str
    analysis: Optional[SpeechAnalysis] = None
    error: Optional[str] = None
