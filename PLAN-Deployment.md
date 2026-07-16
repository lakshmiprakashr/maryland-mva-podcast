# MVA Audio Deployment Plan

## Current State

✅ **All audio files generated:**
- 36 MP3 files (10 Driver + 25 Rookie + 1 Full Practice)
- Location: `output/mp3/`
- Voice: `en-US-GuyNeural`
- Rate: `-5%`

## Goal

Deploy MVA audio to GitHub with automated generation and Netlify hosting.

---

## Phase 1: GitHub Repository Setup

### 1.1 Repository Structure
```
maryland-mva-podcast/
├── .github/
│   └── workflows/
│       └── generate-audio.yml      # GitHub Actions
├── config/
│   └── podcast.yaml                # Voice/config settings
├── scripts/
│   ├── extract_text.py             # MD → clean text
│   ├── generate_audio.py           # Text → MP3
│   ├── build_podcast.py            # RSS feed
│   └── package_vault.py            # Obsidian vault
├── source/                         # Audio scripts (markdown)
│   ├── Driver-Manual/
│   │   ├── Chapter-01/
│   │   │   └── 06.Audio-Review-Script.md
│   │   └── ...
│   └── Rookie-Manual/
├── output/                         # Generated audio
│   ├── mp3/                        # 36 MP3 files
│   ├── wav/                        # Temporary WAV files
│   └── srt/                        # Subtitle files
├── docs/                           # Netlify site
│   ├── index.html                  # Landing page
│   ├── player.html                 # Audio player
│   ├── feed.xml                    # RSS podcast feed
│   └── audio/                      # Symlink to output/mp3
├── pyproject.toml                  # uv dependencies
└── README.md
```

### 1.2 Git Setup
```bash
# Initialize git
cd /home/lpq/projects/maryland-mva-podcast
git init
git branch -M main

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.pyc
.venv/

# Generated files (keep in git for deployment)
# output/mp3/

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add -A
git commit -m "Initial commit: MVA podcast with 35 chapters"
```

---

## Phase 2: GitHub Actions Workflow

### 2.1 Workflow File (`.github/workflows/generate-audio.yml`)

```yaml
name: Generate MVA Podcast

on:
  push:
    branches: [main]
    paths:
      - 'source/**/*.md'
      - 'scripts/**'
      - 'config/**'
  workflow_dispatch:
    inputs:
      chapter:
        description: 'Specific chapter to regenerate'
        required: false

jobs:
  generate-audio:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      
      - name: Set up Python
        run: uv python install 3.12
      
      - name: Install dependencies
        run: uv sync
      
      - name: Install ffmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg
      
      - name: Generate audio files
        run: uv run python scripts/generate_audio.py
        env:
          VOICE: en-US-GuyNeural
          RATE: -5%
      
      - name: Build podcast feed
        run: uv run python scripts/build_podcast.py
      
      - name: Upload MP3 artifacts
        uses: actions/upload-artifact@v4
        with:
          name: mva-audio-${{ github.sha }}
          path: output/mp3/*.mp3
          retention-days: 90
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: ./docs
          production-deploy: true
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy audio ${{ github.sha }}"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---

## Phase 3: Netlify Setup

### 3.1 Netlify Site Structure (`docs/`)

**`docs/index.html`** - Landing page:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maryland MVA Study Podcast</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
               max-width: 800px; margin: 0 auto; padding: 20px; }
        .chapter { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .chapter h3 { margin-top: 0; }
        audio { width: 100%; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Maryland MVA Study Podcast</h1>
    <p>Audio review materials for the Maryland Driver's License Exam.</p>
    
    <h2>Driver's Manual</h2>
    <div id="driver-chapters"></div>
    
    <h2>Rookie Manual</h2>
    <div id="rookie-chapters"></div>
    
    <script>
        // Load chapters dynamically
        fetch('/audio/manifest.json')
            .then(r => r.json())
            .then(data => {
                // Render chapters
            });
    </script>
</body>
</html>
```

**`docs/feed.xml`** - RSS Podcast Feed:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Maryland MVA Study Podcast</title>
    <description>Audio review for Maryland Driver's License Exam</description>
    <language>en-us</language>
    <itunes:author>MVA Study Guide</itunes:author>
    <!-- Episodes -->
  </channel>
</rss>
```

### 3.2 Netlify Configuration (`netlify.toml`)

```toml
[build]
  publish = "docs"
  command = "echo 'Static site'"

[[redirects]]
  from = "/audio/*"
  to = "/.netlify/functions/audio/:splat"
  status = 200

[[headers]]
  for = "/audio/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Cache-Control = "public, max-age=31536000"
```

---

## Phase 4: Secrets Configuration

### 4.1 Required GitHub Secrets

| Secret | Description | How to Get |
|--------|-------------|------------|
| `NETLIFY_AUTH_TOKEN` | Netlify personal access token | Netlify → User Settings → Applications |
| `NETLIFY_SITE_ID` | Netlify site ID | Netlify → Site → Settings → General |

### 4.2 Setup Commands
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Create site
netlify init

# Get site ID
netlify env:list
```

---

## Phase 5: Deployment Steps

### 5.1 Initial Setup
```bash
cd /home/lpq/projects/maryland-mva-podcast

# Create pyproject.toml for uv
cat > pyproject.toml << EOF
[project]
name = "maryland-mva-podcast"
version = "0.1.0"
description = "Maryland MVA Study Podcast"
requires-python = ">=3.10"
dependencies = [
    "edge-tts>=6.1.0",
    "pyyaml>=6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF

# Install dependencies with uv
uv sync

# Create docs directory
mkdir -p docs/audio

# Copy MP3 files to docs
cp output/mp3/*.mp3 docs/audio/

# Generate manifest
uv run python scripts/build_podcast.py
```

### 5.2 Git Push
```bash
# Add remote
git remote add origin https://github.com/USERNAME/maryland-mva-podcast.git

# Push
git push -u origin main
```

### 5.3 Netlify Deploy
```bash
# Manual deploy (first time)
netlify deploy --dir=docs --prod

# Or connect to GitHub for auto-deploy
```

---

## Phase 6: Verification

### 6.1 Test Checklist
- [ ] GitHub Actions runs successfully
- [ ] MP3 files are uploaded as artifacts
- [ ] Netlify site is accessible
- [ ] Audio player works
- [ ] RSS feed validates
- [ ] Podcast apps can subscribe

### 6.2 URLs
- **GitHub**: `https://github.com/USERNAME/maryland-mva-podcast`
- **Netlify**: `https://your-site.netlify.app`
- **RSS Feed**: `https://your-site.netlify.app/feed.xml`

---

## Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Audio Files | ✅ 36 MP3s | Ready to deploy |
| GitHub Actions | ⏳ To create | Uses uv |
| Netlify Site | ⏳ To create | Static hosting |
| RSS Feed | ⏳ To create | For podcast apps |

## Next Steps

1. Create `pyproject.toml` for uv
2. Update GitHub Actions workflow
3. Create Netlify site
4. Push to GitHub
5. Verify deployment
