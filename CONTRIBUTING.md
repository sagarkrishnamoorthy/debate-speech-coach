# Contributing to Speech Analyzer and Coach

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.9+ (for backend development)
- Node.js 18+ (for frontend development)
- Git
- FFmpeg (for audio processing)
- One or more AI provider API keys (Gemini, OpenAI, or Anthropic)

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/debate-speech-coach.git
   cd debate-speech-coach
   ```

3. **Set up backend development environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Set up frontend development environment:**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Start development servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   python main.py --provider gemini

   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## Development Workflow

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

Example: `feature/add-export-pdf` or `bugfix/fix-cors-issue`

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Maintenance

**Examples:**
```
feat(backend): add real-time analysis endpoint
fix(frontend): resolve microphone permission issue
docs: update setup instructions for Windows
refactor(analyzers): simplify pace calculation logic
test(models): add tests for SpeechAnalysis validation
```

### Code Style

#### Python Backend

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting
- Use type hints for all functions
- Add docstrings to all public functions and classes

```python
def analyze_pace(transcription: str, duration_seconds: float) -> PaceAnalysis:
    """
    Analyze the pace of speech.
    
    Args:
        transcription: The speech transcription
        duration_seconds: Duration of the speech in seconds
        
    Returns:
        PaceAnalysis object with detailed metrics and feedback
        
    Raises:
        ValueError: If duration is zero or negative
    """
```

#### TypeScript/React Frontend

- Use [ESLint](https://eslint.org/) configuration in the project
- Add proper TypeScript types
- Document complex components with JSDoc comments
- Keep components focused and single-responsibility

```typescript
/**
 * Displays the overall speech score and breakdown by category.
 * @param analysis - The speech analysis results
 * @param onReset - Callback when user wants to analyze another speech
 */
export const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ analysis, onReset }) => {
  // Component implementation
};
```

## Testing

### Adding Tests

- Write tests for new features
- Update tests when modifying existing functionality
- Aim for meaningful test coverage, not 100%

### Running Tests

**Backend:**
```bash
cd backend
python -m pytest tests/
# Or with coverage:
python -m pytest --cov=src tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

## Documentation

### Updating Docs

When making changes that affect functionality:

1. Update [QUICKSTART.md](QUICKSTART.md) for setup/usage changes
2. Update [ARCHITECTURE.md](ARCHITECTURE.md) for architectural changes
3. Update [README.md](README.md) for major feature additions
4. Add inline code comments for complex logic

### Documentation Standards

- Use clear, concise language
- Include examples for complex features
- Keep API documentation in sync with code
- Update README badges if dependencies change

## Pull Request Process

1. **Create a pull request** from your branch to `main`

2. **PR Title Format:**
   ```
   [type] Brief description of changes
   ```
   Examples: `[feature] Add export PDF functionality`, `[fix] Resolve CORS error`

3. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of what changed and why.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Related Issues
   Closes #(issue number)

   ## Testing
   - [ ] I've tested on macOS/Linux/Windows (as applicable)
   - [ ] Manual testing completed
   - [ ] Unit tests added/updated

   ## Checklist
   - [ ] Code follows PEP 8 / ESLint rules
   - [ ] Documentation updated
   - [ ] No new warnings introduced
   - [ ] Commits are clean and descriptive
   ```

4. **Code Review:**
   - At least one maintainer must review
   - Address review comments
   - Respond to all feedback

5. **Merge:**
   - Squash or rebase commits if needed
   - Ensure CI/CD passes
   - Maintainer merges when approved

## Reporting Bugs

### Before Submitting

- Check [existing issues](https://github.com/arjvid805/debate-speech-coach/issues)
- Check [discussions](https://github.com/arjvid805/debate-speech-coach/discussions)
- Try reproducing with the latest code

### Bug Report Template

**Title:** Brief description of bug

**Description:**
```markdown
## Describe the Bug
Clear description of what's happening.

## Steps to Reproduce
1. Step one
2. Step two
3. Bug occurs

## Expected Behavior
What should happen instead.

## Environment
- OS: (macOS/Linux/Windows)
- Python version: 
- Node version:
- Browser (if frontend): 
- AI Provider: (Gemini/OpenAI/Anthropic)

## Error Message/Logs
```
Stack trace or error output
```

## Additional Context
Any other relevant information.
```

## Feature Requests

### Suggesting Enhancements

**Title:** Brief description of feature

**Description:**
```markdown
## Problem Statement
What problem does this solve?

## Proposed Solution
How should it work?

## Alternative Solutions
Other approaches considered?

## Additional Context
Relevant examples or resources.
```

## Project Structure

```
debate-speech-coach/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── analyzers/      # Analysis modules
│   │   ├── ai/             # AI provider integrations
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── config.py       # Configuration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── tests/             # Backend tests
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── App.tsx        # Main app
│   ├── package.json       # Node dependencies
│   └── tests/            # Frontend tests
├── docs/                   # Additional documentation
├── README.md              # Project overview
├── QUICKSTART.md          # Setup guide
├── ARCHITECTURE.md        # Architecture documentation
└── CONTRIBUTING.md        # This file
```

## Key Areas for Contribution

### High Priority
- Database integration for persistent storage
- User authentication and profiles
- Improved error handling and validation
- Comprehensive test coverage

### Medium Priority
- Real-time analysis during recording
- Export reports as PDF
- Historical trend analysis
- Performance optimizations

### Low Priority (Nice to Have)
- Additional language support
- Custom vocabulary databases
- Multi-speaker detection
- UI/UX enhancements

## Questions?

- 💬 **Ask in Discussions:** [GitHub Discussions](https://github.com/arjvid805/debate-speech-coach/discussions)
- 📧 **Email:** (contact info if available)
- 📖 **Read the Docs:** [ARCHITECTURE.md](ARCHITECTURE.md)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub automatically tracks contributions

Thank you for making Speech Analyzer and Coach better! 🚀
