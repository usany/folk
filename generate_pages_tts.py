#!/usr/bin/env python3
from google import genai
import base64
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY', '').strip("'\"")
client = genai.Client(api_key=api_key)

book_name = "01-rabbit-tale"
if len(sys.argv) > 1:
    book_name = sys.argv[1]

book_dir = Path(__file__).parent / "books" / book_name
book_json = book_dir / "book.json"

with open(book_json, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

audio_dir = book_dir / "audio"
audio_dir.mkdir(exist_ok=True)

pages = book_data.get('pages', [])
scenes = [p for p in pages if p.get('type') == 'scene']
total = len(scenes)

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

print(f"🎤 Generating TTS for {total} pages...\n")

for idx, page in enumerate(scenes, 1):
    page_num = page.get('number', idx)
    title = page.get('title', '')
    body = page.get('body', '')

    tone = page.get('voice_tone', '')
    if not tone and page.get('emotion'):
        tone = emotion_to_tone.get(page.get('emotion'), '')

    text = f"{title}. {body}".strip()
    if tone:
        text = f"{tone}: {text}"

    output_file = audio_dir / f"page_{page_num:02d}.wav"
    print(f"[{idx}/{total}] Page {page_num}...", end=" ", flush=True)

    try:
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

        with open(output_file, 'wb') as f:
            f.write(base64.b64decode(interaction.output_audio.data))

        print(f"✓")

    except Exception as e:
        print(f"✗ ({str(e)[:40]})")

print(f"\n✅ Done!")
