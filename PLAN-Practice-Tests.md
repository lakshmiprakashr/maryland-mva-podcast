# Practice Tests Implementation Plan

## Overview

The `04-Practice/` folder is empty. This plan outlines creating practice tests with answer keys for all 35 chapters.

## Current State

- **Rapid Recall Drills** exist in each chapter folder with 20 questions each
- Questions include: RECALL (8), APPLICATION (8), SYNTHESIS (4)
- Answers are embedded in the same file

## Implementation Plan

### Phase 1: Extract Questions from Existing Drills

Create a script to extract questions from Rapid Recall Drills and separate them into:
- **Test versions** (questions only, no answers)
- **Answer keys** (answers with explanations)

### Phase 2: Generate Practice Tests

Create the following for each chapter:

```
04-Practice/
├── Driver-Manual/
│   ├── Chapter-01-Test.md          # Questions only
│   ├── Chapter-01-Answers.md       # Answers with explanations
│   ├── Chapter-02-Test.md
│   ├── Chapter-02-Answers.md
│   └── ...
├── Rookie-Manual/
│   ├── Chapter-01-Test.md
│   ├── Chapter-01-Answers.md
│   └── ...
├── Full-Practice-Test.md           # 50-question comprehensive test
├── Full-Practice-Test-Answers.md
├── Road-Signs-Gallery.md           # Visual sign identification
└── Common-Questions.md             # Most frequently tested topics
```

### Phase 3: Test Formats

#### Format A: Chapter Test (20 questions)
```markdown
# Chapter 01: Driving Tests Requirements — Practice Test

## Instructions
- 20 questions
- 25 minutes recommended
- No answers visible until you complete

## Questions

1. What are the three licensing requirements?
   - A) Vision screening, written test, road test
   - B) Vision screening, knowledge test, driving skills test
   - C) Knowledge test, driving skills test, medical exam
   - D) Vision screening, knowledge test, medical exam

2. What is the minimum visual acuity required?
   - A) 20/20 in each eye
   - B) 20/40 in each eye
   - C) 20/40 combined
   - D) 20/30 in each eye

[Continue for 20 questions...]
```

#### Format B: Answer Key (separate file)
```markdown
# Chapter 01: Driving Tests Requirements — Answer Key

## Question 1
**Correct Answer:** B) Vision screening, knowledge test, driving skills test

**Explanation:** Maryland requires all three tests. The vision screening is separate from the knowledge test.

**Common Mistake:** Option A says "written test" instead of "knowledge test" and omits that vision screening is distinct.

---

## Question 2
**Correct Answer:** B) 20/40 in each eye

**Explanation:** The requirement is 20/40 acuity in EACH eye individually, not combined.

**Common Mistake:** Option C suggests combined vision, but Maryland requires each eye separately.

[Continue for all questions...]
```

#### Format C: Full Practice Test (50 questions)
- Mix of questions from all Driver Manual chapters
- Simulates actual MVA knowledge test format
- 50 questions, 45 minutes

#### Format D: Road Signs Gallery
```markdown
# Maryland Road Signs — Visual Guide

## Regulatory Signs (Red/White)

### Stop Sign
![Stop Sign](images/stop-sign.png)
- **Shape:** Octagon
- **Color:** Red background, white text
- **Meaning:** Come to a complete stop
- **Test Tip:** Only sign with octagon shape

### Yield Sign
![Yield Sign](images/yield-sign.png)
- **Shape:** Triangle (inverted)
- **Color:** Red border, white background
- **Meaning:** Slow down, prepare to stop
```

## Implementation Steps

### Step 1: Create Test Generator Script
```python
# scripts/generate_practice_tests.py

def extract_questions_from_drill(drill_path):
    """Extract questions and answers from Rapid Recall Drill."""
    # Parse markdown to separate Q&A
    
def generate_test_version(questions):
    """Create test with questions only (multiple choice format)."""
    
def generate_answer_key(questions, answers):
    """Create answer key with explanations."""
    
def generate_full_practice_test(all_questions):
    """Create comprehensive 50-question test."""
```

### Step 2: Generate Chapter Tests
- Extract from 35 Rapid Recall Drills
- Convert to multiple choice format
- Create separate answer keys

### Step 3: Generate Comprehensive Materials
- Full 50-question practice test
- Road signs visual gallery
- Common questions compilation

## File Structure After Implementation

```
04-Practice/
├── README.md                          # How to use practice tests
├── Driver-Manual/
│   ├── Chapter-01-Test.md            # 20 questions
│   ├── Chapter-01-Answers.md         # Answer key
│   ├── Chapter-02-Test.md
│   ├── Chapter-02-Answers.md
│   ├── ... (10 chapters × 2 files = 20 files)
├── Rookie-Manual/
│   ├── Chapter-01-Test.md
│   ├── Chapter-01-Answers.md
│   ├── ... (25 chapters × 2 files = 50 files)
├── Full-Practice-Test.md             # 50 questions
├── Full-Practice-Test-Answers.md
├── Road-Signs-Gallery.md
└── Common-Questions.md
```

## Estimated Output
- Chapter Tests: 35 tests × 20 questions = 700 questions
- Full Practice Test: 50 questions
- Total: 750+ practice questions with answers

## Timeline
1. **Step 1**: Create test generator script (10 min)
2. **Step 2**: Generate all chapter tests (15 min)
3. **Step 3**: Create comprehensive materials (10 min)
4. **Step 4**: Package and commit (5 min)

## Success Criteria
- [ ] Each chapter has a test file and answer key
- [ ] Questions are in multiple choice format
- [ ] Answers include explanations
- [ ] Full practice test covers all topics
- [ ] All files are in Obsidian vault
