# Podcast Generator

Generate RSS feed and episode metadata.

---

## Overview

The podcast generator creates:

- `podcast/podcast.xml` - RSS feed for podcast apps
- `podcast/episodes.json` - Episode metadata for web player

---

## Usage

```bash
# Generate with default base URL
uv run python scripts/podcast_generator.py

# Generate with custom base URL
uv run python scripts/podcast_generator.py \
  --base-url "https://mva-2tqlc3sd.netlify.app"
```

---

## Input

### Audio Files
```
podcast/Driver-Manual/Chapter-*.mp3
podcast/Rookie-Manual/Chapter-*.mp3
```

### Configuration
```yaml
# config/podcast.yaml
title: "Maryland MVA Study Podcast"
description: "Study materials for Maryland MVA tests"
author: "MVA Study Team"
```

---

## Output

### podcast.xml

RSS feed with:
- Channel metadata
- Episode listings
- iTunes tags
- Audio enclosures

### episodes.json

JSON with:
- Episode list
- Titles, descriptions
- Audio URLs
- Durations
- Chapter numbers

---

## How It Works

1. **Scan audio files** in `podcast/Driver-Manual/` and `podcast/Rookie-Manual/`
2. **Extract metadata** from filenames
3. **Calculate durations** from MP3 files
4. **Generate RSS XML** using feedgen library
5. **Generate JSON** for web player
6. **Write output files** to `podcast/`

---

## Metadata Extraction

### From Filename
```
Chapter-01.mp3 → Chapter number: 1
                 Section: Driver-Manual
```

### From Content
- Duration: Read from MP3 file
- Title: Generated from chapter number
- Description: Generated from chapter content

---

## Customization

### Change Title

Edit `config/podcast.yaml`:

```yaml
title: "My Custom Title"
```

### Change Description

Edit `config/podcast.yaml`:

```yaml
description: "My custom description"
```

### Change Author

Edit `config/podcast.yaml`:

```yaml
author: "My Name"
```

---

## Regeneration

To regenerate after adding new episodes:

```bash
# Delete existing files
rm podcast/podcast.xml
rm podcast/episodes.json

# Regenerate
uv run python scripts/podcast_generator.py \
  --base-url "https://mva-2tqlc3sd.netlify.app"
```

---

## Dependencies

```toml
[project]
dependencies = [
    "feedgen>=1.0.0",
    "mutagen>=1.47.0",
]
```

Install with:
```bash
uv sync
```

---

## Troubleshooting

### "feedgen not found"
```bash
uv sync
```

### "No audio files found"
- Ensure audio files exist in `podcast/Driver-Manual/` and `podcast/Rookie-Manual/`
- Check filenames match pattern `Chapter-*.mp3`

### "Invalid XML"
- Check for special characters in titles
- Ensure all required tags present

---

## Related

- [RSS-FEED-SPECIFICATION.md](RSS-FEED-SPECIFICATION.md) - Feed format
- [AUDIO-GENERATION.md](AUDIO-GENERATION.md) - Audio pipeline
- [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) - Apple submission
