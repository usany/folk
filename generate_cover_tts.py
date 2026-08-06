#!/usr/bin/env python3
from google import genai
import base64
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def save_audio(filename, audio_bytes):
    with open(filename, 'wb') as f:
        f.write(audio_bytes)

api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
client = genai.Client(api_key=api_key)

book_name = "01-rabbit-tale"
if len(sys.argv) > 1:
    book_name = sys.argv[1]

book_dir = Path(__file__).parent / "books" / book_name
book_json = book_dir / "book.json"

with open(book_json, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

cover_title = book_data.get('title', '')
print(f"📚 {cover_title}")
print("🎤 Generating TTS...", end=" ", flush=True)

input_text = f"Say in an spooky whisper: {cover_title}"

interaction = client.interactions.create(
    model="gemini-3.1-flash-tts-preview",
    input=input_text,
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [
            {"voice": "Kore"}
        ]
    }
)

output_file = book_dir / "audio" / "cover_speech.mp3"
output_file.parent.mkdir(exist_ok=True)

save_audio(str(output_file), base64.b64decode(interaction.output_audio.data))

size = output_file.stat().st_size / 1024
print(f"✓ ({size:.1f}KB)")
print(f"📄 {output_file}")
