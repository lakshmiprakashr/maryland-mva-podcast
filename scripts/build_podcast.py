#!/usr/bin/env python3
"""
Build podcast episodes and RSS feed from generated audio files.
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
import yaml


def load_config():
    """Load configuration from podcast.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "podcast.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_episode_duration(mp3_path):
    """Get duration of MP3 file in seconds."""
    # Simple estimation based on file size (rough: 1MB ≈ 1 minute at 128kbps)
    size_mb = mp3_path.stat().st_size / (1024 * 1024)
    return int(size_mb * 60)


def build_rss_feed(config):
    """Build RSS feed for podcast."""
    
    podcast_config = config.get('podcast', {})
    chapters = config.get('chapters', {})
    
    # Create RSS structure
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    
    channel = ET.SubElement(rss, 'channel')
    
    # Channel metadata
    ET.SubElement(channel, 'title').text = podcast_config.get('title', 'Maryland MVA Study Podcast')
    ET.SubElement(channel, 'description').text = podcast_config.get('description', 'Audio review for Maryland Driver\'s License Exam')
    ET.SubElement(channel, 'language').text = podcast_config.get('language', 'en-us')
    ET.SubElement(channel, 'link').text = podcast_config.get('link', '')
    
    itunes_author = ET.SubElement(channel, '{http://www.itunes.com/dtds/podcast-1.0.dtd}author')
    itunes_author.text = podcast_config.get('author', 'Maryland MVA Study Guide')
    
    itunes_summary = ET.SubElement(channel, '{http://www.itunes.com/dtds/podcast-1.0.dtd}summary')
    itunes_summary.text = podcast_config.get('description', '')
    
    # Add episodes
    mp3_dir = Path(__file__).parent.parent / "output" / "mp3"
    
    episode_num = 1
    
    # Driver Manual episodes
    for chapter in chapters.get('driver_manual', []):
        mp3_path = mp3_dir / f"driver-manual-chapter-{chapter['id']}.mp3"
        if mp3_path.exists():
            item = add_episode_item(
                channel, mp3_path, chapter, 
                f"Driver Manual Chapter {chapter['id']}",
                episode_num
            )
            episode_num += 1
    
    # Rookie Manual episodes
    for chapter in chapters.get('rookie_manual', []):
        mp3_path = mp3_dir / f"rookie-manual-chapter-{chapter['id']}.mp3"
        if mp3_path.exists():
            item = add_episode_item(
                channel, mp3_path, chapter,
                f"Rookie Manual Chapter {chapter['id']}",
                episode_num
            )
            episode_num += 1
    
    # Pretty print XML
    rough_string = ET.tostring(rss, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    return pretty_xml


def add_episode_item(channel, mp3_path, chapter, manual_type, episode_num):
    """Add an episode item to the RSS feed."""
    
    item = ET.SubElement(channel, 'item')
    
    title = f"{manual_type}: {chapter['title']}"
    ET.SubElement(item, 'title').text = title
    ET.SubElement(item, 'enclosure', 
                  url=str(mp3_path.name),
                  type='audio/mpeg',
                  str(mp3_path.stat().st_size))
    
    duration = get_episode_duration(mp3_path)
    itunes_duration = ET.SubElement(item, '{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')
    itunes_duration.text = f"{duration // 60}:{duration % 60:02d}"
    
    ET.SubElement(item, 'description').text = f"Review of {chapter['title']} for Maryland MVA knowledge test."
    
    return item


def create_podcast_json(config):
    """Create JSON manifest for podcast episodes."""
    
    chapters = config.get('chapters', {})
    mp3_dir = Path(__file__).parent.parent / "output" / "mp3"
    
    episodes = []
    episode_num = 1
    
    # Driver Manual
    for chapter in chapters.get('driver_manual', []):
        mp3_path = mp3_dir / f"driver-manual-chapter-{chapter['id']}.mp3"
        if mp3_path.exists():
            episodes.append({
                "episode": episode_num,
                "manual": "Driver Manual",
                "chapter": chapter['id'],
                "title": chapter['title'],
                "file": str(mp3_path.name),
                "duration_seconds": get_episode_duration(mp3_path),
                "size_bytes": mp3_path.stat().st_size
            })
            episode_num += 1
    
    # Rookie Manual
    for chapter in chapters.get('rookie_manual', []):
        mp3_path = mp3_dir / f"rookie-manual-chapter-{chapter['id']}.mp3"
        if mp3_path.exists():
            episodes.append({
                "episode": episode_num,
                "manual": "Rookie Manual",
                "chapter": chapter['id'],
                "title": chapter['title'],
                "file": str(mp3_path.name),
                "duration_seconds": get_episode_duration(mp3_path),
                "size_bytes": mp3_path.stat().st_size
            })
            episode_num += 1
    
    return {
        "title": config.get('podcast', {}).get('title', ''),
        "description": config.get('podcast', {}).get('description', ''),
        "total_episodes": len(episodes),
        "total_duration_seconds": sum(e['duration_seconds'] for e in episodes),
        "episodes": episodes
    }


def main():
    """Main entry point."""
    config = load_config()
    
    print("=" * 60)
    print("MARYLAND MVA PODCAST - BUILD PODCAST")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "podcast"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate RSS feed
    print("\nGenerating RSS feed...")
    rss_xml = build_rss_feed(config)
    rss_path = output_dir / "feed.xml"
    with open(rss_path, 'w') as f:
        f.write(rss_xml)
    print(f"  Created: {rss_path.name}")
    
    # Generate JSON manifest
    print("\nGenerating episode manifest...")
    manifest = create_podcast_json(config)
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"  Created: {manifest_path.name}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PODCAST BUILD COMPLETE")
    print("=" * 60)
    print(f"Total episodes: {manifest['total_episodes']}")
    total_min = manifest['total_duration_seconds'] // 60
    print(f"Total duration: {total_min} minutes")
    print(f"\nOutput files:")
    print(f"  {rss_path}")
    print(f"  {manifest_path}")


if __name__ == "__main__":
    main()
