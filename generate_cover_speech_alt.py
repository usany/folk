"""Alternative text-to-speech methods for book cover titles."""

import sys
from pathlib import Path


def generate_cover_speech_alt(book_dir, output_dir, cover_title, api_key):
    """Alternative method using gTTS."""
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
