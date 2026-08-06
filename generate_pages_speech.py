#!/usr/bin/env python3
from google import genai
import wave
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def generate_speech(text, output_path, api_key):
    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model="gemini-2.5-flash-preview-tts",
        input=text,
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": "Kore"}
            ]
        }
    )

    wave_file(output_path, base64.b64decode(interaction.output_audio.data))
    print(f"✓ Generated {output_path}")

api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")

# Load rabbit tale metadata
book_json_path = "books/01-rabbit-tale/book.json"
with open(book_json_path, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

audio_dir = "books/01-rabbit-tale/audio"
os.makedirs(audio_dir, exist_ok=True)

# Generate speech for all pages
for page in book_data['pages']:
    page_type = page['type']
    page_num = page['number']

    if page_type == 'cover':
        # Cover: title + subtitle
        text = f"{page['title']}. {page['subtitle']}"
        filename = f"page_00_cover.wav"

    elif page_type == 'scene':
        # Scene: title + body
        title = page.get('title', '')
        body = page.get('body', '')
        text = f"{title}. {body}"
        filename = f"page_{page_num:02d}_scene.wav"

    elif page_type == 'ending':
        # Ending: title + message
        title = page.get('title', '')
        message = page.get('message', '')
        text = f"{title}. {message}"
        filename = f"page_{page_num:02d}_ending.wav"
    else:
        continue

    output_path = os.path.join(audio_dir, filename)
    generate_speech(text, output_path, api_key)

print(f"\n✓ All pages speech generated for rabbit tale")
