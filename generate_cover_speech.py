#!/usr/bin/env python3
from google import genai
import wave
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
client = genai.Client(api_key=api_key)

# Load rabbit tale metadata
book_json_path = "books/01-rabbit-tale/book.json"
with open(book_json_path, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

# Extract cover page info
cover_page = book_data['pages'][0]
title = cover_page['title']
subtitle = cover_page['subtitle']

# Generate TTS for cover title
cover_text = f"{title}. {subtitle}"

interaction = client.interactions.create(
    model="gemini-2.5-flash-preview-tts",
    input=cover_text,
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [
            {"voice": "Kore"}
        ]
    }
)

output_path = "books/01-rabbit-tale/audio/cover.wav"
wave_file(output_path, base64.b64decode(interaction.output_audio.data))
print(f"✓ Generated {output_path}")
print(f"  Text: {cover_text}")
