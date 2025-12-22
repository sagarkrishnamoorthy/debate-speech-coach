"""Main FastAPI application for Speech Analyzer and Coach."""
# Python 3.14 compatibility
from src import compat

import argparse
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from typing import Dict, Optional
import uuid
import shutil
from loguru import logger
from datetime import datetime

from src.config import settings
from src.models.speech import (
    AIProvider, SpeechAnalysis, AnalysisResponse
)
from src.services.transcription import TranscriptionService
from src.analyzers.pace import PaceAnalyzer
from src.analyzers.filler_words import FillerWordAnalyzer
from src.ai.factory import AIProviderFactory

# Configure logging
logger.add(
    settings.log_dir / "app.log",
    rotation="500 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Initialize FastAPI app
app = FastAPI(
    title="Speech Analyzer and Coach API",
    description="AI-powered speech analysis for debate and public speaking improvement",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for analyses
analyses: Dict[str, Dict] = {}

# Initialize services
transcription_service = TranscriptionService()
pace_analyzer = PaceAnalyzer()
filler_word_analyzer = FillerWordAnalyzer()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Speech Analyzer and Coach API",
        "version": "1.0.0",
        "ai_provider": settings.default_ai_provider,
        "endpoints": {
            "upload": "/api/speech/upload",
            "analyze": "/api/speech/analyze/{analysis_id}",
            "history": "/api/speech/history",
            "docs": "/docs"
        }
    }


@app.get("/favicon.ico")
async def favicon():
    """Return 204 No Content for favicon requests."""
    return JSONResponse(status_code=204, content={})


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Speech Analyzer API",
        "ai_provider": settings.default_ai_provider
    }


@app.post("/api/speech/upload")
async def upload_speech(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload a speech audio file for analysis.
    
    Args:
        file: Audio file (mp3, wav, ogg, m4a, flac)
        
    Returns:
        Analysis ID for tracking
    """
    # Validate file type (outside try-except so HTTPException can propagate)
    allowed_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".webm"]
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Save uploaded file
        upload_path = settings.upload_dir / f"{analysis_id}{file_ext}"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize analysis status
        analyses[analysis_id] = {
            "id": analysis_id,
            "filename": file.filename,
            "upload_path": str(upload_path),
            "status": "uploaded",
            "created_at": datetime.now().isoformat(),
            "analysis": None,
            "error": None
        }
        
        logger.info(f"Speech uploaded: {analysis_id} - {file.filename}")
        
        return {
            "analysis_id": analysis_id,
            "status": "uploaded",
            "message": "File uploaded successfully. Use /api/speech/analyze to start analysis."
        }
        
    except Exception as e:
        import traceback
        logger.error(f"Upload error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_analysis(
    analysis_id: str,
    upload_path: Path,
    filename: str,
    ai_provider: AIProvider
):
    """Process speech analysis asynchronously."""
    try:
        logger.info(f"Starting analysis: {analysis_id}")
        analyses[analysis_id]["status"] = "processing"
        
        # Step 1: Transcribe audio
        logger.info(f"Transcribing audio: {analysis_id}")
        transcription, duration = transcription_service.transcribe(upload_path)
        
        # Step 2: Basic analyses (pace, filler words)
        logger.info(f"Analyzing pace and filler words: {analysis_id}")
        pace_analysis = pace_analyzer.analyze(transcription, duration)
        filler_analysis = filler_word_analyzer.analyze(transcription, duration)
        
        # Step 3: AI-powered analyses
        logger.info(f"Running AI analysis with {ai_provider}: {analysis_id}")
        ai_provider_instance = AIProviderFactory.create(ai_provider)
        
        structure_analysis = ai_provider_instance.analyze_argument_structure(transcription)
        word_choice_analysis = ai_provider_instance.analyze_word_choice(transcription)
        
        # Step 4: Calculate pace score
        if pace_analysis.pace_rating == "optimal":
            pace_score = 25
        elif pace_analysis.pace_rating == "too_slow":
            pace_score = max(15, 25 - int((PaceAnalyzer.OPTIMAL_WPM_MIN - pace_analysis.words_per_minute) / 5))
        else:  # too_fast
            pace_score = max(15, 25 - int((pace_analysis.words_per_minute - PaceAnalyzer.OPTIMAL_WPM_MAX) / 5))
        
        # Step 5: Generate overall score
        score = ai_provider_instance.generate_score(
            transcription,
            pace_score,
            filler_analysis.filler_word_rate,
            structure_analysis,
            word_choice_analysis
        )
        
        # Create complete analysis
        analysis = SpeechAnalysis(
            id=analysis_id,
            filename=filename,
            analyzed_at=datetime.now(),
            duration_seconds=duration,
            transcription=transcription,
            pace_analysis=pace_analysis,
            filler_word_analysis=filler_analysis,
            argument_structure=structure_analysis,
            word_choice_analysis=word_choice_analysis,
            score=score,
            ai_provider=ai_provider,
            raw_ai_feedback=""
        )
        
        analyses[analysis_id]["analysis"] = analysis
        analyses[analysis_id]["status"] = "completed"
        logger.info(f"Analysis completed: {analysis_id} - Score: {score.total_score}/100")
        
    except Exception as e:
        logger.error(f"Analysis failed for {analysis_id}: {e}")
        analyses[analysis_id]["status"] = "failed"
        analyses[analysis_id]["error"] = str(e)


@app.post("/api/speech/analyze/{analysis_id}")
async def analyze_speech(
    analysis_id: str,
    background_tasks: BackgroundTasks,
    ai_provider: Optional[AIProvider] = Query(None, description="AI provider to use (gemini, openai, anthropic)")
):
    """
    Start analysis of an uploaded speech.
    
    Args:
        analysis_id: ID from upload endpoint
        ai_provider: Optional AI provider override
        
    Returns:
        Analysis status
    """
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis_data = analyses[analysis_id]
    
    if analysis_data["status"] != "uploaded":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis already {analysis_data['status']}"
        )
    
    # Use specified provider or default
    provider = ai_provider or AIProvider(settings.default_ai_provider)
    
    # Start async processing
    background_tasks.add_task(
        process_analysis,
        analysis_id,
        Path(analysis_data["upload_path"]),
        analysis_data["filename"],
        provider
    )
    
    return {
        "analysis_id": analysis_id,
        "status": "processing",
        "ai_provider": provider.value,
        "message": "Analysis started. Check status with GET /api/speech/status/{analysis_id}"
    }


@app.get("/api/speech/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get the status of a speech analysis."""
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    data = analyses[analysis_id]
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status=data["status"],
        analysis=data.get("analysis"),
        error=data.get("error")
    )


@app.get("/api/speech/history")
async def get_analysis_history():
    """Get all speech analyses."""
    history = []
    for analysis_id, data in analyses.items():
        history.append({
            "id": analysis_id,
            "filename": data["filename"],
            "status": data["status"],
            "created_at": data["created_at"],
            "score": data["analysis"].score.total_score if data.get("analysis") else None
        })
    
    # Sort by created_at (most recent first)
    history.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"analyses": history, "total": len(history)}


@app.delete("/api/speech/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete a speech analysis."""
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete uploaded file
    upload_path = Path(analyses[analysis_id]["upload_path"])
    if upload_path.exists():
        upload_path.unlink()
    
    # Remove from storage
    del analyses[analysis_id]
    
    return {"message": "Analysis deleted successfully"}


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Speech Analyzer API Server")
    parser.add_argument(
        "--provider",
        type=str,
        choices=["gemini", "openai", "anthropic"],
        default=settings.default_ai_provider,
        help="AI provider to use"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help="Port to run the server on"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=settings.host,
        help="Host to bind the server to"
    )
    return parser.parse_args()


if __name__ == "__main__":
    import uvicorn
    
    args = parse_args()
    
    # Update settings with CLI args
    settings.default_ai_provider = args.provider
    
    logger.info(f"Starting Speech Analyzer API with {args.provider} provider")
    logger.info(f"Server will run on {args.host}:{args.port}")
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=True
    )
