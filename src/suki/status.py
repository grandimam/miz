"""suki-status: deterministic progress + spaced-repetition status for topics.

Usage:
  suki-status                 # all topics, human table
  suki-status python          # one topic
  suki-status python --json   # machine-readable
  suki-status --due           # only chapters due for review (all topics)
  suki-status python --due    # only chapters due for review (one topic)

Reads curriculum.json + mastery.json under ~/.suki/topics/<slug>/.
A mastered chapter is "due" when now >= next_review_at. If next_review_at is
absent, it falls back to mastered_at/probed_at + a 1-day default interval.
"""
import datetime as dt
import json
import os
import sys

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
TOPICS_DIR = os.path.join(SUKI_HOME, "topics")
DEFAULT_INTERVAL_DAYS = 1.0

STATUS_ORDER = ["not_started", "in_progress", "probed", "mastered", "credited"]


def now():
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(value):
    if not value:
        return None
    try:
        v = value.replace("Z", "+00:00")
        d = dt.datetime.fromisoformat(v)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d
    except ValueError:
        return None


def topic_slugs():
    if not os.path.isdir(TOPICS_DIR):
        return []
    return sorted(
        n for n in os.listdir(TOPICS_DIR)
        if os.path.isfile(os.path.join(TOPICS_DIR, n, "curriculum.json"))
    )


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def chapter_due(chapter):
    """Return the due datetime for a mastered chapter, or None if not due yet."""
    next_review = parse_iso(chapter.get("next_review_at"))
    if next_review:
        return next_review
    base = parse_iso(chapter.get("mastered_at")) or parse_iso(chapter.get("probed_at"))
    if not base:
        return now()  # mastered but never timestamped -> due now
    return base + dt.timedelta(days=DEFAULT_INTERVAL_DAYS)


def topic_report(slug):
    tdir = os.path.join(TOPICS_DIR, slug)
    mastery = load_json(os.path.join(tdir, "mastery.json")) or {}
    curriculum = load_json(os.path.join(tdir, "curriculum.json")) or {}
    chapters = mastery.get("chapters", {})

    counts = {s: 0 for s in STATUS_ORDER}
    for ch in chapters.values():
        s = ch.get("status", "not_started")
        counts[s] = counts.get(s, 0) + 1
    total = len(chapters)
    mastered = counts.get("mastered", 0) + counts.get("credited", 0)

    titles = {}
    for tier in curriculum.get("tiers", []):
        for c in tier.get("chapters", []):
            titles[c.get("id")] = c.get("title", "")

    due = []
    ts = now()
    for cid, ch in sorted(chapters.items()):
        if ch.get("status") != "mastered":
            continue
        d = chapter_due(ch)
        if d and d <= ts:
            due.append({"chapter": cid, "title": titles.get(cid, ""), "due_at": d.isoformat()})

    return {
        "slug": slug,
        "topic": curriculum.get("topic", slug),
        "total": total,
        "counts": counts,
        "progress_pct": round(100.0 * mastered / total, 1) if total else 0.0,
        "reviews_due": due,
    }


def print_table(reports):
    for r in reports:
        c = r["counts"]
        print(f"\n{r['topic']}  [{r['slug']}]  {r['progress_pct']}%")
        parts = [f"{r['total']} chapters"]
        for s in STATUS_ORDER:
            if c.get(s):
                parts.append(f"{c[s]} {s}")
        print("  " + " | ".join(parts))
        if r["reviews_due"]:
            print(f"  reviews due: {len(r['reviews_due'])}")
            for d in r["reviews_due"]:
                print(f"    - {d['chapter']} {d['title']}")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = [a for a in argv]
    as_json = "--json" in args
    due_only = "--due" in args
    args = [a for a in args if not a.startswith("--")]
    slug = args[0] if args else None

    slugs = [slug] if slug else topic_slugs()
    if slug and slug not in topic_slugs():
        print(f"NO_TOPIC: {slug} (run the curriculum skill first)", file=sys.stderr)
        return 1
    if not slugs:
        print("NO_TOPICS: run the curriculum skill to create one", file=sys.stderr)
        return 1

    reports = [topic_report(s) for s in slugs]

    if due_only:
        due = []
        for r in reports:
            for d in r["reviews_due"]:
                due.append({"slug": r["slug"], **d})
        if as_json:
            print(json.dumps(due, indent=2))
        elif due:
            for d in due:
                print(f"{d['slug']}\t{d['chapter']}\t{d['title']}")
        else:
            print("No reviews due.")
        return 0

    if as_json:
        print(json.dumps(reports, indent=2))
    else:
        print_table(reports)
    return 0


if __name__ == "__main__":
    sys.exit(main())