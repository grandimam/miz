"""miz-topics: list topics under ~/.miz/topics/."""
import json
import os
import sys

MIZ_HOME = os.environ.get("MIZ_HOME", os.path.expanduser("~/.miz"))
TOPICS_DIR = os.path.join(MIZ_HOME, "topics")


def topic_slugs():
    if not os.path.isdir(TOPICS_DIR):
        return []
    out = []
    for name in sorted(os.listdir(TOPICS_DIR)):
        if os.path.isfile(os.path.join(TOPICS_DIR, name, "curriculum.json")):
            out.append(name)
    return out


def summarize(slug):
    path = os.path.join(TOPICS_DIR, slug, "mastery.json")
    try:
        with open(path) as f:
            mastery = json.load(f)
    except (OSError, ValueError):
        return {"total": 0, "mastered": 0}
    chapters = mastery.get("chapters", {})
    total = len(chapters)
    mastered = sum(1 for c in chapters.values() if c.get("status") == "mastered")
    return {"total": total, "mastered": mastered}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    verbose = "--verbose" in argv or "-v" in argv
    slugs = topic_slugs()
    if not slugs:
        print("NO_TOPICS: run the curriculum skill to create one", file=sys.stderr)
        return 1
    for slug in slugs:
        if verbose:
            s = summarize(slug)
            print(f"{slug}\t{s['mastered']}/{s['total']} mastered")
        else:
            print(slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())