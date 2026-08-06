#!/usr/bin/env python3
"""Generate TTS for fairy tale scenes using google.genai SDK."""

import json
import sys
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def generate_tts_for_book(book_dir, output_dir="audio"):
    """Generate TTS for all scenes in a book."""
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

    print(f"🎤 Generating TTS for {total} scenes using google.genai...\n")

    # Emotion to voice tone mapping
    emotion_to_tone = {
        '조심스러운 호소, 은밀함': 'Say in a cautious, secretive whisper',
        '위협, 압도': 'Say in a menacing, threatening tone',
        '공포, 굴복': 'Say in a fearful, trembling voice',
        '의식화된 위압, 고립': 'Say in a tense, isolated whisper',
        '필사적 질주, 불길한 위화감': 'Say desperately while breathless',
        '매복, 충격': 'Say in shocked, panicked tone',
        '버려짐, 잔인한 대비': 'Say sadly with bitter irony',
        '일상 속 불시의 충격': 'Say in startled, confused tone',
        '압도적 배신감': 'Say with overwhelming despair',
        '조작된 진실, 조롱': 'Say with bitter resignation',
    }

    retry_delay = 2
    for idx, page in enumerate(scenes, 1):
        page_num = page.get('number', idx)
        title = page.get('title', '')
        body = page.get('body', '')

        # Get voice tone instruction
        voice_tone = page.get('voice_tone', '')
        if not voice_tone and page.get('emotion'):
            voice_tone = emotion_to_tone.get(page.get('emotion'), '')

        # Build narration with voice tone
        narration_text = f"{title}. {body}".strip()
        if voice_tone:
            narration_text = f"{voice_tone}: {narration_text}"

        if not narration_text:
            continue

        audio_file = audio_path / f"page_{page_num:02d}.mp3"
        print(f"[{idx}/{total}] Page {page_num}: {title[:40]}...", end=" ", flush=True)

        try:
            # Use gemini-3.1-flash-tts-preview with google.genai
            response = client.models.generate_content(
                model="gemini-3.1-flash-tts-preview",
                contents=narration_text
            )

            # Extract audio data from response
            audio_bytes = b""
            if hasattr(response, 'audio_data') and response.audio_data:
                audio_bytes = response.audio_data
            elif hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        audio_bytes = part.inline_data.data
                        break

            if audio_bytes and len(audio_bytes) > 100:
                with open(audio_file, 'wb') as f:
                    f.write(audio_bytes)
                file_size = audio_file.stat().st_size / 1024
                print(f"✓ ({file_size:.1f} KB)")
                retry_delay = 2
            else:
                print(f"✗ (No/empty audio: {len(audio_bytes)} bytes)")
                retry_delay = 5

        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'quota' in error_msg.lower():
                print(f"✗ (Rate limited, waiting {retry_delay}s)")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
            else:
                print(f"✗ ({error_msg[:60]})")
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
