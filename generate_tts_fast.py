#!/usr/bin/env python3
"""Generate TTS audio files for fairy tale scenes using gTTS (fast)."""

import json
import sys
from pathlib import Path

def generate_tts_for_book(book_dir, output_dir="audio"):
    """Generate TTS using gTTS (Google Text-to-Speech)."""
    try:
        from gtts import gTTS
    except ImportError:
        print("Installing gTTS...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gtts"])
        from gtts import gTTS

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

    print(f"🎤 Generating TTS for {total} scenes using gTTS...\n")

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
            # Generate using gTTS (Korean language)
            tts = gTTS(text=narration_text, lang='ko', slow=False)
            tts.save(str(audio_file))

            file_size = audio_file.stat().st_size / 1024
            print(f"✓ ({file_size:.1f} KB)")

        except Exception as e:
            print(f"✗ ({str(e)[:40]})")
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
