# MVA Podcast Documentation Index

**Complete guide to the Maryland MVA Study Podcast**

---

## Quick Start (New Users)

**Start here if you're new:**

1. **[QUICK-START.md](QUICK-START.md)** (1 page)
   - Setup and first run
   - 5 minute read

2. **[DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)** (2 pages)
   - Netlify deployment steps
   - 10 minute read

**Then choose your workflow:**

- **Just want to listen?** → Use the [Netlify Site](https://mva-2tqlc3sd.netlify.app)
- **Want to study offline?** → See [Obsidian Vault Guide](#obsidian-vault)
- **Want to modify/regenerate?** → See [Development Guide](#development)
- **Want to submit to Apple Podcasts?** → See [Apple Podcasts Guide](#apple-podcasts)

---

## Documentation by Topic

### Deployment

**Deploying and hosting the podcast**

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) | Netlify + GitHub setup | 10 min |
| [NETLIFY-CONFIGURATION.md](NETLIFY-CONFIGURATION.md) | Netlify settings reference | 5 min |

**URLs:**
- Production: https://mva-2tqlc3sd.netlify.app
- RSS Feed: https://mva-2tqlc3sd.netlify.app/podcast.xml

---

### Apple Podcasts

**Submitting to Apple Podcasts and other platforms**

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) | Complete submission guide | 15 min |
| [RSS-FEED-SPECIFICATION.md](RSS-FEED-SPECIFICATION.md) | Feed format reference | 10 min |

---

### Development

**Building and modifying the project**

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [AUDIO-GENERATION.md](AUDIO-GENERATION.md) | Audio pipeline guide | 15 min |
| [PODCAST-GENERATOR.md](PODCAST-GENERATOR.md) | RSS feed generator | 10 min |
| [FILE-ORGANIZATION.md](FILE-ORGANIZATION.md) | Project structure | 10 min |

---

### Obsidian Vault

**Offline study with Obsidian**

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [OBSIDIAN-VAULT-GUIDE.md](OBSIDIAN-VAULT-GUIDE.md) | Vault setup and usage | 10 min |
| [PRACTICE-TESTS-GUIDE.md](PRACTICE-TESTS-GUIDE.md) | Practice test system | 10 min |

---

### Commands Reference

**Copy-paste commands**

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) | All commands | 5 min |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues | 10 min |

---

## Complete Documentation List

| Document | Category | Purpose |
|----------|----------|---------|
| [README.md](README.md) | Overview | Documentation index |
| [QUICK-START.md](QUICK-START.md) | Setup | Get started in 5 minutes |
| [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) | Deployment | Netlify + GitHub setup |
| [NETLIFY-CONFIGURATION.md](NETLIFY-CONFIGURATION.md) | Deployment | Netlify settings |
| [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) | Apple | Submission guide |
| [RSS-FEED-SPECIFICATION.md](RSS-FEED-SPECIFICATION.md) | Apple | Feed format |
| [AUDIO-GENERATION.md](AUDIO-GENERATION.md) | Development | Audio pipeline |
| [PODCAST-GENERATOR.md](PODCAST-GENERATOR.md) | Development | RSS feed generator |
| [FILE-ORGANIZATION.md](FILE-ORGANIZATION.md) | Development | Project structure |
| [OBSIDIAN-VAULT-GUIDE.md](OBSIDIAN-VAULT-GUIDE.md) | Obsidian | Vault setup |
| [PRACTICE-TESTS-GUIDE.md](PRACTICE-TESTS-GUIDE.md) | Obsidian | Practice tests |
| [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) | Commands | All commands |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Support | Common issues |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MVA Podcast System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Source    │    │   Scripts   │    │   Output    │     │
│  │  (MD files) │───▶│  (Python)   │───▶│  (MP3 files)│     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  01-Source  │    │  scripts/   │    │  podcast/   │     │
│  │  02-Chapters│    │  extract    │    │  Driver/    │     │
│  │  04-Artifacts    │  generate   │    │  Rookie/    │     │
│  └─────────────┘    │  podcast    │    │  podcast.xml│     │
│                     └─────────────┘    └─────────────┘     │
│                           │                  │             │
│                           ▼                  ▼             │
│                     ┌─────────────┐    ┌─────────────┐     │
│                     │   GitHub    │    │   Netlify   │     │
│                     │   Actions   │───▶│   Hosting   │     │
│                     └─────────────┘    └─────────────┘     │
│                                              │             │
│                                              ▼             │
│                                       ┌─────────────┐      │
│                                       │   Apple     │      │
│                                       │  Podcasts   │      │
│                                       └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Files

### Configuration
- `pyproject.toml` - Python dependencies (uv)
- `netlify.toml` - Netlify configuration
- `config/podcast.yaml` - Voice and audio settings

### Scripts
- `scripts/extract_text.py` - Extract text from markdown
- `scripts/generate_audio.py` - Generate MP3 from text
- `scripts/podcast_generator.py` - Generate RSS feed
- `scripts/package_vault.py` - Package Obsidian vault
- `scripts/generate_practice_tests.py` - Generate practice tests

### Deployment
- `.github/workflows/deploy-netlify.yml` - GitHub Actions workflow
- `podcast/` - Netlify site root

---

## Quick Reference

### Build Everything
```bash
# Install dependencies
uv sync

# Generate audio (if needed)
uv run python scripts/extract_text.py
uv run python scripts/generate_audio.py

# Build podcast
uv run python scripts/podcast_generator.py --base-url "https://mva-2tqlc3sd.netlify.app"

# Build vault
uv run python scripts/package_vault.py

# Generate practice tests
uv run python scripts/generate_practice_tests.py
```

### Deploy
```bash
# Commit and push
git add -A
git commit -m "Update"
git push
```

### Validate
```bash
# Check RSS feed
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml | head -20

# Check all resources
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/
```

---

## URLs

| Resource | URL |
|----------|-----|
| Netlify Site | https://mva-2tqlc3sd.netlify.app |
| RSS Feed | https://mva-2tqlc3sd.netlify.app/podcast.xml |
| GitHub Repo | https://github.com/lakshmiprakashr/maryland-mva-podcast |
| Episodes JSON | https://mva-2tqlc3sd.netlify.app/episodes.json |

---

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Process documentation (root)
- [README.md](../README.md) - Project overview (root)
