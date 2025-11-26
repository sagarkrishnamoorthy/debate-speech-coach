# Architecture Documentation

## System Overview

The Speech Analyzer and Coach is a full-stack application that combines audio processing, natural language analysis, and AI-powered feedback to help users improve their public speaking skills.

### High-Level Architecture

```
┌─────────────┐          ┌──────────────┐          ┌────────────────┐
│   Browser   │  HTTP    │    FastAPI   │   API    │  AI Providers  │
│  (React)    │◄────────►│   Backend    │◄────────►│  (Gemini/GPT/  │
│             │  WebSocket│              │          │   Claude)      │
└─────────────┘          └──────────────┘          └────────────────┘
      │                         │
      │                         │
      ▼                         ▼
 MediaRecorder           SpeechRecognition
    API                    (Google API)
```

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python)
- **Audio Processing**: SpeechRecognition, FFmpeg
- **AI Integration**: google-generativeai, openai, anthropic
- **Configuration**: Pydantic Settings
- **Logging**: Loguru

### Component Layers

#### 1. API Layer (`main.py`)
**Responsibilities:**
- HTTP endpoint management
- Request validation
- Background task orchestration
- CORS handling
- Error responses

**Key Endpoints:**
```python
POST /api/speech/upload           # Upload audio file
POST /api/speech/analyze/{id}     # Start analysis
GET  /api/speech/status/{id}      # Check progress
GET  /api/speech/history          # List all analyses
DELETE /api/speech/{id}           # Delete analysis
```

**Design Pattern**: Async/Background Tasks
- Upload is synchronous (fast)
- Analysis runs in background (slow)
- Client polls status endpoint for updates

#### 2. Service Layer (`src/services/`)

**TranscriptionService** (`transcription.py`)
- Converts audio to WAV format using FFmpeg
- Transcribes speech using Google Speech Recognition
- Returns text + duration

**Flow:**
```
Audio File → Convert to WAV → Load Audio → Transcribe → Text + Duration
```

**Error Handling:**
- File format validation
- Audio quality checks
- Transcription failures (unclear audio)

#### 3. Analyzer Layer (`src/analyzers/`)

**PaceAnalyzer** (`pace.py`)
- Counts words in transcription
- Calculates WPM (words per minute)
- Rates pace as: too_slow, optimal, too_fast
- Provides contextual feedback

**Algorithm:**
```python
total_words = len(transcription.split())
duration_minutes = duration_seconds / 60
wpm = total_words / duration_minutes

if wpm < 120:
    rating = "too_slow"
elif wpm > 160:
    rating = "too_fast"
else:
    rating = "optimal"
```

**FillerWordAnalyzer** (`filler_words.py`)
- Uses regex to detect filler words
- Tracks frequency of each filler
- Calculates fillers per minute
- Generates feedback based on rate

**Filler Word List:**
- Simple fillers: um, uh, er, ah
- Phrase fillers: like, you know, i mean
- Habit words: basically, actually, literally, so, well

#### 4. AI Provider Layer (`src/ai/`)

**Design Pattern**: Strategy Pattern + Factory

**BaseAIProvider** (`base.py`)
- Abstract interface for all AI providers
- Defines required methods:
  - `analyze_argument_structure()`
  - `analyze_word_choice()`
  - `generate_score()`
- Provides prompt templates

**Provider Implementations:**
- **GeminiProvider** (`gemini_provider.py`)
- **OpenAIProvider** (`openai_provider.py`)
- **AnthropicProvider** (`anthropic_provider.py`)

**Each implements:**
```python
class AIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        # Initialize client
    
    def analyze_argument_structure(self, text: str) -> ArgumentStructure:
        # Call AI API with structured prompt
        # Parse JSON response
        # Return structured data
    
    def analyze_word_choice(self, text: str) -> WordChoiceAnalysis:
        # Similar pattern
    
    def generate_score(...) -> SpeechScore:
        # Calculate component scores
        # Get AI explanation
        # Return complete score
```

**AIProviderFactory** (`factory.py`)
```python
provider = AIProviderFactory.create(AIProvider.GEMINI)
# Returns appropriate provider instance
```

**Benefits:**
- Easy to add new AI providers
- Consistent interface across providers
- Provider selection at runtime
- Testable via mocking

#### 5. Model Layer (`src/models/speech.py`)

**Pydantic Models** for type safety and validation:

```python
# Analysis Results
- FillerWord
- PaceAnalysis
- FillerWordAnalysis
- ArgumentStructure
- WordChoiceAnalysis
- SpeechScore
- SpeechAnalysis (complete result)

# API Communication
- AnalysisRequest
- AnalysisResponse
- AIProvider (enum)
```

**Benefits:**
- Automatic validation
- Type hints for IDE support
- JSON serialization
- Documentation generation

#### 6. Configuration Layer (`src/config.py`)

**Pydantic Settings**:
- Loads from environment variables
- Validates configuration
- Provides defaults
- Creates directories on startup

```python
settings = Settings()
# Loads from .env automatically
# settings.gemini_api_key
# settings.default_ai_provider
```

### Data Flow

**Complete Analysis Pipeline:**

```
1. Upload Audio File
   ↓
2. Save to uploads/ directory
   ↓
3. Create job record (status: uploaded)
   ↓
4. Start background task
   ↓
5. Transcription Service
   - Convert audio format
   - Transcribe to text
   - Extract duration
   ↓
6. Basic Analyzers (Parallel)
   - Pace Analysis
   - Filler Word Analysis
   ↓
7. AI Provider Analysis (Sequential)
   - Argument Structure
   - Word Choice
   ↓
8. Score Calculation
   - Calculate component scores
   - Generate explanation
   - List strengths/improvements
   ↓
9. Complete Analysis Object
   ↓
10. Update job status (completed)
```

### Scoring Algorithm

**Pace Score (25 points):**
```python
if pace_rating == "optimal":
    score = 25
elif pace_rating == "too_slow":
    penalty = (120 - wpm) / 5
    score = max(15, 25 - penalty)
else:  # too_fast
    penalty = (wpm - 160) / 5
    score = max(15, 25 - penalty)
```

**Clarity Score (25 points):**
```python
if filler_rate < 2:
    score = 25
elif filler_rate < 5:
    score = 20
elif filler_rate < 10:
    score = 15
else:
    score = max(5, 25 - int(filler_rate * 1.5))
```

**Structure Score (25 points):**
```python
score = int((logical_flow_score / 10) * 25)
```

**Vocabulary Score (25 points):**
```python
score = int((vocabulary_richness_score / 10) * 25)
```

### Error Handling Strategy

**Layers of Error Handling:**

1. **API Layer**: HTTP exceptions with meaningful messages
2. **Service Layer**: Specific exceptions (transcription errors, file errors)
3. **AI Layer**: Fallback to basic scores if AI fails
4. **Client Layer**: User-friendly error display

**Example:**
```python
try:
    analysis = await process_speech()
except TranscriptionError as e:
    return {"error": "Could not understand audio"}
except AIProviderError as e:
    return {"error": "AI analysis failed", "partial_results": ...}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal server error"}
```

## Frontend Architecture

### Technology Stack
- **Framework**: React 19 with TypeScript
- **State Management**: React Hooks (useState, useEffect)
- **API Client**: Axios
- **Charts**: Recharts
- **Styling**: Inline Tailwind classes

### Component Structure

```
App.tsx (Main Container)
├── AudioRecorder.tsx (Recording Component)
├── ScoreDisplay.tsx (Score Visualization)
└── AnalysisDetails.tsx (Detailed Breakdown)
```

### State Management

**App-Level State:**
```typescript
- selectedFile: File | null          // Uploaded/recorded file
- analysisId: string | null          // Backend job ID
- status: string                     // idle, uploading, processing, completed, error
- analysis: SpeechAnalysis | null    // Complete results
- error: string | null               // Error messages
- aiProvider: string                 // Selected AI provider
```

**Flow:**
```
idle → uploading → analyzing → processing → completed
                                         ↘ error
```

### API Client Design

**Service Pattern** (`services/api.ts`):
```typescript
class API {
    private client: AxiosInstance;
    
    async uploadSpeech(file: File)
    async analyzeUpload(id: string, provider?: string)
    async getAnalysisStatus(id: string)
    async getHistory()
    async deleteAnalysis(id: string)
}

export const api = new API();
```

**Benefits:**
- Centralized API logic
- Type-safe requests/responses
- Easy to mock for testing
- Single source of truth for endpoints

### Component Details

**AudioRecorder**:
- Uses Web MediaRecorder API
- Real-time timer display
- Converts recording to Blob
- Passes Blob to parent via callback

**ScoreDisplay**:
- Radar chart visualization
- Color-coded score ranges
- Component breakdown grid
- Strengths and improvements lists

**AnalysisDetails**:
- Transcription display
- Pace metrics
- Filler word frequency
- Argument structure checks
- Word improvement suggestions

### Polling Mechanism

```typescript
useEffect(() => {
    if (analysisId && status === 'processing') {
        const interval = setInterval(async () => {
            const response = await api.getAnalysisStatus(analysisId);
            
            if (response.status === 'completed') {
                setAnalysis(response.analysis);
                clearInterval(interval);
            }
        }, 2000); // Poll every 2 seconds
        
        return () => clearInterval(interval);
    }
}, [analysisId, status]);
```

## Security Considerations

### API Keys
- Stored in `.env` (never committed)
- Loaded server-side only
- Not exposed to frontend

### File Upload
- File type validation
- Size limits (configurable)
- Unique filename generation
- Stored in server-only directory

### CORS
- Specific origin whitelist
- No wildcard origins in production

### Input Validation
- Pydantic models validate all inputs
- File extension checking
- Duration limits

## Performance Optimization

### Backend
- Async/await for non-blocking operations
- Background tasks for long processes
- Efficient file streaming
- Minimal memory footprint

### Frontend
- Component-level state
- Memoization where needed
- Lazy loading of results
- Efficient re-renders

### AI API Optimization
- Structured prompts for consistent responses
- JSON mode where supported
- Timeout handling
- Retry logic

## Scalability Considerations

### Current Architecture
- In-memory job storage (suitable for single-server, low-volume)
- Local file storage
- Synchronous AI calls

### Future Enhancements for Scale
- **Database**: PostgreSQL for persistent storage
- **Queue System**: Celery/RQ for background jobs
- **File Storage**: S3/Cloud Storage
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Multiple backend instances
- **Rate Limiting**: Prevent API abuse

## Extensibility Points

### Adding New AI Provider
1. Create new provider class in `src/ai/`
2. Implement `BaseAIProvider` interface
3. Add to `AIProviderFactory`
4. Update `AIProvider` enum
5. Add configuration to settings

### Adding New Analyzer
1. Create analyzer class in `src/analyzers/`
2. Define analysis model in `src/models/speech.py`
3. Integrate into pipeline in `main.py`
4. Update `SpeechAnalysis` model
5. Add UI component for results

### Adding New Features
- **Voice comparison**: Compare recordings over time
- **Team analysis**: Batch process team speeches
- **Custom rubrics**: Define scoring criteria
- **Language support**: Multi-language transcription
- **Real-time analysis**: Stream processing during recording

## Testing Strategy

### Unit Tests
- Analyzer logic
- Score calculations
- Prompt generation

### Integration Tests
- API endpoints
- File upload/download
- Background task processing

### E2E Tests
- Complete analysis workflow
- UI interactions
- Error scenarios

## Monitoring and Logging

### Logging Levels
- **INFO**: Normal operations, requests
- **WARNING**: Recoverable errors, timeouts
- **ERROR**: Failures, exceptions

### Log Storage
- Rotating file logs in `logs/`
- Structured logging with Loguru
- Timestamps and context

### Metrics to Track
- Analysis duration
- AI provider response times
- Error rates
- File upload sizes

## Deployment Considerations

### Environment Setup
- Python virtual environment
- Node.js version management
- FFmpeg installation
- API key configuration

### Production Checklist
- [ ] Set secure SECRET_KEY
- [ ] Configure production CORS origins
- [ ] Enable HTTPS
- [ ] Set up logging aggregation
- [ ] Configure file cleanup jobs
- [ ] Set resource limits
- [ ] Enable rate limiting
- [ ] Set up monitoring/alerting

---

**Architecture designed for clarity, extensibility, and maintainability**
