#!/usr/bin/env python3
"""Generate fairy tale illustrations using Cloudflare Workers AI (Flux 1 Schnell)."""

import json
import requests
import base64
import sys
import os
from pathlib import Path
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # If python-dotenv not installed, read .env manually
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().strip().split("\n"):
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

# Cloudflare configuration from environment
CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
CF_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
CF_API_BASE = "https://api.cloudflare.com/client/v4"

if not CF_API_TOKEN or not CF_ACCOUNT_ID:
    print("❌ Error: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set in .env")
    sys.exit(1)

def get_cloudflare_account_id():
    """Get the Cloudflare account ID from environment or config."""
    # Try to read from environment variable
    import os
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

    if account_id:
        print("📋 Using account ID from env...", end=" ", flush=True)
        print(f"✓ ({account_id[:8]}...)")
        return account_id

    # If not in env, prompt user
    print("⚠️  Need Cloudflare Account ID")
    print("   Find it at: https://dash.cloudflare.com/?to=/:account/")
    account_id = input("   Enter your Account ID: ").strip()

    if account_id:
        return account_id
    else:
        return None

def generate_image_cloudflare(prompt: str, filename: str, output_dir: Path, account_id: str) -> bool:
    """Generate a single image using Cloudflare Workers AI."""
    output_path = output_dir / filename

    endpoint = f"{CF_API_BASE}/accounts/{account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "steps": 4  # Fast generation with 4 steps
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        # Response should contain the image data
        result = response.json()

        if "result" in result and "image" in result["result"]:
            # Image is returned as base64
            image_data = base64.b64decode(result["result"]["image"])

            with open(output_path, "wb") as f:
                f.write(image_data)

            if output_path.stat().st_size > 5000:
                return True

        return False

    except Exception as e:
        return False

def main():
    # Paths
    workspace = Path("/Users/user/Desktop/picturebook/_workspace/03")
    images_dir = Path("/Users/user/Desktop/picturebook/books/03-default-story/images")
    prompts_file = workspace / "02_art_director_prompts.json"
    log_file = workspace / "03_illustrator_log.md"

    images_dir.mkdir(parents=True, exist_ok=True)

    # Use configured Cloudflare account ID
    account_id = CF_ACCOUNT_ID
    print(f"📋 Using Cloudflare account: {account_id[:8]}...")

    # Load prompts
    print("📖 Loading prompts...", end=" ", flush=True)
    with open(prompts_file) as f:
        data = json.load(f)
    prompts = data.get("prompts", [])
    print(f"✓ ({len(prompts)} images)")

    print(f"\n🎨 Generating {len(prompts)} images using Cloudflare Flux 1 Schnell")
    print(f"📁 Output: {images_dir}\n")

    success = 0
    failed = 0
    failed_items = []

    for idx, prompt_obj in enumerate(prompts, 1):
        # Generate filename based on image type
        image_type = prompt_obj.get("type", "scene")
        if image_type == "cover":
            filename = "cover.png"
        else:
            scene_num = prompt_obj.get("image_number", idx) - 1  # 0-indexed for scenes
            filename = f"scene_{scene_num:02d}.png"

        english_prompt = prompt_obj.get("english_prompt", "")

        print(f"[{idx:2d}/{len(prompts)}] {filename:20s} ", end="", flush=True)

        if generate_image_cloudflare(english_prompt, filename, images_dir, account_id):
            print("✓")
            success += 1
        else:
            print("✗")
            failed += 1
            failed_items.append(filename)

    # Log results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"""
## Cloudflare Flux 1 Schnell Generation — {timestamp}

- Model: @cf/black-forest-labs/flux-1-schnell
- Total images: {len(prompts)}
- Generated: {success}
- Failed: {failed}
- Status: {'✓ All complete' if failed == 0 else f'⚠ {failed} failed'}
"""

    if failed_items:
        log_entry += f"\n- Failed items: {', '.join(failed_items)}\n"

    with open(log_file, "a") as f:
        f.write(log_entry)

    print(f"\n📊 Summary: {success}/{len(prompts)} generated")
    if failed > 0:
        print(f"⚠️  {failed} images failed")
    print(f"📝 Log: {log_file}\n")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
