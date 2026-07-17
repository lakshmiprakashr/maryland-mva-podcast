# Obsidian Vault Guide

Use the Obsidian vault for offline studying.

---

## What's Included

- **35 chapters** (10 Driver + 25 Rookie)
- **Study materials** for each chapter:
  - Master Memorization Sheet
  - Rapid Recall Drill
  - Audio Review Script
- **Practice tests** with answer keys
- **Web player** integration

---

## Setup

### 1. Package Vault

```bash
uv run python scripts/package_vault.py
```

### 2. Open in Obsidian

1. Open Obsidian
2. File → Open folder as vault
3. Select `obsidian-vault/`

---

## Vault Structure

```
obsidian-vault/
├── .obsidian/                    # Obsidian configuration
├── 00-Overview/
│   ├── README.md                 # Index page
│   ├── Driver-Manual-Index.md    # Driver chapters
│   └── Rookie-Manual-Index.md    # Rookie chapters
├── Driver-Manual/
│   ├── Chapter-01/
│   │   ├── Chapter-01.md         # Source text
│   │   ├── 04.Master-Memorization-Sheet.md
│   │   ├── 05.Rapid-Recall-Drill.md
│   │   └── 06.Audio-Review-Script.md
│   └── ...
├── Rookie-Manual/
│   ├── Chapter-01/
│   │   └── ...
│   └── ...
└── 04-Practice/
    ├── Driver-Manual/
    │   ├── Chapter-01-Test.md
    │   ├── Chapter-01-Answer-Key.md
    │   └── ...
    ├── Rookie-Manual/
    │   └── ...
    └── Full-Practice-Test/
        ├── Full-Practice-Test.md
        └── Full-Practice-Test-Answer-Key.md
```

---

## Study Workflow

### Daily Study Routine

1. **Open vault** in Obsidian
2. **Review chapter** using source text
3. **Study memorization sheet** (04 file)
4. **Test yourself** with rapid recall drill (05 file)
5. **Listen to audio** review script (06 file)
6. **Take practice test** at end of week

### Week-by-Week Plan

| Week | Focus | Chapters |
|------|-------|----------|
| 1 | Driver Manual basics | 1-3 |
| 4 | Driver Manual rules | 4-7 |
| 7 | Driver Manual advanced | 8-10 |
| 9 | Rookie Manual basics | 1-8 |
| 12 | Rookie Manual procedures | 9-16 |
| 15 | Rookie Manual advanced | 17-25 |

---

## Features

### Wiki Links

Chapters are linked with Obsidian wiki links:

```markdown
[[Chapter-01|Chapter 1: The Maryland DMV]]
```

### Tags

Use tags for organization:

```markdown
#driver-manual #rookie-manual #practice-test
```

### Graph View

See connections between chapters in Obsidian's graph view.

---

## Practice Tests

Located in `04-Practice/`:

### Chapter Tests
- 25-30 questions per chapter
- Multiple choice format
- Answer key with explanations

### Full Practice Test
- 100 questions total
- Covers all topics
- Timed format (60 minutes)

---

## Offline Access

The vault works completely offline:

- All text files are local
- Audio files can be downloaded from Netlify
- No internet required for studying

### Download Audio for Offline

```bash
# Download all audio
cd obsidian-vault
mkdir -p audio
curl -s https://mva-2tqlc3sd.netlify.app/episodes.json | \
  python -c "
import sys, json, subprocess
data = json.load(sys.stdin)
for ep in data['episodes']:
    url = ep['audio_url']
    filename = url.split('/')[-1]
    subprocess.run(['curl', '-s', '-o', f'audio/{filename}', url])
"
```

---

## Tips

### Use Obsidian Plugins
- **Spaced Repetition**: Review cards over time
- **Calendar**: Track study sessions
- **Templater**: Create study templates

### Create Study Decks
Convert rapid recall drills to flashcards using Obsidian's built-in flashcard plugin.

### Link Related Topics
Use `[[wiki links]]` to connect related concepts across chapters.

---

## Troubleshooting

### Vault won't open
- Ensure `.obsidian/` folder exists
- Try creating new vault and copying files

### Audio won't play
- Audio files need to be downloaded separately
- See "Download Audio for Offline" section

### Missing files
- Re-run `uv run python scripts/package_vault.py`

---

## Related

- [PRACTICE-TESTS-GUIDE.md](PRACTICE-TESTS-GUIDE.md) - Practice test system
- [FILE-ORGANIZATION.md](FILE-ORGANIZATION.md) - Project structure
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
