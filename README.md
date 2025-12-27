# Speech Analyzer and Coach 🎤

A tool I built to help with debate practice. It analyzes your speeches and gives feedback on pace, filler words, argument structure, and vocabulary.

**Built with help from my dad using AI coding tools (Microsoft Copilot)**

## Why I Made This

I'm on the speech and debate team, and coaches can't always listen to every practice speech. I wanted something that could give me immediate feedback when I'm practicing at home, so I built this with Python and React.

## What It Does

- **Pace Analysis**: Tells you if you're speaking too fast or too slow (optimal is 120-160 words per minute)
- **Filler Word Detection**: Counts things like "um," "like," "you know"
- **Argument Structure**: Uses AI to check if your thesis is clear and your points connect logically
- **Word Choice**: Suggests stronger alternatives for weak or repetitive words

You get a score out of 100 (25 points per category) with explanations for each.

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SpeechRecognition for transcription
- Supports multiple AI providers (Google Gemini, OpenAI GPT, Anthropic Claude)

**Frontend:**
- React with TypeScript
- Recharts for score visualization
- Basic CSS styling

## Project Structure

```
debate-speech-coach/
├── backend/
│   ├── main.py              # Main FastAPI app
│   ├── src/
│   │   ├── analyzers/       # Pace and filler word analysis
│   │   ├── ai/              # AI provider integrations
│   │   ├── models/          # Data structures
│   │   └── services/        # Audio transcription
│   └── uploads/             # Temporary audio files
└── frontend/
    └── src/
        ├── App.tsx          # Main React app
        ├── components/      # UI components
        └── services/        # API calls
```

## Getting Started

Check [QUICKSTART.md](QUICKSTART.md) for setup instructions.

You'll need:
- Python 3.9+
- Node.js 18+
- FFmpeg for audio processing
- At least one AI provider API key (Gemini is free)

## What I Learned

The hardest part was figuring out what kind of feedback actually helps debaters improve. I went through several versions of the scoring system before finding one that was constructive without being too harsh.

I also learned about trade-offs when building something - you can't add every feature you think of. You have to focus on what actually matters for the user.

## Current Status

This is a working prototype that I use for my own debate practice. It's not perfect, but it does what I needed it to do. The code could probably be cleaner in some places, but I'm still learning.

## Contributing

If you want to suggest improvements or report bugs, feel free to open an issue. I'm still learning a lot about software development, so any feedback is helpful.

## License

MIT License - feel free to use this for your own projects.

---

**Note:** Built as a learning project with help from AI coding tools. Some of the architecture decisions were influenced by my dad's experience in software engineering, but the core features and product decisions were things I figured out through testing and iteration.
