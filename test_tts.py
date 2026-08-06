#!/usr/bin/env python3
from google import genai
import wave
import base64
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

interaction = client.interactions.create(
    model="gemini-2.5-flash-preview-tts",
    input="Say cheerfully: Have a wonderful day!",
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [
            {"voice": "Kore"}
        ]
    }
)

with open('out.wav', 'wb') as f:
    f.write(base64.b64decode(interaction.output_audio.data))
print("✓ Generated out.wav")
