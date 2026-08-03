#!/usr/bin/env python3
"""Generate TTS audio files for fairy tale books using pyttsx3 (offline)."""

import json
import sys
from pathlib import Path

def generate_tts_for_book(book_dir, output_dir="audio"):
    """Generate TTS for all pages in a book using pyttsx3."""
    try:
        import pyttsx3
    except ImportError:
        print("Installing pyttsx3...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyttsx3"])
        import pyttsx3

    book_json_path = Path(book_dir) / "book.json"

    if not book_json_path.exists():
        print(f"❌ Book file not found: {book_json_path}")
        return False

    # Load book data
    with open(book_json_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    # Create audio directory
    audio_path = Path(book_dir) / output_dir
    audio_path.mkdir(exist_ok=True)
    print(f"📁 Audio directory: {audio_path}")

    # Initialize TTS engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 0.9)  # Volume

    pages = book_data.get('pages', [])
    total = len([p for p in pages if p.get('type') != 'cover'])

    generated = 0
    for page in pages:
        page_num = page.get('number', 0)
        page_type = page.get('type', 'scene')

        # Skip cover page
        if page_type == 'cover':
            continue

        title = page.get('title', '')
        body = page.get('body', '')
        narration_text = f"{title}. {body}".strip()

        if not narration_text:
            continue

        audio_file = audio_path / f"page_{page_num:02d}.mp3"

        print(f"🎤 Generating audio for page {page_num}...", end=" ", flush=True)

        try:
            engine.save_to_file(narration_text, str(audio_file))
            engine.runAndWait()
            generated += 1
            print(f"✓")
        except Exception as e:
            print(f"✗ ({e})")

    print(f"\n✅ Generated {generated} audio files in {audio_path}")
    return True

if __name__ == "__main__":
    book_name = "01-rabbit-tale"
    if len(sys.argv) > 1:
        book_name = sys.argv[1]

    book_dir = Path(__file__).parent / "books" / book_name
    success = generate_tts_for_book(book_dir)
    sys.exit(0 if success else 1)
