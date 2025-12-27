# Speech Analyzer and Coach 🎤

A web app for analyzing debate speeches and public speaking. Records or uploads audio, transcribes it, and provides feedback on pace, filler words, argument structure, and vocabulary.

## What It Does

The app analyzes speeches across four areas and gives a score out of 100:

**Pace Analysis (25 points)**
- Measures words per minute
- Optimal range is 120-160 WPM
- Tells you if you're speaking too fast or too slow

**Filler Word Detection (25 points)**
- Counts "um," "like," "you know," and similar words
- Helps identify patterns to work on

**Argument Structure (25 points)**
- Evaluates thesis clarity
- Checks if supporting points connect logically
- Uses AI to assess overall flow

**Word Choice Analysis (25 points)**
- Identifies repetitive or weak language
- Suggests stronger alternatives
- Flags vague words that don't add value

Each category includes specific feedback explaining the score and areas to improve.

## Why I Built This

I'm on the speech and debate team, and coaches can't give feedback on every practice round. I wanted a tool that could analyze speeches when I'm practicing at home, so I could see what to work on between tournaments.

The main challenge was figuring out what kind of feedback actually helps debaters improve. Early versions of the scoring were too harsh and felt discouraging. After testing with my brother and adjusting based on feedback, the current system is more constructive while still being honest.

## Tech Stack

**Backend**
- FastAPI (Python web framework)
- SpeechRecognition library for audio transcription
- Multi-AI provider support: Google Gemini, OpenAI GPT, Anthropic Claude

**Frontend**
- React 19 with TypeScript
- Recharts for score visualization
- Standard CSS for styling

## Project Structure

```
debate-speech-coach/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── src/
│   │   ├── analyzers/       # Pace and filler word detection
│   │   ├── ai/              # AI provider integrations
│   │   ├── models/          # Data models
│   │   └── services/        # Transcription service
│   └── uploads/             # Temporary audio files
└── frontend/
    └── src/
        ├── App.tsx          # Main application
        ├── components/      # React components
        └── services/        # API client
```

## Getting Started

See [QUICKSTART.md](QUICKSTART.md) for setup instructions.

Requirements:
- Python 3.9+
- Node.js 18+
- FFmpeg (for audio processing)
- AI provider API key (Gemini is free and works well)

## What I Learned

Building this taught me about product decisions and trade-offs. You can't implement every feature idea—you have to focus on what actually matters for users. I went through several iterations on the scoring system before finding something that balanced being helpful with being honest.

I also learned that getting early feedback matters. Testing with real users (my brother and debate teammates) helped me catch problems I wouldn't have noticed on my own, like the initial scoring being too discouraging.

## Current Status

This is a working tool that I use for my own debate practice. The core features work reliably, but there's room for improvement in error handling and the UI. It does what I built it to do—give useful feedback on practice speeches.

## Contributing

If you find bugs or have suggestions, feel free to open an issue. I'm continuing to learn and improve this project.

## License

MIT License
