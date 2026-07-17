# Practice Tests Guide

Practice test system for the MVA Podcast.

---

## Overview

The practice test system generates:

- **35 chapter tests** (1 per chapter)
- **1 full practice test** (100 questions)
- **Answer keys** with explanations

---

## Generate Tests

```bash
uv run python scripts/generate_practice_tests.py
```

**Output:** `obsidian-vault/04-Practice/`

---

## Test Structure

### Chapter Tests

Each chapter test includes:

- **25-30 questions** per chapter
- **Multiple choice** format (A-D)
- **Answer key** with explanations
- **Difficulty level** indicator

### Full Practice Test

- **100 questions** total
- **Covers all topics**
- **Timed format** (60 minutes)
- **Comprehensive answer key**

---

## File Structure

```
obsidian-vault/04-Practice/
├── Driver-Manual/
│   ├── Chapter-01-Test.md
│   ├── Chapter-01-Answer-Key.md
│   ├── Chapter-02-Test.md
│   ├── Chapter-02-Answer-Key.md
│   └── ...
├── Rookie-Manual/
│   ├── Chapter-01-Test.md
│   ├── Chapter-01-Answer-Key.md
│   └── ...
└── Full-Practice-Test/
    ├── Full-Practice-Test.md
    └── Full-Practice-Test-Answer-Key.md
```

---

## Question Format

### Sample Question

```
1. What is the legal BAC limit for drivers under 21 in Maryland?

A) 0.08%
B) 0.02%
C) 0.05%
D) 0.10%

Answer: B
Explanation: Maryland has a zero tolerance policy for drivers under 21.
Any detectable alcohol is illegal.
```

---

## Study Strategy

### Week 1-2
- Take chapter tests after studying each chapter
- Review wrong answers
- Retake until 90%+ score

### Week 3-4
- Take full practice test
- Identify weak areas
- Focus study on weak topics

### Week 5+
- Retake full practice test
- Take chapter tests for weak areas
- Aim for 95%+ on all tests

---

## Scoring

| Score | Rating |
|-------|--------|
| 90-100% | Excellent |
| 80-89% | Good |
| 70-79% | Fair |
| Below 70% | Needs Review |

---

## Regenerate Tests

To regenerate specific tests:

```bash
# Delete existing test
rm obsidian-vault/04-Practice/Driver-Manual/Chapter-01-Test.md
rm obsidian-vault/04-Practice/Driver-Manual/Chapter-01-Answer-Key.md

# Regenerate
uv run python scripts/generate_practice_tests.py
```

To regenerate all:

```bash
# Delete all tests
rm -rf obsidian-vault/04-Practice/

# Regenerate
uv run python scripts/generate_practice_tests.py
```

---

## Integration with Obsidian

### Create Study Decks

Convert questions to flashcards:

```markdown
---
tags: [flashcard]
---
Q: What is the legal BAC limit for drivers under 21?
A: 0.02% (zero tolerance)
```

### Use Spaced Repetition

Install Obsidian plugin "Spaced Repetition" to review questions over time.

---

## Related

- [OBSIDIAN-VAULT-GUIDE.md](OBSIDIAN-VAULT-GUIDE.md) - Vault setup
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
