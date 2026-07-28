#!/usr/bin/env python3
"""Batch image generation via Cloudflare Workers AI (Flux 1 Schnell).

Usage:
  python3 generate_images_cloudflare.py <prompts.json> <output_dir> [filename ...]

If filenames are given, only those prompts are (re)generated.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

MODEL = "@cf/black-forest-labs/flux-1-schnell"
ROOT = os.path.dirname(os.path.abspath(__file__))


def load_env(path):
    env = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def ensure_png(path):
    """Cloudflare may return JPEG bytes. Normalize to real PNG."""
    with open(path, "rb") as fh:
        magic = fh.read(8)
    if magic.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if magic.startswith(b"\xff\xd8\xff"):
        tmp = path + ".jpg"
        os.rename(path, tmp)
        subprocess.run(
            ["sips", "-s", "format", "png", tmp, "--out", path],
            check=True, capture_output=True,
        )
        os.remove(tmp)
        return "jpeg->png"
    return "unknown"


def generate(account_id, token, item, outdir):
    filename = item["filename"]
    prompt = item["prompt"]
    t0 = time.time()
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{MODEL}"
    body = json.dumps({"prompt": prompt, "steps": 4}).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:400]
        return {"filename": filename, "ok": False,
                "error": f"HTTP {e.code}: {detail}"}
    except Exception as e:  # noqa: BLE001
        return {"filename": filename, "ok": False, "error": f"{type(e).__name__}: {e}"}

    if not payload.get("success", False):
        return {"filename": filename, "ok": False,
                "error": f"API errors: {payload.get('errors')}"}

    b64 = payload.get("result", {}).get("image")
    if not b64:
        return {"filename": filename, "ok": False,
                "error": f"no image in result keys={list(payload.get('result', {}).keys())}"}

    dest = os.path.join(outdir, filename)
    with open(dest, "wb") as fh:
        fh.write(base64.b64decode(b64))
    fmt = ensure_png(dest)
    return {"filename": filename, "ok": True, "bytes": os.path.getsize(dest),
            "format": fmt, "secs": round(time.time() - t0, 1)}


def main():
    prompts_path, outdir = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])

    env = load_env(os.path.join(ROOT, ".env"))
    account_id = env.get("CLOUDFLARE_ACCOUNT_ID")
    token = env.get("CLOUDFLARE_API_TOKEN")
    if not account_id or not token:
        sys.exit("ERROR: CLOUDFLARE_API_TOKEN / CLOUDFLARE_ACCOUNT_ID missing in .env")

    with open(prompts_path) as fh:
        data = json.load(fh)
    items = data["prompts"]
    if only:
        items = [i for i in items if i["filename"] in only]

    os.makedirs(outdir, exist_ok=True)
    print(f"Generating {len(items)} images -> {outdir}", flush=True)

    with ThreadPoolExecutor(max_workers=9) as pool:
        results = list(pool.map(
            lambda i: generate(account_id, token, i, outdir), items))

    for r in sorted(results, key=lambda r: r["filename"]):
        if r["ok"]:
            print(f"OK   {r['filename']}  {r['bytes']:,} bytes  ({r['format']})  {r['secs']}s")
        else:
            print(f"FAIL {r['filename']}  {r['error']}")

    failed = [r["filename"] for r in results if not r["ok"]]
    print(f"\nSUMMARY: {len(results) - len(failed)}/{len(results)} succeeded")
    if failed:
        print("FAILED: " + ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
