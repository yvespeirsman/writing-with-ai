#!/usr/bin/env python3
"""Extract character names from stories using OpenRouter and save to CSV."""

import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable is not set.")
    sys.exit(1)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <stories_folder>")
    sys.exit(1)

STORIES_DIR = Path(sys.argv[1])
if not STORIES_DIR.is_dir():
    print(f"Error: '{STORIES_DIR}' is not a directory.")
    sys.exit(1)

OUTPUT_CSV = STORIES_DIR / "characters.csv"

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-6-luna"

EXTRACTION_PROMPT = (
    "List all character names mentioned in the following story. "
    "Return only the names separated by commas, with no extra text or explanation. "
    "If there are no characters, return 'None'.\n\n"
)


def extract_characters(story_text: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": EXTRACTION_PROMPT + story_text},
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()


def main():
    story_files = sorted(STORIES_DIR.glob("*.txt"))
    if not story_files:
        print(f"No .txt files found in '{STORIES_DIR}'.")
        sys.exit(0)

    print(f"Found {len(story_files)} story files. Processing...")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "characters"])

        for i, story_path in enumerate(story_files, start=1):
            print(f"[{i}/{len(story_files)}] Extracting from {story_path.name} ...")
            try:
                story_text = story_path.read_text(encoding="utf-8")
                characters = extract_characters(story_text)
            except Exception as exc:
                print(f"  Failed: {exc}")
                characters = ""

            writer.writerow([story_path.name, characters])
            print(f"  -> {characters}")

            if i < len(story_files):
                time.sleep(1)

    print(f"Done. Saved results to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
