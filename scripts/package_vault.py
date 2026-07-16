#!/usr/bin/env python3
"""
Package artifacts and audio into an Obsidian vault.
"""

import shutil
import json
from pathlib import Path
import yaml


def load_config():
    """Load configuration from podcast.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "podcast.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def create_obsidian_config(vault_dir):
    """Create .obsidian configuration files."""
    
    obsidian_dir = vault_dir / ".obsidian"
    obsidian_dir.mkdir(exist_ok=True)
    
    # app.json
    app_config = {
        "showLineNumber": True,
        "strictLineBreaks": False,
        "readableLineLength": True,
        "defaultViewMode": "preview",
        "livePreview": True
    }
    with open(obsidian_dir / "app.json", 'w') as f:
        json.dump(app_config, f, indent=2)
    
    # appearance.json
    appearance_config = {
        "baseFontSize": 16,
        "theme": "obsidian",
        "translucency": False,
        "cssTheme": "",
        "accentColor": "#7b6cd9"
    }
    with open(obsidian_dir / "appearance.json", 'w') as f:
        json.dump(appearance_config, f, indent=2)
    
    # core-plugins.json
    core_plugins = [
        "file-explorer",
        "global-search",
        "switcher",
        "graph",
        "backlink",
        "outgoing-link",
        "tag-pane",
        "page-preview",
        "daily-notes",
        "templates",
        "note-composer",
        "command-palette",
        "markdown-importer",
        "outline",
        "word-count",
        "file-recovery"
    ]
    with open(obsidian_dir / "core-plugins.json", 'w') as f:
        json.dump(core_plugins, f, indent=2)
    
    # community-plugins.json (empty)
    with open(obsidian_dir / "community-plugins.json", 'w') as f:
        json.dump([], f)


def create_overview_pages(vault_dir):
    """Create overview and index pages."""
    
    overview_dir = vault_dir / "00-Overview"
    overview_dir.mkdir(exist_ok=True)
    
    # Welcome page
    welcome_md = """# Welcome to Maryland MVA Study Guide

This vault contains study materials for the Maryland Driver's License Exam.

## How to Use This Vault

### Study Materials

Each chapter includes:

- **Memorization Sheet** - One-page high-yield review
- **Rapid Recall Drill** - 20 practice questions
- **Audio Review Script** - Listen on the go

### Audio Files

Audio files are located in the `03-Audio` folder. Click any MP3 file to play.

### Study Plan

1. Start with **01-Driver-Manual** for the knowledge test
2. Use **02-Rookie-Manual** for practical driving lessons
3. Listen to audio reviews while commuting or exercising
4. Test yourself with the Rapid Recall Drills

## Quick Links

- [[Study-Plan]]
- [[License-Requirements]]
- [[Full-Practice-Test]]

---

*Last updated: 2026-07-16*
"""
    with open(overview_dir / "Welcome.md", 'w') as f:
        f.write(welcome_md)
    
    # Study plan
    study_plan_md = """# Maryland MVA Study Plan

## Week 1: Foundations

- [ ] Chapter 01: Driving Tests Requirements
- [ ] Chapter 02: Licensing Requirements
- [ ] Chapter 03: Basic Driving

## Week 2: Rules and Signs

- [ ] Chapter 04: Rules of the Road
- [ ] Chapter 05: Traffic Signs and Signals

## Week 3: Safety

- [ ] Chapter 06: Dangerous Driving
- [ ] Chapter 07: Sharing the Road
- [ ] Chapter 08: Crashes and Traffic Stops

## Week 4: Advanced Topics

- [ ] Chapter 09: Restrictions and Penalties
- [ ] Chapter 10: Important Information

## Week 5-6: Rookie Manual (Lessons 1-16)

- [ ] Lessons 1-4: Basic Vehicle Control
- [ ] Lessons 5-8: Intersection and Lane Skills
- [ ] Lessons 9-12: Advanced Driving
- [ ] Lessons 13-16: Special Situations

## Daily Practice

- Listen to 1-2 audio reviews per day
- Complete 1 Rapid Recall Drill per day
- Review memorization sheets before bed

---

*Adjust this plan based on your test date.*
"""
    with open(overview_dir / "Study-Plan.md", 'w') as f:
        f.write(study_plan_md)
    
    # License requirements
    requirements_md = """# Maryland License Requirements

## Graduated Driver Licensing (GDL)

### Step 1: Learner's Permit

| Requirement | Under 18 | 18-24 | 25+ |
|-------------|----------|-------|-----|
| Minimum Age | 15 years, 9 months | 16 years, 6 months | 18 years |
| Hold Period | 9 months | 9 months | 45 days |
| Practice Hours | 60 hours | 60 hours | 14 hours |
| Night Driving | 10 hours | 10 hours | 3 hours |
| Co-signer | Required | Not required | Not required |

### Step 2: Provisional License

| Requirement | Details |
|-------------|---------|
| Eligibility | Complete GDL requirements |
| Hold Period | 18 months |
| Restrictions | No driving midnight-5am (first 12 months) |
| Passengers | No non-family under 18 (first 12 months) |

### Step 3: Full Driver's License

- Automatic conversion after 18 months with clean record
- No restrictions

## Knowledge Test

- **Questions:** 25
- **Time:** 20 minutes
- **Passing Score:** 80% (20 correct)
- **Topics:** Laws, safe driving, traffic signs

## Vision Requirements

- Binocular vision required
- Visual acuity: 20/40 in each eye
- Field of vision: 140 degrees continuous

## Documents Required

1. Proof of age (birth certificate, passport)
2. Social Security Number
3. Two documents proving Maryland residency
4. Proof of lawful status (if born outside US)

---

*Source: Maryland Driver's Manual*
"""
    with open(overview_dir / "License-Requirements.md", 'w') as f:
        f.write(requirements_md)


def copy_chapters(source_dir, dest_dir, manual_type):
    """Copy chapter files to Obsidian vault."""
    
    source_chapters = Path(source_dir) / "source" / manual_type
    dest_chapters = dest_dir  # Already includes the manual type folder
    
    if not source_chapters.exists():
        print(f"  Warning: {source_chapters} not found")
        return
    
    for chapter_dir in sorted(source_chapters.iterdir()):
        if chapter_dir.is_dir():
            dest_chapter = dest_chapters / chapter_dir.name
            dest_chapter.mkdir(parents=True, exist_ok=True)
            
            # Copy markdown files
            for md_file in chapter_dir.glob("*.md"):
                shutil.copy2(md_file, dest_chapter / md_file.name)
            
            # Copy images if they exist
            images_dir = chapter_dir / "images"
            if images_dir.exists():
                dest_images = dest_chapter / "images"
                dest_images.mkdir(exist_ok=True)
                for img_file in images_dir.glob("*"):
                    shutil.copy2(img_file, dest_images / img_file.name)
            
            print(f"  Copied: {chapter_dir.name}")


def copy_audio_files(config, dest_dir):
    """Copy audio files to Obsidian vault."""
    
    audio_dest = dest_dir / "03-Audio"
    audio_dest.mkdir(exist_ok=True)
    
    mp3_dir = Path(__file__).parent.parent / "output" / "mp3"
    srt_dir = Path(__file__).parent.parent / "output" / "srt"
    
    if not mp3_dir.exists():
        print("  Warning: No audio files found")
        return
    
    for mp3_file in sorted(mp3_dir.glob("*.mp3")):
        shutil.copy2(mp3_file, audio_dest / mp3_file.name)
        
        # Copy corresponding SRT file
        srt_file = srt_dir / mp3_file.name.replace(".mp3", ".srt")
        if srt_file.exists():
            shutil.copy2(srt_file, audio_dest / srt_file.name)
    
    print(f"  Copied {len(list(audio_dest.glob('*.mp3')))} audio files")


def copy_practice_tests(source_dir, dest_dir):
    """Copy practice test files to Obsidian vault."""
    
    practice_dest = dest_dir / "04-Practice"
    practice_dest.mkdir(exist_ok=True)
    
    # Check if practice tests exist in source (they're in obsidian-vault/04-Practice)
    practice_source = source_dir / "obsidian-vault" / "04-Practice"
    if not practice_source.exists():
        # Try alternative location (current directory)
        practice_source = Path.cwd() / "obsidian-vault" / "04-Practice"
        if not practice_source.exists():
            print("  Warning: No practice tests found")
            return
    
    # Copy Driver Manual practice tests
    driver_practice_source = practice_source / "Driver-Manual"
    driver_practice_dest = practice_dest / "Driver-Manual"
    if driver_practice_source.exists():
        driver_practice_dest.mkdir(exist_ok=True)
        for md_file in driver_practice_source.glob("*.md"):
            shutil.copy2(md_file, driver_practice_dest / md_file.name)
        print(f"  Copied {len(list(driver_practice_dest.glob('*.md')))} Driver Manual practice files")
    
    # Copy Rookie Manual practice tests
    rookie_practice_source = practice_source / "Rookie-Manual"
    rookie_practice_dest = practice_dest / "Rookie-Manual"
    if rookie_practice_source.exists():
        rookie_practice_dest.mkdir(exist_ok=True)
        for md_file in rookie_practice_source.glob("*.md"):
            shutil.copy2(md_file, rookie_practice_dest / md_file.name)
        print(f"  Copied {len(list(rookie_practice_dest.glob('*.md')))} Rookie Manual practice files")
    
    # Copy full practice tests
    for md_file in practice_source.glob("*.md"):
        shutil.copy2(md_file, practice_dest / md_file.name)
    print(f"  Copied full practice test files")


def main():
    """Main entry point."""
    config = load_config()
    
    print("=" * 60)
    print("MARYLAND MVA PODCAST - OBSIDIAN VAULT PACKAGE")
    print("=" * 60)
    
    # Setup paths
    source_dir = Path(__file__).parent.parent
    vault_dir = Path(__file__).parent.parent / "obsidian-vault"
    
    # Clean existing vault
    if vault_dir.exists():
        print("\nCleaning existing vault...")
        shutil.rmtree(vault_dir)
    
    # Create vault structure
    print("\nCreating vault structure...")
    vault_dir.mkdir(parents=True)
    
    # Create Obsidian config
    print("Creating Obsidian configuration...")
    create_obsidian_config(vault_dir)
    
    # Create overview pages
    print("Creating overview pages...")
    create_overview_pages(vault_dir)
    
    # Copy Driver Manual chapters
    print("\nCopying Driver Manual chapters...")
    copy_chapters(source_dir, vault_dir / "01-Driver-Manual", "Driver-Manual")
    
    # Copy Rookie Manual chapters
    print("\nCopying Rookie Manual chapters...")
    copy_chapters(source_dir, vault_dir / "02-Rookie-Manual", "Rookie-Manual")
    
    # Copy audio files
    print("\nCopying audio files...")
    copy_audio_files(config, vault_dir)
    
    # Copy practice tests
    print("\nCopying practice tests...")
    copy_practice_tests(source_dir, vault_dir)
    
    # Create practice folder
    practice_dir = vault_dir / "04-Practice"
    practice_dir.mkdir(exist_ok=True)
    
    # Create README
    readme_md = f"""# Maryland MVA Study Vault

## Overview

This Obsidian vault contains study materials for the Maryland Driver's License Exam.

## Contents

- **00-Overview** - Welcome, study plan, requirements
- **01-Driver-Manual** - {len(list((vault_dir / '01-Driver-Manual').glob('Chapter-*')))} chapters
- **02-Rookie-Manual** - {len(list((vault_dir / '02-Rookie-Manual').glob('Chapter-*')))} chapters
- **03-Audio** - MP3 audio reviews
- **04-Practice** - Practice tests and quizzes

## How to Use

1. Open this folder as a vault in Obsidian
2. Start with the Welcome page
3. Follow the Study Plan
4. Listen to audio reviews on the go
5. Test yourself with Rapid Recall Drills

## Audio Playback

Click any MP3 file in the `03-Audio` folder to play.

---

*Generated: 2026-07-16*
"""
    with open(vault_dir / "README.md", 'w') as f:
        f.write(readme_md)
    
    # Create ZIP for distribution
    print("\nCreating ZIP archive...")
    zip_path = vault_dir.parent / "maryland-mva-obsidian.zip"
    shutil.make_archive(
        str(zip_path.with_suffix('')),
        'zip',
        vault_dir.parent,
        vault_dir.name
    )
    
    print("\n" + "=" * 60)
    print("VAULT PACKAGE COMPLETE")
    print("=" * 60)
    print(f"Vault location: {vault_dir}")
    print(f"ZIP archive: {zip_path}")
    print(f"\nTo use:")
    print(f"  1. Open Obsidian")
    print(f"  2. Open folder as vault")
    print(f"  3. Navigate to: {vault_dir}")


if __name__ == "__main__":
    main()
