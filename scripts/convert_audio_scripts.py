#!/usr/bin/env python3
"""
Convert JSON Audio Review Scripts to human-readable Markdown format.

Usage:
    uv run python scripts/convert_audio_scripts.py
"""

import json
from pathlib import Path


def convert_json_to_markdown(json_path: Path) -> str:
    """Convert a JSON audio script to markdown format."""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix common JSON issues
    # Fix unescaped quotes in tts_notes (e.g., 4'9" -> 4'9\")
    content = content.replace("4'9\"", "4'9\\\"")
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    # Get chapter info from path
    path_str = str(json_path)
    if "Driver-Manual" in path_str:
        manual_type = "Driver's Manual"
    else:
        manual_type = "Rookie Manual"
    
    chapter_num = json_path.parent.name.replace("Chapter-", "")
    topic = data.get('topic', 'Unknown Topic')
    total_duration = data.get('total_duration', 0)
    total_words = data.get('total_word_count', 0)
    
    # Build markdown
    md = f"# Chapter {chapter_num} — {topic} — Audio Review Script\n\n"
    md += f"**Manual:** {manual_type}\n"
    md += f"**Topic:** {topic}\n"
    md += f"**Duration:** {total_duration} minutes\n"
    md += f"**Word Count:** {total_words} words\n\n"
    md += "---\n\n"
    
    # Add sections
    for section in data.get('sections', []):
        title = section.get('title', 'Untitled')
        start_time = section.get('start_time', '0:00')
        end_time = section.get('end_time', '0:00')
        content = section.get('content', '')
        
        md += f"## [{start_time} - {end_time}] {title}\n\n"
        md += content + "\n\n"
        md += "---\n\n"
    
    # Add pronunciation guide
    pronunciation = data.get('pronunciation_guide', {})
    if pronunciation:
        md += "## Pronunciation Guide\n\n"
        for word, pronunciation_text in pronunciation.items():
            md += f"- **{word}**: {pronunciation_text}\n"
        md += "\n"
    
    # Add TTS notes
    tts_notes = data.get('tts_notes', '')
    if tts_notes:
        md += "## Text-to-Speech Notes\n\n"
        md += f"{tts_notes}\n\n"
    
    return md


def main():
    """Main function to convert all JSON audio scripts."""
    print("=" * 60)
    print("CONVERTING JSON AUDIO SCRIPTS TO MARKDOWN")
    print("=" * 60)
    print()
    
    vault_path = Path("obsidian-vault")
    
    # Find all JSON audio scripts
    json_scripts = []
    for manual_dir in ["01-Driver-Manual", "02-Rookie-Manual"]:
        manual_path = vault_path / manual_dir
        if manual_path.exists():
            for chapter_dir in sorted(manual_path.glob("Chapter-*")):
                script_file = chapter_dir / "06.Audio-Review-Script.md"
                if script_file.exists():
                    # Check if it's JSON
                    with open(script_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('{'):
                            json_scripts.append(script_file)
    
    print(f"Found {len(json_scripts)} JSON audio scripts to convert")
    print()
    
    # Convert each script
    converted = 0
    for json_path in json_scripts:
        print(f"Converting: {json_path.parent.name}/{json_path.name}")
        
        try:
            markdown_content = convert_json_to_markdown(json_path)
            
            # Write back to the same file
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            converted += 1
            print(f"  ✓ Converted successfully")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print(f"COMPLETE: {converted} scripts converted")
    print("=" * 60)


if __name__ == "__main__":
    main()
