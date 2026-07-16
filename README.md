# Maryland MVA Study Podcast

Audio review materials for the Maryland Driver's License Exam.

## Quick Start

```bash
# Install dependencies
pip install edge-tts pyyaml

# Copy source audio scripts
cp -r ../Maryland-Driver-TSOS/04-Artifacts/* source/

# Generate audio
python scripts/extract_text.py
python scripts/generate_audio.py

# Build podcast
python scripts/build_podcast.py

# Package Obsidian vault
python scripts/package_vault.py
```

## Contents

- `source/` - Audio scripts from Maryland Driver's Manual
- `output/` - Generated audio files (WAV, MP3, SRT)
- `obsidian-vault/` - Ready-to-use Obsidian vault
- `scripts/` - Generation pipeline scripts

## Features

- 35 chapters (10 Driver + 25 Rookie Manual)
- TTS-optimized audio with natural pauses
- MVA-specific pronunciation guides
- RSS feed for podcast apps
- Obsidian vault with audio playback

## Requirements

- Python 3.10+
- edge-tts (`pip install edge-tts`)
- ffmpeg (for WAV to MP3 conversion)

## License

MIT
