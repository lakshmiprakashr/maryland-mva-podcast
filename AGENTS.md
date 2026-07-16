# MVA Podcast — Process Documentation

## Objective

Build a complete Maryland MVA study system with:
1. Audio podcast for Apple Podcasts/Spotify
2. Obsidian vault for offline study
3. Practice tests with answer keys
4. GitHub Actions for automated deployment

---

## Project Structure

```
maryland-mva-podcast/
├── .github/workflows/
│   └── deploy-netlify.yml        # CI/CD pipeline
├── config/
│   └── podcast.yaml              # Voice/config settings
├── scripts/
│   ├── extract_text.py           # MD → clean TTS text
│   ├── generate_audio.py         # Text → MP3 via edge-tts
│   ├── podcast_generator.py      # RSS feed + episodes JSON
│   ├── package_vault.py          # Obsidian vault packager
│   ├── convert_audio_scripts.py  # JSON → markdown converter
│   └── generate_practice_tests.py # Practice test generator
├── source/                       # Audio scripts (markdown)
│   ├── Driver-Manual/
│   │   ├── Chapter-01/
│   │   │   ├── 01.Memorization-Sheet.md
│   │   │   ├── 02.Rapid-Recall-Drill.md
│   │   │   └── 06.Audio-Review-Script.md
│   │   └── ...
│   └── Rookie-Manual/
├── output/                       # Generated audio
│   ├── mp3/                      # 36 MP3 files
│   └── wav/                      # Temporary WAV files
├── podcast/                      # Netlify site
│   ├── Driver-Manual/            # 10 MP3 files
│   ├── Rookie-Manual/            # 25 MP3 files
│   ├── podcast.xml               # RSS feed (feedgen)
│   ├── episodes.json             # Episode metadata
│   ├── index.html                # Web player
│   └── artwork.jpg               # Podcast artwork
├── obsidian-vault/               # Obsidian vault
│   ├── .obsidian/                # Obsidian config
│   ├── 00-Overview/              # Welcome, study plan
│   ├── 01-Driver-Manual/         # 10 chapters
│   ├── 02-Rookie-Manual/         # 25 chapters
│   ├── 03-Audio/                 # 36 MP3 files
│   └── 04-Practice/              # Practice tests
├── pyproject.toml                # uv dependencies
├── netlify.toml                  # Netlify config
└── AGENTS.md                     # This file
```

---

## Quick Start Commands

### 1. Setup Environment
```bash
# Clone repository
git clone git@github.com:lakshmiprakashr/maryland-mva-podcast.git
cd maryland-mva-podcast

# Install dependencies
uv sync
```

### 2. Generate Audio (if needed)
```bash
# Extract text from markdown scripts
uv run python scripts/extract_text.py

# Generate MP3 audio files
uv run python scripts/generate_audio.py
```

### 3. Build Podcast
```bash
# Generate RSS feed and episodes JSON
uv run python scripts/podcast_generator.py \
  --base-url "https://mva-2tqlc3sd.netlify.app"

# Validate feed
uv run python scripts/podcast_generator.py --validate-only
```

### 4. Build Obsidian Vault
```bash
# Package vault with all materials
uv run python scripts/package_vault.py
```

### 5. Generate Practice Tests
```bash
# Generate practice tests from Rapid Recall Drills
uv run python scripts/generate_practice_tests.py
```

### 6. Convert Audio Scripts
```bash
# Convert JSON audio scripts to markdown
uv run python scripts/convert_audio_scripts.py
```

---

## Deployment

### Netlify (Primary)

**Site URL:** https://mva-2tqlc3sd.netlify.app

**RSS Feed:** https://mva-2tqlc3sd.netlify.app/podcast.xml

**Setup:**
1. Go to https://app.netlify.com
2. Import from Git → Select `lakshmiprakashr/maryland-mva-podcast`
3. Configure:
   - Branch: `main`
   - Build command: `echo 'Static site'`
   - Publish directory: `podcast`
4. Deploy

**GitHub Secrets Required:**
```
NETLIFY_AUTH_TOKEN=<your-netlify-token>
NETLIFY_SITE_ID=<your-site-id>
NETLIFY_SITE_NAME=mva-2tqlc3sd
```

### GitHub Pages (Alternative)

**URL:** https://lakshmiprakashr.github.io/maryland-mva-podcast

**Setup:**
1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. Workflow auto-deploys on push

---

## Apple Podcasts Submission

### Step 1: Validate RSS Feed
```bash
# Local validation
uv run python scripts/podcast_generator.py --validate-only

# Online validation
# Go to: https://cast feedvalidator.org/
# Enter: https://mva-2tqlc3sd.netlify.app/podcast.xml
```

### Step 2: Submit to Apple Podcasts Connect
1. Go to https://podcastsconnect.apple.com/
2. Sign in with Apple ID
3. Click "Add a Show" or "+"
4. Enter RSS feed URL:
   ```
   https://mva-2tqlc3sd.netlify.app/podcast.xml
   ```
5. Click "Submit"
6. Wait 24-48 hours for review

### Step 3: Apple Podcasts Requirements
- ✅ Valid RSS 2.0 feed with iTunes extensions
- ✅ Show artwork (1400x1400 minimum, 3000x3000 recommended)
- ✅ At least one episode published
- ✅ Episode titles and descriptions
- ✅ Audio files accessible via HTTPS

---

## Audio Generation

### Voice Configuration
```yaml
# config/podcast.yaml
voice: en-US-GuyNeural
rate: "-5%"
pitch: "+0Hz"
```

### Generate Audio
```bash
# Generate all audio files
uv run python scripts/generate_audio.py

# Audio files saved to:
# - output/mp3/ (final MP3 files)
# - output/wav/ (temporary WAV files)
```

### Audio Files
- **Driver Manual:** 10 chapters
- **Rookie Manual:** 25 chapters
- **Total:** 35 episodes
- **Voice:** en-US-GuyNeural (natural male voice)
- **Rate:** -5% (slightly slower for clarity)

---

## Obsidian Vault

### Package Vault
```bash
# Create vault with all materials
uv run python scripts/package_vault.py
```

### Vault Contents
- **00-Overview/** - Welcome page, study plan, requirements
- **01-Driver-Manual/** - 10 chapters with study materials
- **02-Rookie-Manual/** - 25 chapters with study materials
- **03-Audio/** - 36 MP3 files for listening
- **04-Practice/** - Practice tests with answer keys

### Each Chapter Contains
1. `01.Memorization-Sheet.md` - One-page high-yield review
2. `02.Rapid-Recall-Drill.md` - 20 practice questions
3. `06.Audio-Review-Script.md` - TTS-optimized script

---

## Practice Tests

### Generate Practice Tests
```bash
# Generate tests from Rapid Recall Drills
uv run python scripts/generate_practice_tests.py
```

### Test Structure
```
04-Practice/
├── Driver-Manual/
│   ├── Chapter-01-Test.md        # 20 questions
│   ├── Chapter-01-Answers.md     # Answer key
│   └── ...
├── Rookie-Manual/
│   ├── Chapter-01-Test.md
│   ├── Chapter-01-Answers.md
│   └── ...
├── Full-Practice-Test.md         # 50 questions
└── Full-Practice-Test-Answers.md
```

### Test Format
- **RECALL Questions:** Definitions, facts, laws
- **APPLICATION Questions:** Real-world scenarios
- **SYNTHESIS Questions:** Compare, contrast, relationships

---

## Source Materials

### Input Files
- `01-Source/Driver-Manual.pdf` - Official MD Driver's Manual
- `01-Source/Rookie-Manual.pdf` - Official MD Rookie Manual

### Extracted Chapters
- `02-Chapters/Driver-Manual/Chapter-01.md` to `Chapter-10.md`
- `02-Chapters/Rookie-Manual/Chapter-01.md` to `Chapter-25.md`

### Artifacts (Generated)
- `04-Artifacts/Driver-Manual/Chapter-01/` to `Chapter-10/`
- `04-Artifacts/Rookie-Manual/Chapter-01/` to `Chapter-25/`

---

## Common Commands

### Development
```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint code
uv run ruff check .

# Format code
uv run ruff format .
```

### Audio Generation
```bash
# Extract text
uv run python scripts/extract_text.py

# Generate audio
uv run python scripts/generate_audio.py

# Build podcast
uv run python scripts/podcast_generator.py

# Validate feed
uv run python scripts/podcast_generator.py --validate-only
```

### Deployment
```bash
# Build vault
uv run python scripts/package_vault.py

# Generate practice tests
uv run python scripts/generate_practice_tests.py

# Convert audio scripts
uv run python scripts/convert_audio_scripts.py
```

### Git Operations
```bash
# Check status
git status

# Stage changes
git add -A

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull
```

---

## Troubleshooting

### Audio Generation Fails
```bash
# Check edge-tts installation
uv pip list | grep edge-tts

# Reinstall if needed
uv pip install edge-tts --force-reinstall
```

### RSS Feed Validation Errors
```bash
# Regenerate feed
uv run python scripts/podcast_generator.py --rebuild

# Check XML syntax
xmllint --noout podcast/podcast.xml
```

### Netlify Deployment Issues
```bash
# Check build logs in Netlify dashboard
# Verify publish directory is "podcast"
# Ensure build command is: echo 'Static site'
```

### GitHub Actions Fails
```bash
# Check workflow runs
# Go to: https://github.com/lakshmiprakashr/maryland-mva-podcast/actions
# Review failed job logs
```

---

## Environment Variables

### Required for Local Development
```bash
# Optional: Override default voice
export VOICE=en-US-GuyNeural
export RATE=-5%
```

### Required for GitHub Actions
```
NETLIFY_AUTH_TOKEN=<your-token>
NETLIFY_SITE_ID=<your-site-id>
NETLIFY_SITE_NAME=mva-2tqlc3sd
```

---

## URLs Reference

### Production
- **Netlify Site:** https://mva-2tqlc3sd.netlify.app
- **RSS Feed:** https://mva-2tqlc3sd.netlify.app/podcast.xml
- **GitHub Repo:** https://github.com/lakshmiprakashr/maryland-mva-podcast

### Development
- **Local Site:** http://localhost:8888 (via Netlify CLI)
- **Local RSS:** http://localhost:8888/podcast.xml

---

## File Naming Conventions

### Audio Files
- `driver-manual-chapter-01.mp3` to `driver-manual-chapter-10.mp3`
- `rookie-manual-chapter-01.mp3` to `rookie-manual-chapter-25.mp3`

### Source Files
- `01.Memorization-Sheet.md` - One-page review
- `02.Rapid-Recall-Drill.md` - Practice questions
- `06.Audio-Review-Script.md` - TTS script

### Practice Tests
- `Chapter-01-Test.md` - Questions only
- `Chapter-01-Answers.md` - Answer key

---

## Dependencies

### Python Packages
```toml
[project.dependencies]
edge-tts = ">=6.1.0"
feedgen = ">=1.0.0"
mutagen = ">=1.47.0"
pyyaml = ">=6.0"
```

### System Requirements
- Python 3.10+
- uv (package manager)
- ffmpeg (for audio conversion)
- Git

---

## Memory-Optimized Summary

### Key Facts
- **35 total episodes** (10 Driver + 25 Rookie)
- **Voice:** en-US-GuyNeural at -5% rate
- **RSS Feed:** Valid RSS 2.0 with iTunes extensions
- **Hosting:** Netlify (primary), GitHub Pages (backup)
- **URL:** https://mva-2tqlc3sd.netlify.app

### Critical Commands
```bash
# Build everything
uv run python scripts/podcast_generator.py --base-url "https://mva-2tqlc3sd.netlify.app"
uv run python scripts/package_vault.py
uv run python scripts/generate_practice_tests.py

# Deploy
git add -A && git commit -m "Update" && git push
```

### Apple Podcasts RSS
```
https://mva-2tqlc3sd.netlify.app/podcast.xml
```

### GitHub Secrets
```
NETLIFY_AUTH_TOKEN
NETLIFY_SITE_ID
NETLIFY_SITE_NAME=mva-2tqlc3sd
```
