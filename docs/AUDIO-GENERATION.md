# Audio Generation Guide

Generate podcast audio from markdown scripts using edge-tts.

---

## Overview

The audio pipeline converts markdown audio scripts into MP3 files:

```
Markdown Scripts → Text Extraction → edge-tts → MP3 Files
```

---

## Prerequisites

```bash
# Install dependencies
uv sync
```

---

## Pipeline Steps

### Step 1: Extract Text from Markdown

```bash
uv run python scripts/extract_text.py
```

**Input:** `04-Artifacts/*/06.Audio-Review-Script.md`
**Output:** `podcast/Driver-Manual/*.txt` and `podcast/Rookie-Manual/*.txt`

### Step 2: Generate Audio

```bash
uv run python scripts/generate_audio.py
```

**Input:** `podcast/Driver-Manual/*.txt` and `podcast/Rookie-Manual/*.txt`
**Output:** `podcast/Driver-Manual/*.mp3` and `podcast/Rookie-Manual/*.mp3`

---

## Configuration

Voice and audio settings are in `config/podcast.yaml`:

```yaml
voice: en-US-GuyNeural
rate: -5%
output_format: audio-24khz-96kbitrate-mono-mp3
```

### Voice Options

| Voice | Description |
|-------|-------------|
| `en-US-GuyNeural` | Male, clear (current) |
| `en-US-JennyNeural` | Female, friendly |
| `en-US-AriaNeural` | Female, professional |

Change voice in `config/podcast.yaml` and regenerate.

---

## File Structure

```
podcast/
├── Driver-Manual/
│   ├── Chapter-01.txt      # Extracted text
│   ├── Chapter-01.mp3      # Generated audio
│   └── ...
└── Rookie-Manual/
    ├── Chapter-01.txt
    ├── Chapter-01.mp3
    └── ...
```

---

## Duration Estimation

| Manual | Chapters | Est. Duration |
|--------|----------|---------------|
| Driver | 10 | ~2 hours |
| Rookie | 25 | ~5 hours |
| **Total** | **35** | **~7 hours** |

---

## Troubleshooting

### "edge-tts not found"
```bash
uv sync
```

### Audio quality issues
- Check `config/podcast.yaml` settings
- Ensure sufficient disk space

### Slow generation
- Audio generation is sequential
- Each chapter takes 1-3 minutes
- Total time: ~30-60 minutes for all 35 chapters

---

## Regenerating Audio

To regenerate specific chapters:

```bash
# Delete existing MP3
rm podcast/Driver-Manual/Chapter-01.mp3

# Regenerate
uv run python scripts/generate_audio.py
```

To regenerate all:

```bash
# Delete all MP3s
find podcast -name "*.mp3" -delete

# Regenerate
uv run python scripts/generate_audio.py
```

---

## Next Steps

- [PODCAST-GENERATOR.md](PODCAST-GENERATOR.md) - Generate RSS feed
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
