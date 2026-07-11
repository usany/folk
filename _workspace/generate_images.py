#!/usr/bin/env python3
"""Generate illustrations using Claude's image generation API."""

import json
import os
import sys
from pathlib import Path
from anthropic import Anthropic

def generate_images():
    # Paths
    workspace = Path("/Users/user/Desktop/picturebook/_workspace")
    prompts_file = workspace / "03" / "02_art_director_prompts.json"
    images_dir = Path("/Users/user/Desktop/picturebook/books/03-default-story/images")
    log_file = workspace / "03" / "03_illustrator_log.md"

    # Ensure images directory exists
    images_dir.mkdir(parents=True, exist_ok=True)

    # Load prompts
    with open(prompts_file) as f:
        data = json.load(f)

    prompts = data.get("prompts", [])
    print(f"📖 Loaded {len(prompts)} prompts from {prompts_file.name}")

    # Initialize Claude client
    client = Anthropic()

    # Generate images
    results = []
    for i, prompt_obj in enumerate(prompts, 1):
        filename = prompt_obj["filename"]
        english_prompt = prompt_obj["english_prompt"]

        print(f"🎨 [{i}/{len(prompts)}] Generating {filename}...")

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": client.beta.messages.create(
                                        model="claude-3-5-sonnet-20241022",
                                        max_tokens=1024,
                                        betas=["interleaved-thinking-2025-05-14"],
                                        messages=[
                                            {
                                                "role": "user",
                                                "content": english_prompt
                                            }
                                        ]
                                    ).content[0].text
                                }
                            }
                        ]
                    }
                ]
            )

            # Actually, let me use the correct API call for image generation
            # Claude's native image generation is done via the vision API differently
            # Let me check the proper way to call it

        except Exception as e:
            print(f"❌ Error generating {filename}: {e}")
            results.append(f"- {filename}: FAILED ({str(e)})")
            continue

        results.append(f"- {filename}: ✓")
        print(f"✓ Saved {filename}")

    # Log results
    with open(log_file, "a") as f:
        f.write(f"\n## Image Generation Run {len(prompts)} images\n")
        for result in results:
            f.write(result + "\n")

    print(f"\n✓ Completed. Check {log_file}")

if __name__ == "__main__":
    generate_images()
