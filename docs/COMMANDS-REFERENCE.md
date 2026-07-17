# Commands Reference

Quick copy-paste commands for the MVA Podcast project.

---

## Setup

```bash
# Clone repository
git clone git@github.com:lakshmiprakashr/maryland-mva-podcast.git
cd maryland-mva-podcast

# Install dependencies
uv sync

# Verify installation
uv run python --version
```

---

## Audio Generation

```bash
# Extract text from markdown
uv run python scripts/extract_text.py

# Generate audio files
uv run python scripts/generate_audio.py

# Check audio files exist
ls -la podcast/Driver-Manual/*.mp3
ls -la podcast/Rookie-Manual/*.mp3
```

---

## Podcast Generation

```bash
# Generate RSS feed and episodes JSON
uv run python scripts/podcast_generator.py \
  --base-url "https://mva-2tqlc3sd.netlify.app"

# Check generated files
ls -la podcast/podcast.xml
ls -la podcast/episodes.json
```

---

## Obsidian Vault

```bash
# Package vault for distribution
uv run python scripts/package_vault.py

# Check vault
ls -la obsidian-vault/
```

---

## Practice Tests

```bash
# Generate practice tests
uv run python scripts/generate_practice_tests.py

# Check tests
ls -la obsidian-vault/04-Practice/
```

---

## Deployment

```bash
# Commit changes
git add -A
git commit -m "Update podcast"

# Push to GitHub (triggers Netlify deployment)
git push

# Check deployment status
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/
```

---

## Validation

```bash
# Check RSS feed
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml | head -20

# Check all resources return 200
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/podcast.xml
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/episodes.json

# Check audio files
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/Driver-Manual/Chapter-01.mp3
```

---

## Maintenance

```bash
# Clear Netlify cache (if needed)
# Go to Netlify dashboard → Deploys → Clear cache

# Regenerate everything
rm -rf podcast/Driver-Manual/*.mp3
rm -rf podcast/Rookie-Manual/*.mp3
uv run python scripts/extract_text.py
uv run python scripts/generate_audio.py
uv run python scripts/podcast_generator.py --base-url "https://mva-2tqlc3sd.netlify.app"
```

---

## Quick One-Liners

```bash
# Check if podcast is working
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/

# Get episode count
curl -s https://mva-2tqlc3sd.netlify.app/episodes.json | python -c "import sys,json; print(len(json.load(sys.stdin)['episodes']))"

# Get total audio duration
curl -s https://mva-2tqlc3sd.netlify.app/episodes.json | python -c "import sys,json; print(sum(e['duration'] for e in json.load(sys.stdin)['episodes']))"
```

---

## Troubleshooting

```bash
# If uv sync fails
uv sync --refresh

# If audio generation fails
pip install edge-tts

# If podcast generator fails
pip install feedgen mutagen
```

---

## Related

- [AUDIO-GENERATION.md](AUDIO-GENERATION.md) - Audio pipeline details
- [PODCAST-GENERATOR.md](PODCAST-GENERATOR.md) - RSS feed generation
- [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) - Deployment setup
