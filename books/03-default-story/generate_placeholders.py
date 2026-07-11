#!/usr/bin/env python3
import json
import os
import base64
from anthropic import Anthropic
import concurrent.futures

client = Anthropic()

with open('/Users/user/Desktop/picturebook/_workspace/03/02_art_director_prompts.json') as f:
    data = json.load(f)

os.makedirs('/Users/user/Desktop/picturebook/books/03-default-story/images', exist_ok=True)

def generate_image(prompt_item):
    img_num = prompt_item['image_number']
    img_type = prompt_item['type']
    prompt = prompt_item['english_prompt']

    if img_type == 'cover':
        filename = 'cover.png'
    else:
        filename = f'scene_{img_num - 1:02d}.png'

    filepath = f'/Users/user/Desktop/picturebook/books/03-default-story/images/{filename}'

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        print(f'✗ {filename}: API does not support image generation via messages')
        return None
    except Exception as e:
        print(f'✗ {filename}: {str(e)}')
        return None

print("Attempting image generation using Claude API...")
for item in data['prompts']:
    generate_image(item)
print('Generation attempt complete')
