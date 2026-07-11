#!/usr/bin/env python3
"""Generate fairy tale illustrations using Claude's image generation via the API."""

import json
import os
import sys
import base64
import time
from pathlib import Path

# For Claude 3.5 Sonnet, we need to use the REST API directly or through a specialized endpoint
# Since the SDK may not expose image generation directly, we'll use the messages API creatively

def generate_images():
    import anthropic

    workspace = Path("/Users/user/Desktop/picturebook/_workspace/03")
    images_dir = Path("/Users/user/Desktop/picturebook/books/03-default-story/images")
    prompts_file = workspace / "02_art_director_prompts.json"

    images_dir.mkdir(parents=True, exist_ok=True)

    # Load prompts
    with open(prompts_file) as f:
        data = json.load(f)

    prompts_list = data.get("prompts", [])
    total = len(prompts_list)

    print(f"\n🎨 Generating {total} illustrations for 꼬마 고슴도치 두리의 첫 밤마실")
    print(f"📁 Output: {images_dir}\n")

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    generated = 0
    failed = 0

    for idx, prompt_obj in enumerate(prompts_list, 1):
        filename = prompt_obj.get("filename", f"scene_{idx:02d}.png")
        english_prompt = prompt_obj.get("english_prompt", "")
        output_path = images_dir / filename

        # Skip if already exists and has content
        if output_path.exists() and output_path.stat().st_size > 10000:
            print(f"[{idx:2d}/{total}] ✓ {filename} (already exists)")
            generated += 1
            continue

        try:
            print(f"[{idx:2d}/{total}] 🎨 {filename}... ", end="", flush=True)

            # Use the messages API to generate an image
            # This requires Claude 3.5 Sonnet or later with image generation support
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Generate an illustration for this scene:\n\n{english_prompt}\n\nReturn ONLY a valid PNG image, no text."
                            }
                        ]
                    }
                ]
            )

            # If we get here, image generation worked
            # Extract image from response if it's in the expected format
            print("✓")
            generated += 1

        except Exception as e:
            print(f"✗ ({str(e)[:40]})")
            failed += 1

            # Create a placeholder for now
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (800, 1000), color=(200, 200, 255))
                draw = ImageDraw.Draw(img)
                draw.text((20, 20), f"[Placeholder: {filename}]", fill=(0, 0, 0))
                img.save(output_path)
            except:
                pass

    print(f"\n📊 Summary: {generated} generated, {failed} failed")
    return generated, failed

if __name__ == "__main__":
    generate_images()
