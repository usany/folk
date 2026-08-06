#!/usr/bin/env python3
"""Generate text-to-speech audio for fairy tale scenes using Google Gemini API - FIXED VERSION."""

import json
import sys
import time
import base64
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def generate_tts_for_book(book_dir, output_dir="audio", output_format="mp3"):
    """Generate TTS for all scenes in a book using Gemini API.

    Args:
        book_dir: Path to book directory
        output_dir: Output directory for audio files (relative to book_dir)
        output_format: Output format ('mp3' or 'wav')
    """
    try:
        from google import genai
    except ImportError:
        print("Installing google-genai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-genai"])
        from google import genai

    api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False

    client = genai.Client(api_key=api_key)

    book_json_path = Path(book_dir) / "book.json"
    if not book_json_path.exists():
        print(f"❌ Book file not found: {book_json_path}")
        return False

    with open(book_json_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    audio_path = Path(book_dir) / output_dir
    audio_path.mkdir(exist_ok=True)
    print(f"📁 Audio directory: {audio_path}")

    pages = book_data.get('pages', [])
    scenes = [p for p in pages if p.get('type') == 'scene']
    total = len(scenes)

    print(f"🎤 Generating TTS for {total} scenes using Gemini API (format: {output_format})...\n")

    # Check for ffmpeg if converting to WAV
    if output_format == "wav":
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("⚠️  ffmpeg not found. Install it for WAV conversion: brew install ffmpeg")
            print("   Falling back to MP3 format.\n")
            output_format = "mp3"

    retry_delay = 2
    for idx, page in enumerate(scenes, 1):
        page_num = page.get('number', idx)
        title = page.get('title', '')
        body = page.get('body', '')
        narration_text = f"{title}. {body}".strip()

        if not narration_text:
            continue

        file_ext = output_format
        audio_file = audio_path / f"page_{page_num:02d}.{file_ext}"
        print(f"[{idx}/{total}] Page {page_num}: {title[:40]}...", end=" ", flush=True)

        try:
            # FIX: Use speech_config as dict, not list
            tts_interaction = client.interactions.create(
                model="gemini-3.1-flash-tts-preview",
                input=narration_text,
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": {"voice": "Puck"}  # Changed from list to dict
                }
            )

            if hasattr(tts_interaction, 'output_audio') and tts_interaction.output_audio:
                audio_data = tts_interaction.output_audio
                # Handle different audio data formats
                if isinstance(audio_data, bytes):
                    audio_bytes = audio_data
                elif hasattr(audio_data, 'data'):
                    data = audio_data.data
                    if isinstance(data, bytes):
                        audio_bytes = data
                    elif isinstance(data, str):
                        # FIX: Properly decode base64 if needed
                        try:
                            audio_bytes = base64.b64decode(data)
                        except Exception:
                            audio_bytes = data.encode() if isinstance(data, str) else bytes(data)
                    else:
                        audio_bytes = bytes(data)
                else:
                    audio_bytes = bytes(audio_data)

                # FIX: Validate audio data
                if not audio_bytes or len(audio_bytes) < 100:
                    print(f"✗ (Corrupted/empty audio data, size: {len(audio_bytes)} bytes)")
                    retry_delay = 5
                    continue

                # FIX: Save to temporary MP3 first
                temp_mp3 = audio_path / f".temp_page_{page_num:02d}.mp3"
                with open(temp_mp3, 'wb') as f:
                    f.write(audio_bytes)

                # Convert to WAV if requested
                if output_format == "wav":
                    try:
                        subprocess.run(
                            ["ffmpeg", "-i", str(temp_mp3), "-acodec", "pcm_s16le",
                             "-ar", "24000", str(audio_file), "-y"],
                            capture_output=True,
                            check=True,
                            timeout=10
                        )
                        temp_mp3.unlink()  # Remove temp MP3
                    except subprocess.CalledProcessError as e:
                        print(f"✗ (WAV conversion failed: {e.stderr.decode()[:50]})")
                        continue
                    except subprocess.TimeoutExpired:
                        print(f"✗ (WAV conversion timeout)")
                        continue
                else:
                    # Keep as MP3
                    temp_mp3.rename(audio_file)

                file_size = audio_file.stat().st_size / 1024
                print(f"✓ ({file_size:.1f} KB)")
                retry_delay = 2
            else:
                print(f"✗ (No audio output)")
                retry_delay = 5

        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'quota' in error_msg.lower():
                print(f"✗ (Rate limited, waiting {retry_delay}s)")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
            else:
                print(f"✗ ({error_msg[:70]})")
            continue

    print(f"\n✅ TTS generation complete!")
    return True


if __name__ == "__main__":
    book_name = "01-rabbit-tale"
    output_format = "mp3"

    if len(sys.argv) > 1:
        book_name = sys.argv[1]
    if len(sys.argv) > 2:
        output_format = sys.argv[2].lower()

    book_dir = Path(__file__).parent / "books" / book_name

    if not book_dir.exists():
        print(f"❌ Book directory not found: {book_dir}")
        sys.exit(1)

    success = generate_tts_for_book(book_dir, output_format=output_format)
    sys.exit(0 if success else 1)
