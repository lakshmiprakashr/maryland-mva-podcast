#!/usr/bin/env python3
"""
Generate audio files from extracted text using edge-tts or piper.
"""

import asyncio
import subprocess
import sys
from pathlib import Path
import yaml

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


def load_config():
    """Load configuration from podcast.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "podcast.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


async def generate_with_edge_tts(text, output_path, voice, rate, pitch):
    """Generate audio using edge-tts."""
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))


def generate_with_piper(text_file, output_path, model, sentence_silence):
    """Generate audio using piper."""
    cmd = [
        "python3", "-m", "piper",
        "-m", model,
        "-f", str(output_path),
        "--sentence-silence", str(sentence_silence),
        "--input-file", str(text_file)
    ]
    subprocess.run(cmd, check=True)


def convert_wav_to_mp3(wav_path, mp3_path, quality="256k"):
    """Convert WAV to MP3 using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", str(wav_path),
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",
        "-y", str(mp3_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)


async def process_chapter_edge_tts(manual_type, chapter_id, config):
    """Process a single chapter using edge-tts."""
    
    tts_config = config.get('tts', {})
    voice_config = config.get('voices', {})
    
    voice = voice_config.get('default', 'en-US-GuyNeural')
    settings = voice_config.get('settings', {})
    rate = settings.get('rate', '-5%')
    pitch = settings.get('pitch', '+0Hz')
    
    # Read extracted text
    input_dir = Path(__file__).parent.parent / "output" / "wav"
    input_path = input_dir / f"{manual_type.lower()}-chapter-{chapter_id}.txt"
    
    if not input_path.exists():
        print(f"  Warning: {input_path} not found, skipping")
        return None
    
    with open(input_path) as f:
        text = f.read()
    
    # Generate MP3
    output_dir = Path(__file__).parent.parent / "output" / "mp3"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"{manual_type.lower()}-chapter-{chapter_id}.mp3"
    
    print(f"  Generating: {output_path.name} with {voice}...")
    await generate_with_edge_tts(text, output_path, voice, rate, pitch)
    
    # Note: SRT generation can be added later with edge-tts SubMaker
    # For now, we focus on MP3 generation
    return output_path


def process_chapter_piper(manual_type, chapter_id, config):
    """Process a single chapter using piper."""
    
    tts_config = config.get('tts', {})
    piper_config = tts_config.get('piper', {})
    
    model = piper_config.get('model', 'en_US-lessac-medium')
    sentence_silence = piper_config.get('sentence_silence', 0.5)
    
    # Read extracted text
    input_dir = Path(__file__).parent.parent / "output" / "wav"
    input_path = input_dir / f"{manual_type.lower()}-chapter-{chapter_id}.txt"
    
    if not input_path.exists():
        print(f"  Warning: {input_path} not found, skipping")
        return None
    
    # Generate WAV
    wav_dir = Path(__file__).parent.parent / "output" / "wav"
    wav_path = wav_dir / f"{manual_type.lower()}-chapter-{chapter_id}.wav"
    
    print(f"  Generating: {wav_path.name} with piper...")
    generate_with_piper(input_path, wav_path, model, sentence_silence)
    
    # Convert to MP3
    mp3_dir = Path(__file__).parent.parent / "output" / "mp3"
    mp3_dir.mkdir(parents=True, exist_ok=True)
    
    mp3_path = mp3_dir / f"{manual_type.lower()}-chapter-{chapter_id}.mp3"
    convert_wav_to_mp3(wav_path, mp3_path)
    
    print(f"  Created: {mp3_path.name}")
    return mp3_path


async def process_chapter(manual_type, chapter_id, config):
    """Process a single chapter."""
    tts_provider = config.get('tts', {}).get('provider', 'edge-tts')
    
    if tts_provider == 'edge-tts' and HAS_EDGE_TTS:
        return await process_chapter_edge_tts(manual_type, chapter_id, config)
    elif tts_provider == 'piper':
        return process_chapter_piper(manual_type, chapter_id, config)
    else:
        print(f"  Error: TTS provider '{tts_provider}' not available")
        return None


async def main():
    """Main entry point."""
    config = load_config()
    
    print("=" * 60)
    print("MARYLAND MVA PODCAST - AUDIO GENERATION")
    print("=" * 60)
    
    # Process Driver Manual
    print("\nDriver Manual:")
    driver_chapters = config['chapters']['driver_manual']
    for chapter in driver_chapters:
        await process_chapter("Driver-Manual", chapter['id'], config)
    
    # Process Rookie Manual
    print("\nRookie Manual:")
    rookie_chapters = config['chapters']['rookie_manual']
    for chapter in rookie_chapters:
        await process_chapter("Rookie-Manual", chapter['id'], config)
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    
    # List generated files
    mp3_dir = Path(__file__).parent.parent / "output" / "mp3"
    if mp3_dir.exists():
        mp3_files = list(mp3_dir.glob("*.mp3"))
        print(f"\nGenerated {len(mp3_files)} MP3 files:")
        for f in sorted(mp3_files):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  {f.name} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    asyncio.run(main())
