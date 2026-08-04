#!/usr/bin/env python3
"""Generate text-to-speech audio for fairy tale scenes using Google Gemini API."""

import json
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def generate_tts_for_book(book_dir, output_dir="audio"):
    """Generate TTS for all scenes in a book using Gemini API."""
    try:
        from google import genai
    except ImportError:
        print("Installing google-genai...")
        import subprocess
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

    print(f"🎤 Generating TTS for {total} scenes using Gemini API...\n")

    retry_delay = 2
    for idx, page in enumerate(scenes, 1):
        page_num = page.get('number', idx)
        title = page.get('title', '')
        body = page.get('body', '')
        narration_text = f"{title}. {body}".strip()

        if not narration_text:
            continue

        audio_file = audio_path / f"page_{page_num:02d}.mp3"
        print(f"[{idx}/{total}] Page {page_num}: {title[:40]}...", end=" ", flush=True)

        try:
            tts_interaction = client.interactions.create(
                model="gemini-3.1-flash-tts-preview",
                input=narration_text,
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": [
                        {"voice": "Puck"}
                    ]
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
                        import base64
                        audio_bytes = base64.b64decode(data)
                    else:
                        audio_bytes = bytes(data)
                else:
                    audio_bytes = bytes(audio_data)

                if audio_bytes:
                    with open(audio_file, 'wb') as f:
                        f.write(audio_bytes)
                    file_size = audio_file.stat().st_size / 1024
                    print(f"✓ ({file_size:.1f} KB)")
                    retry_delay = 2
                else:
                    print(f"✗ (Empty audio data)")
                    retry_delay = 5
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
    if len(sys.argv) > 1:
        book_name = sys.argv[1]

    book_dir = Path(__file__).parent / "books" / book_name

    if not book_dir.exists():
        print(f"❌ Book directory not found: {book_dir}")
        sys.exit(1)

    success = generate_tts_for_book(book_dir)
    sys.exit(0 if success else 1)
