# Maryland MVA Study Podcast

Audio review materials for the Maryland Driver's License Exam.

## Quick Start

```bash
# Install dependencies
uv sync

# Generate audio (if needed)
uv run python scripts/generate_audio.py

# Build podcast site
uv run python scripts/build_podcast.py

# Package Obsidian vault
uv run python scripts/package_vault.py
```

## Contents

- `source/` - Audio scripts (markdown)
- `output/` - Generated audio files (MP3)
- `docs/` - Netlify site (HTML, RSS, audio)
- `obsidian-vault/` - Obsidian vault with all materials
- `scripts/` - Generation pipeline

## Features

- 35 chapters (10 Driver + 25 Rookie Manual)
- TTS-optimized audio with natural pauses
- MVA-specific pronunciation guides
- RSS feed for podcast apps
- Netlify deployment for web access
- Obsidian vault for offline study

## Deployment

### GitHub Actions (Automatic)
1. Push to `main` branch
2. GitHub Actions generates audio
3. Deploys to Netlify automatically

### Manual Deploy
```bash
# Build site
uv run python scripts/build_podcast.py

# Deploy to Netlify
netlify deploy --dir=docs --prod
```

## Netlify Site

Once deployed, your site will be available at:
- **URL**: `https://your-site.netlify.app`
- **RSS Feed**: `https://your-site.netlify.app/feed.xml`

## Configuration

### Environment Variables
- `VOICE` - TTS voice (default: `en-US-GuyNeural`)
- `RATE` - Speech rate (default: `-5%`)

### GitHub Secrets (for CI/CD)
- `NETLIFY_AUTH_TOKEN` - Netlify personal access token
- `NETLIFY_SITE_ID` - Netlify site ID

## Requirements

- Python 3.10+
- uv (package manager)
- edge-tts
- ffmpeg (for audio conversion)

## License

MIT
