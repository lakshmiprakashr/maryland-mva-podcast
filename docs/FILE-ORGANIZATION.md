# File Organization Guide

Project structure and organization.

---

## Directory Structure

```
maryland-mva-podcast/
├── README.md                          # Project overview
├── AGENTS.md                          # Process documentation
├── pyproject.toml                     # Python dependencies (uv)
├── netlify.toml                       # Netlify configuration
│
├── 01-Source/                         # Source PDFs
│   ├── Maryland_Driver_Manual.pdf
│   └── Maryland_Rookie_Manual.pdf
│
├── 02-Chapters/                       # Extracted markdown
│   ├── Driver-Manual/
│   │   ├── Chapter-01.md
│   │   └── ...
│   └── Rookie-Manual/
│       ├── Chapter-01.md
│       └── ...
│
├── 04-Artifacts/                      # Generated study materials
│   ├── Driver-Manual/
│   │   ├── Chapter-01/
│   │   │   ├── 04.Master-Memorization-Sheet.md
│   │   │   ├── 05.Rapid-Recall-Drill.md
│   │   │   └── 06.Audio-Review-Script.md
│   │   └── ...
│   └── Rookie-Manual/
│       ├── Chapter-01/
│       │   └── ...
│       └── ...
│
├── podcast/                           # Netlify site root
│   ├── index.html                     # Web player
│   ├── podcast.xml                    # RSS feed
│   ├── episodes.json                  # Episode metadata
│   ├── artwork.jpg                    # Podcast artwork (1400x1400)
│   ├── Driver-Manual/
│   │   ├── Chapter-01.txt             # Text for TTS
│   │   ├── Chapter-01.mp3             # Audio file
│   │   └── ...
│   └── Rookie-Manual/
│       ├── Chapter-01.txt
│       ├── Chapter-01.mp3
│       └── ...
│
├── scripts/                           # Python scripts
│   ├── extract_text.py                # Markdown → text
│   ├── generate_audio.py              # Text → MP3
│   ├── podcast_generator.py           # Generate RSS feed
│   ├── package_vault.py               # Package Obsidian vault
│   ├── generate_practice_tests.py     # Generate practice tests
│   └── convert_audio_scripts.py       # JSON → markdown
│
├── obsidian-vault/                    # Obsidian vault
│   ├── .obsidian/                     # Obsidian config
│   ├── 00-Overview/                   # Index pages
│   ├── Driver-Manual/                 # Driver chapters + artifacts
│   ├── Rookie-Manual/                 # Rookie chapters + artifacts
│   └── 04-Practice/                   # Practice tests
│
├── config/                            # Configuration
│   └── podcast.yaml                   # Voice settings
│
├── docs/                              # Documentation
│   ├── README.md
│   ├── QUICK-START.md
│   ├── DEPLOYMENT-GUIDE.md
│   └── ...
│
└── .github/workflows/                 # GitHub Actions
    └── deploy-netlify.yml
```

---

## Key Files

### Configuration
| File | Purpose |
|------|---------|
| `pyproject.toml` | Python dependencies |
| `netlify.toml` | Netlify build settings |
| `config/podcast.yaml` | Voice and audio settings |

### Scripts
| File | Purpose |
|------|---------|
| `scripts/extract_text.py` | Extract text from markdown |
| `scripts/generate_audio.py` | Generate MP3 files |
| `scripts/podcast_generator.py` | Generate RSS feed |
| `scripts/package_vault.py` | Package Obsidian vault |
| `scripts/generate_practice_tests.py` | Generate practice tests |

### Deployment
| File | Purpose |
|------|---------|
| `.github/workflows/deploy-netlify.yml` | CI/CD workflow |
| `podcast/` | Netlify site root |

---

## File Naming Conventions

### Audio Files
```
Driver-Manual/Chapter-01.mp3
Rookie-Manual/Chapter-01.mp3
```

### Text Files
```
Driver-Manual/Chapter-01.txt
Rookie-Manual/Chapter-01.txt
```

### Chapter Numbers
- Driver Manual: 01-10
- Rookie Manual: 01-25

---

## Data Flow

```
01-Source/PDFs
    ↓ (manual extraction)
02-Chapters/Markdown
    ↓ (04-Artifacts generation)
04-Artifacts/Audio Scripts
    ↓ (extract_text.py)
podcast/Text Files
    ↓ (generate_audio.py)
podcast/MP3 Files
    ↓ (podcast_generator.py)
podcast/podcast.xml
    ↓ (GitHub Actions)
Netlify Site
```

---

## Related

- [QUICK-START.md](QUICK-START.md) - Get started
- [AUDIO-GENERATION.md](AUDIO-GENERATION.md) - Audio pipeline
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
