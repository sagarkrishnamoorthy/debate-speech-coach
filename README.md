# Speech Analyzer and Coach 🎤

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)

An AI-powered speech analysis tool designed for debate and public speaking improvement. Analyzes pace, filler words, argument structure, and vocabulary to provide detailed feedback and scoring.

**[Quick Start](#getting-started)** • **[Documentation](#documentation)** • **[Contributing](#contributing)** • **[License](#license)**

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

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Setup and first steps
- **[Architecture Guide](ARCHITECTURE.md)** - System design and components
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[API Reference](QUICKSTART.md#api-endpoints)** - Endpoint documentation

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

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with clear commit messages
4. **Add** tests for new functionality
5. **Submit** a pull request with a description of changes

### Code Standards

- **Python**: Follow [PEP 8](https://pep8.org/) with [Black](https://github.com/psf/black) formatting
- **TypeScript**: Follow [ESLint](https://eslint.org/) config in `frontend/`
- **Documentation**: Keep README.md and QUICKSTART.md updated
- **Tests**: Add tests for new features

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

For issues, questions, or contributions:
- 📝 **Issues**: [GitHub Issues](https://github.com/arjvid805/debate-speech-coach/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/arjvid805/debate-speech-coach/discussions)
- 🤝 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini](https://ai.google.dev/), [OpenAI](https://openai.com/), and [Anthropic](https://www.anthropic.com/)
- Frontend with [React](https://react.dev/) and [Tailwind CSS](https://tailwindcss.com/)

---

**Made with ❤️ for better public speaking**
