"""suki-focus: set or show which part of the stack the dashboard leads with.

Usage:
  suki focus                 # show current focus
  suki focus learning        # lead with the learning loop
  suki focus career          # lead with career tools
  suki focus all             # show everything

Stores a small preference at ~/.suki/profile/prefs.json.
"""
import argparse
import json
import os
import sys

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
PROFILE_DIR = os.path.join(SUKI_HOME, "profile")
PREFS_PATH = os.path.join(PROFILE_DIR, "prefs.json")

CHOICES = ["learning", "career", "all"]


def read_prefs():
    try:
        with open(PREFS_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def write_prefs(prefs):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    with open(PREFS_PATH, "w") as f:
        json.dump(prefs, f, indent=2)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Set the dashboard focus.")
    ap.add_argument("value", nargs="?", choices=CHOICES, default=None)
    args = ap.parse_args(argv)

    if args.value is None:
        current = read_prefs().get("focus", "all")
        print(f"focus: {current}")
        return 0

    prefs = read_prefs()
    prefs["focus"] = args.value
    write_prefs(prefs)
    print(f"focus set to: {args.value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
