#!/usr/bin/env python3
"""Generate 100 stories using a GPT model via OpenRouter and save them to text files."""

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

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
MODEL = sys.argv[2] if len(sys.argv) > 2 else "openai/gpt-6-luna"
MODEL_SLUG = MODEL.replace("/", "_")
PROMPTS = {
    "en": "write a story",
    "nl": "schrijf een verhaal",
}
if LANG not in PROMPTS:
    print(f"Error: unsupported language '{LANG}'. Supported: {', '.join(PROMPTS)}")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent / "stories" / LANG / MODEL_SLUG
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://openrouter.ai/api/v1/chat/completions"
PROMPT = PROMPTS[LANG]
TOTAL_STORIES = 100

def generate_story() -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": PROMPT},
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
        return data["choices"][0]["message"]["content"]


def main():
    for i in range(1, TOTAL_STORIES + 1):
        file_path = OUTPUT_DIR / f"story_{i:03d}.txt"
        if file_path.exists():
            print(f"Skipping {file_path.name} (already exists)")
            continue

        print(f"Generating story {i}/{TOTAL_STORIES} ...")
        try:
            story = generate_story()
        except Exception as exc:
            print(f"Failed to generate story {i}: {exc}")
            continue

        file_path.write_text(story, encoding="utf-8")
        print(f"Saved {file_path.name}")

        if i < TOTAL_STORIES:
            time.sleep(1)

    print("Done.")


if __name__ == "__main__":
    main()
