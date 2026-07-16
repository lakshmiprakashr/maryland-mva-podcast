#!/usr/bin/env python3
"""
Build RSS podcast feed and manifest for Netlify deployment.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta


def load_config():
    """Load configuration."""
    import yaml
    config_path = Path(__file__).parent.parent / "config" / "podcast.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


def get_chapter_info():
    """Get chapter information."""
    return {
        "driver": [
            {"id": 1, "title": "Driving Tests Requirements", "duration": 720, "date_offset": 0},
            {"id": 2, "title": "The Maryland GDL System", "duration": 840, "date_offset": 1},
            {"id": 3, "title": "Basic Driving", "duration": 780, "date_offset": 2},
            {"id": 4, "title": "Speed and Right-of-Way", "duration": 900, "date_offset": 3},
            {"id": 5, "title": "Traffic Signs and Signals", "duration": 720, "date_offset": 4},
            {"id": 6, "title": "Parking", "duration": 600, "date_offset": 5},
            {"id": 7, "title": "Sharing the Road", "duration": 840, "date_offset": 6},
            {"id": 8, "title": "Crashes and Traffic Stops", "duration": 660, "date_offset": 7},
            {"id": 9, "title": "Other Restrictions", "duration": 780, "date_offset": 8},
            {"id": 10, "title": "Insurance and Safety", "duration": 900, "date_offset": 9},
        ],
        "rookie": [
            {"id": i + 1, "title": f"Chapter {i + 1}", "duration": 720, "date_offset": 10 + i}
            for i in range(25)
        ]
    }


def generate_rss_feed(base_url="https://your-site.netlify.app"):
    """Generate RSS feed XML."""
    chapters = get_chapter_info()
    base_date = datetime(2024, 1, 1)
    
    items = []
    
    # Driver Manual episodes
    for ch in chapters["driver"]:
        pub_date = base_date + timedelta(days=ch["date_offset"])
        item = f"""    <item>
      <title>Chapter {ch['id']}: {ch['title']}</title>
      <description>Learn about {ch['title'].lower()} for the Maryland MVA exam.</description>
      <enclosure url="{base_url}/audio/driver-manual-chapter-{ch['id']:02d}.mp3" type="audio/mpeg" length="0"/>
      <itunes:title>Chapter {ch['id']}: {ch['title']}</itunes:title>
      <itunes:duration>{ch['duration']}</itunes:duration>
      <pubDate>{pub_date.strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>
      <guid>driver-manual-chapter-{ch['id']:02d}</guid>
    </item>"""
        items.append(item)
    
    # Rookie Manual episodes
    for ch in chapters["rookie"]:
        pub_date = base_date + timedelta(days=ch["date_offset"])
        item = f"""    <item>
      <title>Rookie Chapter {ch['id']}: {ch['title']}</title>
      <description>Learn about {ch['title'].lower()} for the Maryland MVA exam.</description>
      <enclosure url="{base_url}/audio/rookie-manual-chapter-{ch['id']:02d}.mp3" type="audio/mpeg" length="0"/>
      <itunes:title>Rookie Chapter {ch['id']}: {ch['title']}</itunes:title>
      <itunes:duration>{ch['duration']}</itunes:duration>
      <pubDate>{pub_date.strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>
      <guid>rookie-manual-chapter-{ch['id']:02d}</guid>
    </item>"""
        items.append(item)
    
    items_xml = "\n".join(items)
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Maryland MVA Study Podcast</title>
    <link>{base_url}</link>
    <language>en-us</language>
    <description>Audio review materials for the Maryland Driver's License Exam. Study for the MVA knowledge test with chapter-by-chapter audio guides.</description>
    <itunes:author>MVA Study Guide</itunes:author>
    <itunes:summary>Prepare for your Maryland driver's license exam with these audio study guides.</itunes:summary>
    <itunes:owner>
      <itunes:name>MVA Study Guide</itunes:name>
    </itunes:owner>
    <itunes:explicit>false</itunes:explicit>
    <itunes:category text="Education">
      <itunes:category text="Self-Improvement"/>
    </itunes:category>
    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>
    
{items_xml}
    
  </channel>
</rss>"""
    
    return rss


def generate_manifest():
    """Generate JSON manifest for the player."""
    chapters = get_chapter_info()
    
    manifest = {
        "title": "Maryland MVA Study Podcast",
        "description": "Audio review materials for the Maryland Driver's License Exam",
        "chapters": {
            "driver": [
                {
                    "id": ch["id"],
                    "title": ch["title"],
                    "file": f"driver-manual-chapter-{ch['id']:02d}.mp3",
                    "duration": ch["duration"]
                }
                for ch in chapters["driver"]
            ],
            "rookie": [
                {
                    "id": ch["id"],
                    "title": ch["title"],
                    "file": f"rookie-manual-chapter-{ch['id']:02d}.mp3",
                    "duration": ch["duration"]
                }
                for ch in chapters["rookie"]
            ]
        }
    }
    
    return manifest


def main():
    """Main function."""
    print("=" * 60)
    print("BUILDING PODCAST FEED AND MANIFEST")
    print("=" * 60)
    
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Generate RSS feed
    print("\nGenerating RSS feed...")
    rss = generate_rss_feed()
    rss_path = docs_dir / "feed.xml"
    rss_path.write_text(rss, encoding='utf-8')
    print(f"  Created: {rss_path}")
    
    # Generate manifest
    print("\nGenerating manifest...")
    manifest = generate_manifest()
    manifest_path = docs_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f"  Created: {manifest_path}")
    
    # Copy audio files
    print("\nCopying audio files to docs/audio...")
    audio_dir = docs_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    
    mp3_dir = Path("output/mp3")
    if mp3_dir.exists():
        count = 0
        for mp3_file in mp3_dir.glob("*.mp3"):
            (audio_dir / mp3_file.name).write_bytes(mp3_file.read_bytes())
            count += 1
        print(f"  Copied {count} MP3 files")
    else:
        print("  Warning: No MP3 files found in output/mp3")
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
