#!/usr/bin/env python3
"""
Extract clean text from audio script markdown files for TTS processing.
"""

import re
import sys
from pathlib import Path
import yaml


def load_config():
    """Load configuration from podcast.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "podcast.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def extract_text_from_audio_script(md_content, config):
    """Convert audio script markdown to clean TTS-ready text."""
    
    # Get abbreviations from config
    abbreviations = config.get('abbreviations', {})
    
    # Remove markdown headers (keep text)
    text = re.sub(r'^#+\s+', '', md_content, flags=re.MULTILINE)
    
    # Remove timestamps like [0:00], [1:30]
    text = re.sub(r'\[[\d:]+\]', '', text)
    
    # Remove SSML break tags (edge-tts doesn't support them properly)
    text = re.sub(r'<break\s+time="[^"]*"\s*/>', '', text)
    
    # Remove pause markers entirely (don't replace with periods)
    pause_markers = config.get('pause_markers', {})
    for marker in pause_markers.keys():
        text = text.replace(marker, '')
    
    # Remove [EMPHASIS: ...] markers
    text = re.sub(r'\[EMPHASIS:.*?\]', '', text)
    
    # Expand abbreviations
    for abbr, expansion in abbreviations.items():
        # Match whole words only
        text = re.sub(rf'\b{abbr}\b', expansion, text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # Italic
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text) # Links
    text = re.sub(r'`(.*?)`', r'\1', text)          # Code
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[#&@<>{}]', '', text)
    
    # Clean up multiple periods or spaces
    text = re.sub(r'\.{2,}', '.', text)  # Multiple periods to single
    text = re.sub(r' +', ' ', text)      # Multiple spaces to single
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def process_chapter(manual_type, chapter_id, config):
    """Process a single chapter's audio script."""
    
    source_dir = Path(__file__).parent.parent / "source" / manual_type
    chapter_dir = source_dir / f"Chapter-{chapter_id}"
    
    script_path = chapter_dir / "06.Audio-Review-Script.md"
    
    if not script_path.exists():
        print(f"  Warning: {script_path} not found, skipping")
        return None
    
    with open(script_path) as f:
        content = f.read()
    
    # Extract clean text
    clean_text = extract_text_from_audio_script(content, config)
    
    # Save to output
    output_dir = Path(__file__).parent.parent / "output" / "wav"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"{manual_type.lower()}-chapter-{chapter_id}.txt"
    with open(output_path, 'w') as f:
        f.write(clean_text)
    
    print(f"  Extracted: {output_path.name} ({len(clean_text)} chars)")
    return output_path


def main():
    """Main entry point."""
    config = load_config()
    
    print("=" * 60)
    print("MARYLAND MVA PODCAST - TEXT EXTRACTION")
    print("=" * 60)
    
    # Process Driver Manual
    print("\nDriver Manual:")
    driver_chapters = config['chapters']['driver_manual']
    for chapter in driver_chapters:
        process_chapter("Driver-Manual", chapter['id'], config)
    
    # Process Rookie Manual
    print("\nRookie Manual:")
    rookie_chapters = config['chapters']['rookie_manual']
    for chapter in rookie_chapters:
        process_chapter("Rookie-Manual", chapter['id'], config)
    
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
