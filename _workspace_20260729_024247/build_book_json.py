#!/usr/bin/env python3
"""Regenerate book/book.json from the storyteller scenario, and sync the
file:// fallback copy embedded in book/index.html."""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENARIO = ROOT / "_workspace" / "01_storyteller_scenario.json"
BOOK_JSON = ROOT / "book" / "book.json"
INDEX_HTML = ROOT / "book" / "index.html"

START = "<!-- BOOK_DATA_START -->"
END = "<!-- BOOK_DATA_END -->"


def scene_image(n):
    return f"images/scene_{n:02d}.png"


def build(scenario):
    scenes = scenario["scenes"]
    pages = [
        {
            "type": "cover",
            "image": "images/cover.png",
            "title": scenario["book_title"],
            "subtitle": scenario["subtitle"],
            "author": scenario["narrator"],
            "text": "",
        }
    ]

    for s in scenes:
        pages.append(
            {
                "type": "scene",
                "number": s["scene_number"],
                "title": s["title"],
                "text": s["text"],
                "image": scene_image(s["scene_number"]),
                "mood": s["emotion"],
            }
        )

    pages.append(
        {
            "type": "ending",
            "message": scenario["closing_line"],
            "image": scene_image(scenes[-1]["scene_number"]),
            "text": "",
        }
    )

    return {
        "title": scenario["book_title"],
        "subtitle": scenario["subtitle"],
        "author": scenario["narrator"],
        "description": (
            f"{scenario['narrator']}의 시선으로 다시 쓴 {len(scenes)}장면의 그림책. "
            f"{scenario['closing_line']}"
        ),
        "tone": scenario["tone"],
        "scene_count": len(scenes),
        "total_pages": len(pages),
        "cover": "images/cover.png",
        "pages": pages,
    }


def main():
    scenario = json.loads(SCENARIO.read_text(encoding="utf-8"))
    book = build(scenario)

    BOOK_JSON.write_text(
        json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {BOOK_JSON} ({book['total_pages']} pages)")

    if not INDEX_HTML.exists():
        return

    html = INDEX_HTML.read_text(encoding="utf-8")
    if START not in html or END not in html:
        print("index.html has no BOOK_DATA markers; skipped inline sync")
        return

    # Inline copy so the viewer also works when opened via file:// (fetch blocked).
    payload = json.dumps(book, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    block = (
        f'{START}\n  <script id="book-data" type="application/json">\n'
        f"{payload}\n  </script>\n  {END}"
    )
    html = re.sub(
        re.escape(START) + r".*?" + re.escape(END), lambda _: block, html, flags=re.S
    )
    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"synced inline fallback in {INDEX_HTML}")


if __name__ == "__main__":
    main()
