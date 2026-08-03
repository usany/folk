#!/usr/bin/env python3
"""Generate text-to-speech audio for book cover title using Gemini 3.1 Flash TTS model."""

import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_cover_speech(book_dir, output_dir="audio"):
    """Generate TTS for cover title using Gemini 3.1 Flash TTS model."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Installing google-generativeai...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-generativeai"])
        import google.generativeai as genai

    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False

    # Configure the API client
    genai.configure(api_key=api_key)

    book_json_path = Path(book_dir) / "book.json"

    if not book_json_path.exists():
        print(f"❌ Book file not found: {book_json_path}")
        return False

    # Load book data
    with open(book_json_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    # Get cover title
    cover_title = book_data.get('title', '')
    if not cover_title:
        print("❌ Cover title not found in book.json")
        return False

    # Create audio directory
    audio_path = Path(book_dir) / output_dir
    audio_path.mkdir(exist_ok=True)
    print(f"📁 Audio directory: {audio_path}")
    print(f"🎤 Cover title: {cover_title}\n")

    audio_file = audio_path / "cover_speech.wav"
    print(f"[1/1] Generating speech for cover title...", end=" ", flush=True)

    try:
        # Use the Gemini 3.1 Flash TTS model
        model = genai.GenerativeModel('gemini-3.1-flash-tts-preview')

        response = model.generate_content(
            genai.types.ContentType.text(cover_title)
        )

        # Check if response contains audio
        if response.data and hasattr(response, 'audio_data'):
            # Save the audio file
            with open(audio_file, 'wb') as f:
                f.write(response.audio_data)

            file_size = audio_file.stat().st_size / 1024
            print(f"✓ ({file_size:.1f} KB)")
            print(f"\n✅ Cover speech generated successfully!")
            print(f"📄 Output: {audio_file}")
            return True
        else:
            # Fallback: Try using the text-to-speech method if available
            print("\n⚠️  Audio not in response, trying alternative method...")
            return generate_cover_speech_alt(book_dir, output_dir, cover_title, api_key)

    except Exception as e:
        print(f"✗ ({str(e)})")
        print("\n⚠️  Trying alternative method...")
        return generate_cover_speech_alt(book_dir, output_dir, cover_title, api_key)

def generate_cover_speech_alt(book_dir, output_dir, cover_title, api_key):
    """Alternative method using gTTS or pyttsx3."""
    try:
        from gtts import gTTS
    except ImportError:
        print("Installing gtts...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gtts"])
        from gtts import gTTS

    audio_path = Path(book_dir) / output_dir
    audio_path.mkdir(exist_ok=True)

    audio_file = audio_path / "cover_speech.mp3"
    print(f"[1/1] Generating speech for cover title (using gTTS)...", end=" ", flush=True)

    try:
        # Use gTTS with Korean language
        tts = gTTS(text=cover_title, lang='ko', slow=False)
        tts.save(str(audio_file))

        file_size = audio_file.stat().st_size / 1024
        print(f"✓ ({file_size:.1f} KB)")
        print(f"\n✅ Cover speech generated successfully!")
        print(f"📄 Output: {audio_file}")
        return True
    except Exception as e:
        print(f"✗ ({str(e)})")
        return False

if __name__ == "__main__":
    book_name = "01-rabbit-tale"
    if len(sys.argv) > 1:
        book_name = sys.argv[1]

    book_dir = Path(__file__).parent / "books" / book_name

    if not book_dir.exists():
        print(f"❌ Book directory not found: {book_dir}")
        sys.exit(1)

    success = generate_cover_speech(book_dir)
    sys.exit(0 if success else 1)
