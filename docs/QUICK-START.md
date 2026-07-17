# Quick Start Guide

Get up and running with the MVA Podcast in 5 minutes.

---

## Prerequisites

- Python 3.10+
- uv (package manager)
- Git

---

## 1. Clone Repository

```bash
git clone git@github.com:lakshmiprakashr/maryland-mva-podcast.git
cd maryland-mva-podcast
```

---

## 2. Install Dependencies

```bash
uv sync
```

---

## 3. Listen to Podcast

### Option A: Web Player (Recommended)
Go to: https://mva-2tqlc3sd.netlify.app

### Option B: Podcast App
Subscribe to RSS feed:
```
https://mva-2tqlc3sd.netlify.app/podcast.xml
```

### Option C: Obsidian Vault
```bash
# Package vault
uv run python scripts/package_vault.py

# Open in Obsidian
# File → Open folder as vault → select obsidian-vault/
```

---

## 4. Study with Practice Tests

```bash
# Generate practice tests
uv run python scripts/generate_practice_tests.py

# Tests are in: obsidian-vault/04-Practice/
```

---

## 5. Deploy Changes

```bash
# Make changes
# ...

# Deploy
git add -A
git commit -m "Your changes"
git push
```

---

## What's Included

- **35 Audio Episodes** (10 Driver + 25 Rookie Manual)
- **Obsidian Vault** with study materials
- **Practice Tests** with answer keys
- **Web Player** at https://mva-2tqlc3sd.netlify.app
- **RSS Feed** for podcast apps

---

## Next Steps

- Read [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) for deployment details
- Read [OBSIDIAN-VAULT-GUIDE.md](OBSIDIAN-VAULT-GUIDE.md) for vault usage
- Read [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) for Apple Podcasts submission
