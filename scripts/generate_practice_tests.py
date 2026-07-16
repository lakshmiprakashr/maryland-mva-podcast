#!/usr/bin/env python3
"""
Generate practice tests from Rapid Recall Drills.

Extracts questions from Rapid Recall Drills and creates:
1. Test files (questions only, multiple choice format)
2. Answer keys (answers with explanations)

Usage:
    uv run python scripts/generate_practice_tests.py
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple
import random


def extract_questions_from_drill(drill_path: Path) -> List[Dict]:
    """Extract questions and answers from Rapid Recall Drill."""
    content = drill_path.read_text(encoding='utf-8')
    questions = []
    
    # Check if file is JSON format
    if content.strip().startswith('{'):
        try:
            import json
            data = json.loads(content)
            if 'questions' in data:
                for q in data['questions']:
                    questions.append({
                        'number': q.get('number', 0),
                        'type': q.get('type', 'RECALL'),
                        'question': q.get('question', ''),
                        'answer': q.get('answer', ''),
                        'explanation': q.get('explanation', ''),
                        'trap': q.get('mva_trap', q.get('trap', '')),
                        'mistake': q.get('common_mistake', q.get('mistake', '')),
                        'reference': q.get('reference', 'See chapter')
                    })
                return questions
        except json.JSONDecodeError:
            pass
    
    # Markdown format - split content by question markers and extract each question
    # First, find all question positions
    question_positions = []
    for match in re.finditer(r'\*\*Q(\d+)\.\s*\[(?:Type:\s*)?(\w+)\]\*\*', content):
        question_positions.append((match.start(), match.group(1), match.group(2)))
    
    # Extract each question's content
    for i, (pos, q_num, q_type) in enumerate(question_positions):
        # Get content from this question to the next (or end)
        if i + 1 < len(question_positions):
            end_pos = question_positions[i + 1][0]
        else:
            end_pos = len(content)
        
        question_content = content[pos:end_pos]
        
        # Extract fields using simple regex
        answer_match = re.search(r'\*\*Answer:\*\*\s+(.+?)(?=\n|$)', question_content)
        explanation_match = re.search(r'\*\*Explanation:\*\*\s+(.+?)(?=\n|$)', question_content)
        trap_match = re.search(r'\*\*MVA Test Trap:\*\*\s+(.+?)(?=\n|$)', question_content)
        mistake_match = re.search(r'\*\*Common Mistake:\*\*\s+(.+?)(?=\n|$)', question_content)
        reference_match = re.search(r'\*\*Reference:\*\*\s+(.+?)(?=\n|$)', question_content)
        
        # Get question text (everything after the Q marker until Answer:)
        q_text_match = re.search(r'\*\*Q\d+\.\s*\[(?:Type:\s*)?\w+\]\*\*\s+(.+?)(?=\n\n\*\*Answer)', question_content, re.DOTALL)
        
        # Reference is optional - not all chapters have it
        if all([answer_match, explanation_match, trap_match, mistake_match, q_text_match]):
            questions.append({
                'number': int(q_num),
                'type': q_type.strip(),
                'question': q_text_match.group(1).strip(),
                'answer': answer_match.group(1).strip(),
                'explanation': explanation_match.group(1).strip(),
                'trap': trap_match.group(1).strip(),
                'mistake': mistake_match.group(1).strip(),
                'reference': reference_match.group(1).strip() if reference_match else "See chapter"
            })
    
    return questions


def generate_distractors(correct_answer: str, all_answers: List[str]) -> List[str]:
    """Generate plausible wrong answers (distractors) for multiple choice."""
    distractors = []
    
    # Try to find similar answers from other questions
    for ans in all_answers:
        if ans != correct_answer and len(distractors) < 3:
            # Check if it's somewhat related (same length range)
            if abs(len(ans) - len(correct_answer)) < 20:
                distractors.append(ans)
    
    # If we don't have enough, add generic distractors
    generic_distractors = [
        "Not specified in the manual",
        "Varies by county",
        "Only required for commercial vehicles",
        "Optional but recommended",
        "Depends on the situation"
    ]
    
    while len(distractors) < 3:
        distractors.append(generic_distractors[len(distractors)])
    
    # Shuffle and return first 3
    random.shuffle(distractors)
    return distractors[:3]


def create_multiple_choice(question: Dict, all_answers: List[str]) -> Tuple[str, str]:
    """Convert a question to multiple choice format."""
    correct_answer = question['answer']
    
    # Generate distractors
    distractors = generate_distractors(correct_answer, all_answers)
    
    # Create options
    options = [correct_answer] + distractors
    random.shuffle(options)
    
    # Find correct option letter
    correct_letter = chr(65 + options.index(correct_answer))
    
    # Format question
    formatted = f"**Q{question['number']}. [{question['type']}]** {question['question']}\n\n"
    for i, opt in enumerate(options):
        letter = chr(65 + i)
        formatted += f"- {letter}) {opt}\n"
    
    return formatted, correct_letter


def generate_test_file(questions: List[Dict], chapter_info: str) -> str:
    """Generate a test file with questions only."""
    all_answers = [q['answer'] for q in questions]
    
    content = f"# {chapter_info} — Practice Test\n\n"
    content += "## Instructions\n\n"
    content += "- 20 questions\n"
    content += "- 25 minutes recommended\n"
    content += "- No answers visible until you check the Answer Key\n"
    content += "- Circle or write your answer letter (A, B, C, or D)\n\n"
    content += "---\n\n"
    content += "## Questions\n\n"
    
    for q in questions:
        formatted_q, _ = create_multiple_choice(q, all_answers)
        content += formatted_q + "\n---\n\n"
    
    content += "## Score\n\n"
    content += "Correct: ___ / 20 = ___%\n\n"
    content += "- 18-20 (90-100%): Excellent! Ready for the exam.\n"
    content += "- 15-17 (75-89%): Good, but review missed topics.\n"
    content += "- 12-14 (60-74%): Study more before testing.\n"
    content += "- Below 12 (60%): Review the chapter thoroughly.\n"
    
    return content


def generate_answer_key(questions: List[Dict], chapter_info: str) -> str:
    """Generate an answer key with explanations."""
    all_answers = [q['answer'] for q in questions]
    
    content = f"# {chapter_info} — Answer Key\n\n"
    content += "## Answers with Explanations\n\n"
    
    for q in questions:
        _, correct_letter = create_multiple_choice(q, all_answers)
        
        content += f"### Question {q['number']}\n"
        content += f"**Correct Answer:** {correct_letter}) {q['answer']}\n\n"
        content += f"**Explanation:** {q['explanation']}\n\n"
        content += f"**MVA Test Trap:** {q['trap']}\n\n"
        content += f"**Common Mistake:** {q['mistake']}\n\n"
        content += f"**Reference:** {q['reference']}\n\n"
        content += "---\n\n"
    
    # Add scoring guide
    content += "## Scoring Guide\n\n"
    content += "- 18-20 correct (90-100%): Excellent! You're ready for the exam.\n"
    content += "- 15-17 correct (75-89%): Good work! Review the questions you missed.\n"
    content += "- 12-14 correct (60-74%): Study the chapter again and retake.\n"
    content += "- Below 12 correct (60%): Review the entire chapter before retesting.\n"
    
    return content


def process_chapter(chapter_dir: Path, output_dir: Path) -> Tuple[int, int]:
    """Process a single chapter's Rapid Recall Drill."""
    # Find the Rapid Recall Drill file
    drill_files = list(chapter_dir.glob("*.Rapid-Recall-Drill.md"))
    
    if not drill_files:
        print(f"  No Rapid Recall Drill found in {chapter_dir}")
        return 0, 0
    
    drill_file = drill_files[0]
    print(f"  Processing: {drill_file.name}")
    
    # Extract questions
    questions = extract_questions_from_drill(drill_file)
    
    if not questions:
        print(f"    No questions extracted from {drill_file.name}")
        return 0, 0
    
    print(f"    Extracted {len(questions)} questions")
    
    # Get chapter info from parent directory
    chapter_name = chapter_dir.name
    manual_type = chapter_dir.parent.name
    
    # Determine if this is Driver or Rookie manual
    if "Driver" in manual_type:
        chapter_info = f"Chapter {chapter_name.replace('Chapter-', '')} — Driver's Manual"
    else:
        chapter_info = f"Chapter {chapter_name.replace('Chapter-', '')} — Rookie Manual"
    
    # Create test file
    test_content = generate_test_file(questions, chapter_info)
    test_file = output_dir / f"{chapter_name}-Test.md"
    test_file.write_text(test_content, encoding='utf-8')
    
    # Create answer key
    answer_content = generate_answer_key(questions, chapter_info)
    answer_file = output_dir / f"{chapter_name}-Answers.md"
    answer_file.write_text(answer_content, encoding='utf-8')
    
    return 1, 1


def generate_full_practice_test(all_questions: List[Dict]) -> str:
    """Generate a comprehensive 50-question practice test."""
    # Randomly select 50 questions from all available
    selected = random.sample(all_questions, min(50, len(all_questions)))
    
    content = "# Maryland MVA Knowledge Test — Full Practice Test\n\n"
    content += "## Instructions\n\n"
    content += "- 50 questions (comprehensive)\n"
    content += "- 45 minutes recommended\n"
    content += "- Passing score: 80% (40 correct)\n"
    content += "- No answers visible until you check the Answer Key\n\n"
    content += "---\n\n"
    content += "## Questions\n\n"
    
    all_answers = [q['answer'] for q in selected]
    
    for q in selected:
        formatted_q, _ = create_multiple_choice(q, all_answers)
        content += formatted_q + "\n---\n\n"
    
    content += "## Score\n\n"
    content += "Correct: ___ / 50 = ___%\n\n"
    content += "- 45-50 (90-100%): Excellent! You're ready for the exam.\n"
    content += "- 40-44 (80-89%): Good! You should pass.\n"
    content += "- 35-39 (70-79%): Close, review weak areas.\n"
    content += "- 30-34 (60-69%): Study more before testing.\n"
    content += "- Below 30 (60%): Need significant study time.\n"
    
    return content


def generate_full_answer_key(all_questions: List[Dict]) -> str:
    """Generate answer key for the full practice test."""
    selected = random.sample(all_questions, min(50, len(all_questions)))
    
    content = "# Maryland MVA Knowledge Test — Full Practice Test Answer Key\n\n"
    content += "## Answers with Explanations\n\n"
    
    all_answers = [q['answer'] for q in selected]
    
    for q in selected:
        _, correct_letter = create_multiple_choice(q, all_answers)
        
        content += f"### Question {q['number']}\n"
        content += f"**Correct Answer:** {correct_letter}) {q['answer']}\n\n"
        content += f"**Explanation:** {q['explanation']}\n\n"
        content += f"**MVA Test Trap:** {q['trap']}\n\n"
        content += f"**Common Mistake:** {q['mistake']}\n\n"
        content += f"**Reference:** {q['reference']}\n\n"
        content += "---\n\n"
    
    content += "## Scoring Guide\n\n"
    content += "- 45-50 correct (90-100%): Excellent! You're ready for the exam.\n"
    content += "- 40-44 correct (80-89%): Good! You should pass.\n"
    content += "- 35-39 correct (70-79%): Close, review weak areas.\n"
    content += "- 30-34 correct (60-69%): Study more before testing.\n"
    content += "- Below 30 correct (60%): Need significant study time.\n"
    
    return content


def main():
    """Main function to generate practice tests."""
    print("=" * 60)
    print("MARYLAND MVA PRACTICE TEST GENERATOR")
    print("=" * 60)
    print()
    
    # Paths
    vault_path = Path("obsidian-vault")
    practice_path = vault_path / "04-Practice"
    
    # Create output directories
    driver_practice = practice_path / "Driver-Manual"
    rookie_practice = practice_path / "Rookie-Manual"
    
    driver_practice.mkdir(parents=True, exist_ok=True)
    rookie_practice.mkdir(parents=True, exist_ok=True)
    
    # Track all questions for full practice test
    all_questions = []
    total_tests = 0
    total_answers = 0
    
    # Process Driver Manual chapters
    print("=" * 60)
    print("Processing Driver Manual chapters...")
    print("=" * 60)
    
    driver_chapters = sorted((vault_path / "01-Driver-Manual").glob("Chapter-*"))
    for chapter_dir in driver_chapters:
        tests, answers = process_chapter(chapter_dir, driver_practice)
        total_tests += tests
        total_answers += answers
        
        # Collect questions for full test
        drill_files = list(chapter_dir.glob("*.Rapid-Recall-Drill.md"))
        if drill_files:
            questions = extract_questions_from_drill(drill_files[0])
            all_questions.extend(questions)
    
    print()
    
    # Process Rookie Manual chapters
    print("=" * 60)
    print("Processing Rookie Manual chapters...")
    print("=" * 60)
    
    rookie_chapters = sorted((vault_path / "02-Rookie-Manual").glob("Chapter-*"))
    for chapter_dir in rookie_chapters:
        tests, answers = process_chapter(chapter_dir, rookie_practice)
        total_tests += tests
        total_answers += answers
        
        # Collect questions for full test
        drill_files = list(chapter_dir.glob("*.Rapid-Recall-Drill.md"))
        if drill_files:
            questions = extract_questions_from_drill(drill_files[0])
            all_questions.extend(questions)
    
    print()
    
    # Generate full practice test
    print("=" * 60)
    print("Generating full practice test...")
    print("=" * 60)
    
    if all_questions:
        # Shuffle questions for variety
        random.shuffle(all_questions)
        
        # Generate full practice test
        test_content = generate_full_practice_test(all_questions)
        test_file = practice_path / "Full-Practice-Test.md"
        test_file.write_text(test_content, encoding='utf-8')
        print(f"  Created: Full-Practice-Test.md")
        
        # Generate full answer key
        answer_content = generate_full_answer_key(all_questions)
        answer_file = practice_path / "Full-Practice-Test-Answers.md"
        answer_file.write_text(answer_content, encoding='utf-8')
        print(f"  Created: Full-Practice-Test-Answers.md")
        
        total_tests += 1
        total_answers += 1
    
    print()
    print("=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Total tests generated: {total_tests}")
    print(f"Total answer keys generated: {total_answers}")
    print(f"Total questions available: {len(all_questions)}")
    print()
    print(f"Output locations:")
    print(f"  Driver Manual: {driver_practice}")
    print(f"  Rookie Manual: {rookie_practice}")
    print(f"  Full Practice: {practice_path}")


if __name__ == "__main__":
    main()
