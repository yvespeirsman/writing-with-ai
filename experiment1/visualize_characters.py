#!/usr/bin/env python3
"""Visualize the most frequent character names per model from character CSV files as PNG."""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_TOP_N = 10


def find_character_csvs(base_dir: Path):
    """Find all characters.csv files under base_dir."""
    return list(base_dir.rglob("characters.csv"))


def parse_names(csv_path: Path):
    """Parse character names from a CSV file. Returns list of name strings."""
    names = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row.get("characters", "").strip()
            if not raw or raw.lower() == "none":
                continue
            for name in raw.split(","):
                name = name.strip()
                if name:
                    names.append(name)
    return names


def visualize_png(model: str, counter: Counter, top_n: int, output_path: Path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        print(f"Error: matplotlib is required for PNG output. ({exc})")
        sys.exit(1)

    most_common = counter.most_common(top_n)
    if not most_common:
        print(f"  [{model}] No characters to plot.")
        return

    names, counts = zip(*most_common)

    fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.5)))
    bars = ax.barh(range(len(names)), counts, color="#4a90d9")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlabel("Frequency")
    ax.set_title(f"Most Frequent Character Names – {model}\n(top {top_n})")
    ax.set_xlim(0, max(counts) * 1.15)

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            va="center",
            fontsize=9,
        )

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"  Saved {output_path}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <base_directory> [top_n]")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    if not base_dir.is_dir():
        print(f"Error: '{base_dir}' is not a directory.")
        sys.exit(1)

    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TOP_N

    csv_files = find_character_csvs(base_dir)
    if not csv_files:
        print(f"No characters.csv files found under '{base_dir}'.")
        sys.exit(0)

    print(f"Found {len(csv_files)} character CSV file(s).")

    model_counts = defaultdict(Counter)
    for csv_path in csv_files:
        model = csv_path.parent.name
        names = parse_names(csv_path)
        model_counts[model].update(names)
        print(f"  [{model}] {csv_path} → {len(names)} name(s)")

    print("\nGenerating PNG visualizations...")
    for model, counter in sorted(model_counts.items()):
        safe_model = "".join(c if c.isalnum() or c in "-_" else "_" for c in model)
        output_path = base_dir / f"characters_{safe_model}.png"
        visualize_png(model, counter, top_n, output_path)

    print("Done.")


if __name__ == "__main__":
    main()
