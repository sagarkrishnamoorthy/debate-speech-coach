# Quick Start Guide

Get the Speech Analyzer up and running in minutes!

## Prerequisites

### System Requirements
- **Python 3.9 or higher**
- **Node.js 18 or higher**
- **FFmpeg** (for audio conversion)

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### API Keys

You'll need at least one AI provider API key:

- **Gemini (Google)**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd debate-speech-coach/backend
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate it:
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

DEFAULT_AI_PROVIDER=gemini
```

**Note**: You only need the API key for the provider you plan to use.

### 5. Start the Backend Server

**Using npm (recommended):**
```bash
npm start                    # Default: Gemini on port 8000
# OR choose a specific provider:
npm run dev:gemini          # Gemini (Google)
npm run dev:openai          # OpenAI GPT
npm run dev:claude          # Anthropic Claude
```

**Using Python directly:**
```bash
python main.py                      # Default: Gemini
python main.py --provider openai    # OpenAI
python main.py --provider anthropic # Anthropic
python main.py --port 8080          # Custom port
```

The backend will start at `http://localhost:8000` (or your specified port).

## Frontend Setup

### 1. Open New Terminal and Navigate to Frontend
```bash
cd debate-speech-coach/frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

The app will open at `http://localhost:3000`

## First Speech Analysis

### Option 1: Record Live

1. Open `http://localhost:3000` in your browser
2. Select your AI provider (Gemini, GPT, or Claude)
3. Click **"Start Recording"**
4. Grant microphone permissions when prompted
5. Speak for at least 30 seconds (1-2 minutes recommended)
6. Click **"Stop Recording"**
7. Click **"Analyze Speech"**
8. Wait for results (typically 30-60 seconds)

### Option 2: Upload Audio File

1. Open `http://localhost:3000`
2. Select your AI provider
3. Click **"Upload Audio File"** or drag and drop
4. Select an MP3, WAV, OGG, M4A, or FLAC file
5. Click **"Analyze Speech"**
6. Wait for results

## Understanding Your Results

### Overall Score (1-100)
- **80-100**: Excellent
- **60-79**: Good
- **40-59**: Fair
- **0-39**: Needs Work

### Score Components

**Pace Score (25 points)**
- Optimal: 120-160 words per minute
- Too slow: < 120 WPM
- Too fast: > 160 WPM

**Clarity Score (25 points)**
- Based on filler words per minute
- < 2 fillers/min: Excellent
- 2-5 fillers/min: Good
- 5-10 fillers/min: Fair
- > 10 fillers/min: Needs work

**Structure Score (25 points)**
- Clear thesis/main argument
- Supporting points
- Logical flow
- Conclusion

**Vocabulary Score (25 points)**
- Word variety
- Strong vs. weak words
- Avoidance of repetition

## Troubleshooting

### "Could not access microphone"
- Grant microphone permissions in your browser
- Check system privacy settings
- Try a different browser (Chrome/Edge recommended)

### "Transcription service error"
- Check your internet connection
- Ensure audio quality is clear
- Reduce background noise

### "API key error"
- Verify API key is correctly set in `.env`
- Check that the API key has proper permissions
- Ensure you're using the correct provider flag

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>

# Or use a different port
python main.py --port 8080
```

### Frontend won't start
```bash
# Clear npm cache
npm cache clean --force

# Remove and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Testing the System

### Test with Sample Speech

Record or upload a speech with these characteristics for best results:

**Good Test Speech:**
- Duration: 1-3 minutes
- Clear audio quality
- Structured argument (intro, body, conclusion)
- Natural speaking pace
- Minimal background noise

**Sample Topics:**
- "Why everyone should learn public speaking"
- "The importance of renewable energy"
- "How technology has changed education"

## Next Steps

### Improve Your Scores

1. **Practice Pace**: Use a metronome or timer
2. **Reduce Fillers**: Record yourself and note patterns
3. **Structure Practice**: Write outlines before speaking
4. **Expand Vocabulary**: Read widely and note strong words

### Track Progress

1. Save your scores
2. Analyze similar speeches over time
3. Focus on one component at a time
4. Celebrate improvements!

### Advanced Usage

**Compare AI Providers:**
```bash
# Start backend with different providers (in separate terminals)
npm run dev:gemini
npm run dev:openai
npm run dev:claude

# Or using Python directly:
python main.py --provider gemini
python main.py --provider openai
python main.py --provider anthropic
```

**Batch Analysis:**
- Upload multiple speeches
- Compare scores side-by-side
- Identify consistent patterns

## Support

If you encounter issues:

1. Check the logs in `backend/logs/app.log`
2. Verify all dependencies are installed
3. Ensure API keys are valid
4. Check that FFmpeg is installed correctly

## Tips for Best Results

✅ **Do:**
- Speak clearly and at a natural pace
- Use a good quality microphone
- Record in a quiet environment
- Structure your speech with intro, body, conclusion
- Aim for 1-3 minutes of speech

❌ **Avoid:**
- Background noise or music
- Speaking too fast or too slow
- Very short speeches (< 30 seconds)
- Poor audio quality
- Multiple speakers (for now)

---

**Ready to improve your speaking skills? Start analyzing! 🎤**
