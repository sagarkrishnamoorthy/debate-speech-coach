# Speech Analyzer and Coach 🎤

An AI-powered speech analysis tool designed for debate and public speaking improvement. Analyzes pace, filler words, argument structure, and vocabulary to provide detailed feedback and scoring.

## Features

### 🎯 Core Analysis
- **Pace Analysis**: Measures words per minute and provides feedback on speaking speed
- **Filler Word Detection**: Identifies and counts filler words like "um", "like", "you know", etc.
- **Argument Structure**: Evaluates thesis clarity, supporting points, and logical flow
- **Word Choice Analysis**: Suggests stronger alternatives and identifies repetitive language

### 📊 Comprehensive Scoring
- **100-Point Scale**: Clear scoring with detailed breakdown
- **Four Components**: Pace (25pts), Clarity (25pts), Structure (25pts), Vocabulary (25pts)
- **Detailed Explanations**: Understand exactly why you received your score
- **Actionable Feedback**: Specific strengths and areas for improvement

### 🤖 Multi-Model AI Support
- **Gemini** (Google) - Default provider
- **GPT** (OpenAI) - Optional
- **Claude** (Anthropic) - Optional

Switch providers via command line or API selection!

### 🎙️ Flexible Input
- **Live Recording**: Record directly in the browser
- **File Upload**: Support for MP3, WAV, OGG, M4A, FLAC formats

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SpeechRecognition**: Audio transcription
- **Pydantic**: Data validation and settings
- **Multi-AI Integration**: Gemini, OpenAI, Anthropic APIs

### Frontend
- **React 19 + TypeScript**: Modern UI framework
- **Recharts**: Data visualization for score breakdown
- **Axios**: API communication
- **Tailwind CSS**: Styling (via inline classes)

## Project Structure

```
debate-speech-coach/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment template
│   ├── src/
│   │   ├── config.py       # Configuration management
│   │   ├── models/         # Pydantic data models
│   │   │   └── speech.py
│   │   ├── services/       # Business logic
│   │   │   └── transcription.py
│   │   ├── analyzers/      # Analysis modules
│   │   │   ├── pace.py
│   │   │   └── filler_words.py
│   │   └── ai/            # AI provider integrations
│   │       ├── base.py
│   │       ├── gemini_provider.py
│   │       ├── openai_provider.py
│   │       ├── anthropic_provider.py
│   │       └── factory.py
│   ├── uploads/           # Uploaded audio files
│   └── logs/             # Application logs
└── frontend/
    ├── src/
    │   ├── App.tsx          # Main application
    │   ├── services/
    │   │   └── api.ts       # API client
    │   └── components/
    │       ├── AudioRecorder.tsx
    │       ├── ScoreDisplay.tsx
    │       └── AnalysisDetails.tsx
    └── package.json
```

## Getting Started

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

### Quick Start

**Backend:**
```bash
cd backend
cp .env.example .env
# Add your API keys to .env
pip install -r requirements.txt
npm start
# OR: npm run dev:gemini, npm run dev:openai, npm run dev:claude
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` to start analyzing speeches!

## Usage

1. **Select AI Provider**: Choose between Gemini, GPT, or Claude
2. **Input Speech**: Either record live or upload an audio file
3. **Analyze**: Click "Analyze Speech" to start processing
4. **Review Results**: 
   - Overall score (1-100) with breakdown
   - Detailed pace analysis
   - Filler word detection
   - Argument structure evaluation
   - Word choice recommendations
5. **Track Progress**: Compare scores over time to see improvement

## Scoring System

### Score Breakdown (out of 100)
- **Pace Score (25 points)**: Based on words per minute (optimal: 120-160 WPM)
- **Clarity Score (25 points)**: Based on filler word rate (lower is better)
- **Structure Score (25 points)**: Based on logical flow and organization
- **Vocabulary Score (25 points)**: Based on word choice richness

### Score Interpretation
- **80-100**: Excellent - Professional-level speaking
- **60-79**: Good - Solid fundamentals, minor improvements needed
- **40-59**: Fair - Several areas need attention
- **0-39**: Needs Work - Significant practice required

## API Endpoints

### Upload Speech
```
POST /api/speech/upload
Content-Type: multipart/form-data
Body: file (audio file)
```

### Start Analysis
```
POST /api/speech/analyze/{analysis_id}?ai_provider=gemini
```

### Check Status
```
GET /api/speech/status/{analysis_id}
```

### Get History
```
GET /api/speech/history
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required: At least one API key
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Optional
DEFAULT_AI_PROVIDER=gemini
GEMINI_MODEL=gemini-pro
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### Command Line Options

Start the backend with custom settings:

**Using npm scripts (recommended):**
```bash
npm start                    # Default: Gemini on port 8000
npm run dev:gemini          # Gemini
npm run dev:openai          # OpenAI GPT
npm run dev:claude          # Anthropic Claude
```

**Using Python directly:**
```bash
python main.py --provider gemini --port 8000 --host 0.0.0.0
```

## Architecture

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Requirements

### Backend
- Python 3.9+
- FFmpeg (for audio conversion)
- Internet connection (for AI APIs)

### Frontend
- Node.js 18+
- Modern browser with MediaRecorder API support

## Limitations

- Maximum audio duration: 10 minutes (configurable)
- Transcription requires clear audio quality
- AI analysis quality depends on speech clarity and length
- Best results with speeches longer than 1 minute

## Future Enhancements

- [ ] Database integration for persistent storage
- [ ] User authentication and profiles
- [ ] Historical trend analysis and charts
- [ ] Export reports as PDF
- [ ] Batch processing for multiple speeches
- [ ] Speaker identification in multi-speaker recordings
- [ ] Real-time analysis during recording
- [ ] Custom vocabulary and terminology databases

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for better public speaking**
