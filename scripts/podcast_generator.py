#!/usr/bin/env python3
"""
Maryland MVA Podcast Generator — Convert audio lessons into a podcast feed.

Scans generated MP3 files and produces a valid RSS 2.0 feed with iTunes
extensions suitable for subscribing in Apple Podcasts.

Usage:
    uv run python scripts/podcast_generator.py
    uv run python scripts/podcast_generator.py --validate-only
    uv run python scripts/podcast_generator.py --rebuild
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import mutagen
except ImportError:
    mutagen = None

try:
    from feedgen.feed import FeedGenerator
except ImportError:
    print("ERROR: feedgen not installed. Run: uv add feedgen")
    sys.exit(1)


# Chapter metadata
DRIVER_CHAPTERS = {
    1: {"title": "Driving Tests Requirements", "description": "Learn about the three licensing requirements for Maryland: vision screening, knowledge test, and driving skills test."},
    2: {"title": "The Maryland GDL System", "description": "Understand Maryland's Graduated Driver Licensing system for first-time drivers."},
    3: {"title": "Basic Driving", "description": "Defensive driving, right-of-way rules, speed control, following distance, and lane driving."},
    4: {"title": "Speed and Right-of-Way", "description": "Speed limits, following distances, and right-of-way rules at intersections."},
    5: {"title": "Traffic Signs and Signals", "description": "Understanding traffic signs, signals, and road markings."},
    6: {"title": "Parking", "description": "Parking rules, parallel parking, and parking restrictions."},
    7: {"title": "Sharing the Road", "description": "Sharing the road with pedestrians, bicyclists, and other vehicles."},
    8: {"title": "Crashes and Traffic Stops", "description": "What to do in case of a crash and during traffic stops."},
    9: {"title": "Other Restrictions", "description": "License restrictions, violations, and penalties."},
    10: {"title": "Insurance and Safety", "description": "Insurance requirements and vehicle safety."},
}

ROOKIE_CHAPTERS = {
    i: {"title": f"Chapter {i}", "description": f"Rookie Manual Chapter {i} - Maryland MVA study material."}
    for i in range(1, 26)
}


def get_audio_duration(filepath: Path) -> int:
    """Get audio duration in seconds using mutagen."""
    if mutagen is None:
        return 720  # Default 12 minutes
    
    try:
        audio = mutagen.File(filepath)
        if audio is not None:
            return int(audio.info.length)
    except Exception:
        pass
    
    return 720


def generate_podcast_feed(
    base_url: str = "https://lakshmiprakashr.github.io/maryland-mva-podcast",
    output_dir: Path = Path("podcast"),
    rebuild: bool = False
):
    """Generate RSS podcast feed."""
    
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    # Channel metadata
    fg.title('Maryland MVA Study Podcast')
    fg.link(href=f'{base_url}/podcast.xml', rel='self')
    fg.link(href=base_url, rel='alternate')
    fg.description('Audio review materials for the Maryland Driver\'s License Exam. Study for the MVA knowledge test with chapter-by-chapter audio guides covering traffic laws, safe driving practices, and road signs.')
    fg.language('en')
    fg.managingEditor('MVA Study Guide')
    fg.webMaster('MVA Study Guide')
    fg.podcast.itunes_author('MVA Study Guide')
    fg.podcast.itunes_summary('Prepare for your Maryland driver\'s license exam with these audio study guides. Covers both the Driver\'s Manual and Rookie Manual with detailed explanations, memory tricks, and practice questions.')
    fg.podcast.itunes_owner(name='MVA Study Guide', email='mva-podcast@example.com')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_category('Education')
    fg.podcast.itunes_image(f'{base_url}/artwork.jpg')
    
    # Add Driver Manual episodes
    for ch_num, ch_info in sorted(DRIVER_CHAPTERS.items()):
        mp3_file = output_dir / "Driver-Manual" / f"driver-manual-chapter-{ch_num:02d}.mp3"
        
        if not mp3_file.exists():
            print(f"  WARNING: Missing {mp3_file}")
            continue
        
        duration = get_audio_duration(mp3_file)
        file_size = mp3_file.stat().st_size
        
        fe = fg.add_entry()
        fe.id(str(uuid.uuid4()))
        fe.title(f"Driver Ch.{ch_num}: {ch_info['title']}")
        fe.description(ch_info['description'])
        fe.enclosure(
            url=f"{base_url}/Driver-Manual/driver-manual-chapter-{ch_num:02d}.mp3",
            length=str(file_size),
            type='audio/mpeg'
        )
        fe.pubDate(datetime(2024, 1, ch_num, tzinfo=timezone.utc))
        fe.podcast.itunes_duration(duration)
        fe.podcast.itunes_explicit('no')
        fe.podcast.itunes_summary(ch_info['description'])
        
        print(f"  Added: Driver Ch.{ch_num}: {ch_info['title']}")
    
    # Add Rookie Manual episodes
    for ch_num, ch_info in sorted(ROOKIE_CHAPTERS.items()):
        mp3_file = output_dir / "Rookie-Manual" / f"rookie-manual-chapter-{ch_num:02d}.mp3"
        
        if not mp3_file.exists():
            print(f"  WARNING: Missing {mp3_file}")
            continue
        
        duration = get_audio_duration(mp3_file)
        file_size = mp3_file.stat().st_size
        
        fe = fg.add_entry()
        fe.id(str(uuid.uuid4()))
        fe.title(f"Rookie Ch.{ch_num}: {ch_info['title']}")
        fe.description(ch_info['description'])
        fe.enclosure(
            url=f"{base_url}/Rookie-Manual/rookie-manual-chapter-{ch_num:02d}.mp3",
            length=str(file_size),
            type='audio/mpeg'
        )
        fe.pubDate(datetime(2024, 2, ch_num, tzinfo=timezone.utc))
        fe.podcast.itunes_duration(duration)
        fe.podcast.itunes_explicit('no')
        fe.podcast.itunes_summary(ch_info['description'])
        
        print(f"  Added: Rookie Ch.{ch_num}: {ch_info['title']}")
    
    # Write feed
    feed_path = output_dir / "podcast.xml"
    fg.rss_file(str(feed_path), pretty=True)
    print(f"\n  Feed written to: {feed_path}")
    
    return feed_path


def validate_feed(feed_path: Path):
    """Validate the podcast feed."""
    import xml.etree.ElementTree as ET
    
    try:
        tree = ET.parse(feed_path)
        root = tree.getroot()
        
        # Check for required elements
        channel = root.find('channel')
        if channel is None:
            print("ERROR: No channel element found")
            return False
        
        title = channel.find('title')
        if title is None or not title.text:
            print("ERROR: Channel title missing")
            return False
        
        items = channel.findall('item')
        print(f"  Channel title: {title.text}")
        print(f"  Episodes: {len(items)}")
        
        # Validate each item
        for item in items:
            item_title = item.find('title')
            enclosure = item.find('enclosure')
            
            if item_title is None or not item_title.text:
                print(f"  WARNING: Episode missing title")
            
            if enclosure is None:
                print(f"  WARNING: Episode '{item_title.text}' missing enclosure")
        
        print("\n  Feed validation: PASSED")
        return True
        
    except ET.ParseError as e:
        print(f"ERROR: Invalid XML: {e}")
        return False


def generate_episodes_json(output_dir: Path):
    """Generate episodes.json for the web player."""
    episodes = []
    
    for ch_num, ch_info in sorted(DRIVER_CHAPTERS.items()):
        mp3_file = output_dir / "Driver-Manual" / f"driver-manual-chapter-{ch_num:02d}.mp3"
        if mp3_file.exists():
            episodes.append({
                "id": f"driver-{ch_num:02d}",
                "title": f"Driver Ch.{ch_num}: {ch_info['title']}",
                "description": ch_info['description'],
                "file": f"Driver-Manual/driver-manual-chapter-{ch_num:02d}.mp3",
                "duration": get_audio_duration(mp3_file),
                "manual": "Driver"
            })
    
    for ch_num, ch_info in sorted(ROOKIE_CHAPTERS.items()):
        mp3_file = output_dir / "Rookie-Manual" / f"rookie-manual-chapter-{ch_num:02d}.mp3"
        if mp3_file.exists():
            episodes.append({
                "id": f"rookie-{ch_num:02d}",
                "title": f"Rookie Ch.{ch_num}: {ch_info['title']}",
                "description": ch_info['description'],
                "file": f"Rookie-Manual/rookie-manual-chapter-{ch_num:02d}.mp3",
                "duration": get_audio_duration(mp3_file),
                "manual": "Rookie"
            })
    
    json_path = output_dir / "episodes.json"
    json_path.write_text(json.dumps(episodes, indent=2))
    print(f"  Episodes JSON written to: {json_path}")
    
    return json_path


def main():
    parser = argparse.ArgumentParser(description='Generate MVA podcast feed')
    parser.add_argument('--validate-only', action='store_true', help='Only validate existing feed')
    parser.add_argument('--rebuild', action='store_true', help='Force rebuild all files')
    parser.add_argument('--output-dir', type=Path, default=Path('podcast'), help='Output directory')
    parser.add_argument('--base-url', type=str, 
                       default='https://lakshmiprakashr.github.io/maryland-mva-podcast',
                       help='Base URL for the podcast')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MARYLAND MVA PODCAST GENERATOR")
    print("=" * 60)
    print()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.validate_only:
        feed_path = args.output_dir / "podcast.xml"
        if not feed_path.exists():
            print("ERROR: podcast.xml not found. Run without --validate-only first.")
            sys.exit(1)
        
        print("Validating podcast feed...")
        validate_feed(feed_path)
        return
    
    # Generate feed
    print("Generating podcast feed...")
    generate_podcast_feed(
        base_url=args.base_url,
        output_dir=args.output_dir,
        rebuild=args.rebuild
    )
    
    # Generate episodes JSON
    print("\nGenerating episodes JSON...")
    generate_episodes_json(args.output_dir)
    
    # Validate
    print("\nValidating feed...")
    feed_path = args.output_dir / "podcast.xml"
    if feed_path.exists():
        validate_feed(feed_path)
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
