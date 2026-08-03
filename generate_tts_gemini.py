#!/usr/bin/env python3
"""Generate text-to-speech audio for fairy tale scenes using Google Cloud TTS."""

import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_tts_for_book(book_dir, output_dir="audio"):
    """Generate TTS for all scenes in a book using Google Cloud Text-to-Speech."""
    try:
        from google.cloud import texttospeech
    except ImportError:
        print("Installing google-cloud-texttospeech...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-cloud-texttospeech"])
        from google.cloud import texttospeech

    # Get API key from environment and set as credential
    api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False

    # Set the API key for the TTS service
    os.environ['GOOGLE_API_KEY'] = api_key

    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print(f"❌ Failed to initialize TTS client: {e}")
        print("   Note: Google Cloud TTS requires additional setup.")
        print("   Using local pyttsx3 as fallback...\n")
        return generate_tts_local(book_dir, output_dir)

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

    pages = book_data.get('pages', [])
    scenes = [p for p in pages if p.get('type') == 'scene']
    total = len(scenes)

    print(f"🎤 Generating TTS for {total} scenes...\n")

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
            # Prepare the TTS request
            synthesis_input = texttospeech.SynthesisInput(text=narration_text)

            # Use Korean voice
            voice = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=0.0,
                speaking_rate=1.0,
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            # Save the audio file
            with open(audio_file, 'wb') as f:
                f.write(response.audio_content)

            file_size = audio_file.stat().st_size / 1024
            print(f"✓ ({file_size:.1f} KB)")

        except Exception as e:
            print(f"✗ ({str(e)[:40]})")
            continue

    print(f"\n✅ TTS generation complete!")
    return True

def generate_tts_local(book_dir, output_dir="audio"):
    """Fallback: Generate TTS using local pyttsx3 library."""
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

    with open(book_json_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    audio_path = Path(book_dir) / output_dir
    audio_path.mkdir(exist_ok=True)
    print(f"📁 Audio directory: {audio_path}")

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    pages = book_data.get('pages', [])
    scenes = [p for p in pages if p.get('type') == 'scene']
    total = len(scenes)

    print(f"🎤 Generating TTS for {total} scenes (local pyttsx3)...\n")

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
            engine.save_to_file(narration_text, str(audio_file))
            engine.runAndWait()
            print(f"✓")
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
