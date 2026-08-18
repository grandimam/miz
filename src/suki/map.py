"""suki-map: render a topic's whole guide as a visual tree.

Usage:
  suki map python                # parts -> chapters, with status
  suki map python --color never

Reads curriculum.json + mastery.json. Prints a book-like table of contents
with the mastery status of every chapter.
"""
import argparse
import json
import os
import sys

from .status import STATUS_COLOR, paint, set_color

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
TOPICS_DIR = os.path.join(SUKI_HOME, "topics")

STATUS_ICON = {
    "mastered": "✓",
    "credited": "✓",
    "in_progress": "~",
    "probed": "?",
    "not_started": "·",
}


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Render a topic as a status tree.")
    ap.add_argument("slug")
    ap.add_argument("--color", default="auto", choices=["auto", "always", "never"])
    args = ap.parse_args(argv)
    set_color(args.color)

    tdir = os.path.join(TOPICS_DIR, args.slug)
    if not os.path.isdir(tdir):
        print(f"NO_TOPIC: {args.slug} (run the curriculum skill first)", file=sys.stderr)
        return 1
    curriculum = load_json(os.path.join(tdir, "curriculum.json")) or {}
    mastery = load_json(os.path.join(tdir, "mastery.json")) or {}

    chapters = mastery.get("chapters", {})
    print(paint(curriculum.get("topic", args.slug), "bold"))
    print(paint("  " + (curriculum.get("book_thesis") or "learn it in order, prove each chapter"), "dim"))

    tiers = curriculum.get("tiers", [])
    if not tiers:
        print("  (no tiers yet)")
        return 0

    for tier in tiers:
        name = tier.get("name", tier.get("tier", ""))
        print(paint(f"\nTier {tier.get('tier', '')}: {name}", "cyan"))
        for ch in tier.get("chapters", []):
            cid = ch.get("id", "?")
            st = chapters.get(cid, {}).get("status", "not_started")
            icon = STATUS_ICON.get(st, "·")
            label = paint(f"{icon} {cid} {ch.get('title', '')}", STATUS_COLOR.get(st, "dim"))
            print(f"  {label}")

    mastered = sum(1 for c in chapters.values() if c.get("status") in ("mastered", "credited"))
    total = len(chapters)
    if total:
        print(paint(f"\n{mastered}/{total} chapters mastered", "green" if mastered == total else "yellow"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
