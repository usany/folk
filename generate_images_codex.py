#!/usr/bin/env python3
"""Generate fairy tale illustrations using codex (via ChatGPT)."""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_codex_image(prompt: str, filename: str, output_dir: Path) -> bool:
    """Generate a single image using codex image generation."""
    output_path = output_dir / filename

    try:
        # Use codex to generate image
        # The exact command might vary, but typically: codex imagine <prompt> -o <file>
        result = subprocess.run(
            ["codex", "imagine", prompt, "-o", str(output_path)],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"    ❌ codex error: {result.stderr[:100]}")
            return False

        if output_path.exists() and output_path.stat().st_size > 5000:
            print(f"    ✅ {output_path.name}")
            return True
        else:
            print(f"    ❌ file not created or too small")
            return False

    except subprocess.TimeoutExpired:
        print(f"    ❌ timeout")
        return False
    except Exception as e:
        print(f"    ❌ {str(e)[:60]}")
        return False

def main():
    # Paths
    workspace = Path("/Users/user/Desktop/picturebook/_workspace/03")
    images_dir = Path("/Users/user/Desktop/picturebook/books/03-default-story/images")
    prompts_file = workspace / "02_art_director_prompts.json"
    log_file = workspace / "03_illustrator_log.md"

    images_dir.mkdir(parents=True, exist_ok=True)

    # Load prompts
    with open(prompts_file) as f:
        data = json.load(f)

    prompts = data.get("prompts", [])

    print(f"\n🎨 Generating {len(prompts)} images using Codex")
    print(f"📁 Output: {images_dir}\n")

    success = 0
    failed = 0

    for idx, prompt_obj in enumerate(prompts, 1):
        filename = prompt_obj.get("filename", f"scene_{idx:02d}.png")
        english_prompt = prompt_obj.get("english_prompt", "")

        print(f"[{idx:2d}/{len(prompts)}] {filename}...", end=" ", flush=True)

        if run_codex_image(english_prompt, filename, images_dir):
            success += 1
        else:
            failed += 1

    # Log results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"""
## Codex Generation Run — {timestamp}

- Total images: {len(prompts)}
- Generated: {success}
- Failed: {failed}
- Status: {'✓ All complete' if failed == 0 else f'⚠ {failed} failed'}
"""

    with open(log_file, "a") as f:
        f.write(log_entry)

    print(f"\n📊 Summary: {success}/{len(prompts)} generated")
    print(f"📝 Log: {log_file}\n")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
