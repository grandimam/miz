"""suki-status: deterministic progress + spaced-repetition status for topics.

Usage:
  suki status                      # all topics, human table
  suki status python               # one topic
  suki status python --json        # machine-readable
  suki status --due                # only chapters due for review (all topics)
  suki status python --due         # only chapters due for review (one topic)
  suki status --color always       # auto / always / never

Reads curriculum.json + mastery.json under ~/.suki/topics/<slug>/.
A mastered chapter is "due" when now >= next_revisit_at (probe's field;
next_review_at is accepted as a legacy alias). If neither is present, it
falls back to mastered_at/probed_at + a 1-day default interval.
"""
import datetime as dt
import json
import os
import sys

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
TOPICS_DIR = os.path.join(SUKI_HOME, "topics")
DEFAULT_INTERVAL_DAYS = 1.0

STATUS_ORDER = ["not_started", "in_progress", "probed", "mastered", "credited"]

STATUS_COLOR = {
    "not_started": "dim",
    "in_progress": "yellow",
    "probed": "cyan",
    "mastered": "green",
    "credited": "green",
}

_USE_COLOR = "auto"


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


def set_color(mode):
    global _USE_COLOR
    _USE_COLOR = mode


def use_color():
    if _USE_COLOR == "never":
        return False
    if _USE_COLOR == "always":
        return True
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def paint(text, style):
    if not use_color():
        return text
    codes = {
        "reset": "0",
        "bold": "1",
        "dim": "2",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
    }
    code = codes.get(style)
    if not code:
        return text
    return f"\x1b[{code}m{text}\x1b[0m"


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


def load_jsonl(path):
    rows = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    return rows


def chapter_due(chapter):
    """Return the due datetime for a mastered chapter, or None if not due yet."""
    next_review = parse_iso(chapter.get("next_revisit_at")) or parse_iso(chapter.get("next_review_at"))
    if next_review:
        return next_review
    base = parse_iso(chapter.get("mastered_at")) or parse_iso(chapter.get("probed_at"))
    if not base:
        return now()  # mastered but never timestamped -> due now
    return base + dt.timedelta(days=DEFAULT_INTERVAL_DAYS)


def chapter_titles(curriculum):
    titles = {}
    for tier in curriculum.get("tiers", []):
        for c in tier.get("chapters", []):
            titles[c.get("id")] = c.get("title", "")
    return titles


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

    titles = chapter_titles(curriculum)

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


def progress_bar(pct, width=10):
    filled = int(round(pct / 100.0 * width))
    bar = "█" * filled + "░" * (width - filled)
    color = "green" if pct >= 80 else ("yellow" if pct >= 40 else "red")
    return paint(bar, color)


def print_table(reports):
    if not reports:
        return
    # compute column width for the topic column
    topic_w = max(len(r["topic"]) for r in reports)
    for r in reports:
        c = r["counts"]
        pct = r["progress_pct"]
        header = f"{paint(r['topic'], 'bold')}  {paint(progress_bar(pct), '')}"
        print(f"\n{header}  {paint(f'{pct:.1f}%', 'cyan')}")
        parts = [f"{r['total']} chapters"]
        for s in STATUS_ORDER:
            if c.get(s):
                parts.append(paint(f"{c[s]} {s}", STATUS_COLOR[s]))
        print("  " + " | ".join(parts))
        if r["reviews_due"]:
            label = paint(f"reviews due: {len(r['reviews_due'])}", "red")
            print(f"  {label}")
            for d in r["reviews_due"]:
                print(f"    - {paint(d['chapter'], 'yellow')} {d['title']}")


def human_due(when):
    ts = now()
    delta = when - ts
    secs = delta.total_seconds()
    if secs < 0:
        return paint("due now", "red")
    days = secs / 86400
    if days < 1:
        hours = max(1, int(secs / 3600))
        return f"in {hours}h"
    return f"in {int(round(days))}d"


def print_due(due):
    """Aligned columns: slug / chapter / title / due-in."""
    if not due:
        print(paint("No reviews due.", "green"))
        return
    rows = []
    for d in due:
        due_at = parse_iso(d["due_at"])
        rows.append((d["slug"], d["chapter"], d["title"], human_due(due_at) if due_at else ""))
    slug_w = max(len(r[0]) for r in rows)
    ch_w = max(len(r[1]) for r in rows)
    for slug, ch, title, when in rows:
        print(f"{paint(slug.ljust(slug_w), 'bold')}  {ch.ljust(ch_w)}  {title}  {when}")


def learning_streak():
    """Consecutive days with at least one probe session across all topics."""
    days = set()
    for slug in topic_slugs():
        for row in load_jsonl(os.path.join(TOPICS_DIR, slug, "probes.jsonl")):
            at = parse_iso(row.get("at"))
            if at:
                days.add(at.date())
    if not days:
        return 0
    today = now().date()
    if today not in days:
        today -= dt.timedelta(days=1)  # today not yet probed: streak can still be alive
        if today not in days:
            return 0
    streak = 0
    d = today
    while d in days:
        streak += 1
        d -= dt.timedelta(days=1)
    return streak


def streak_line(reports):
    streak = learning_streak()
    total_topics = len(reports)
    due_count = sum(len(r["reviews_due"]) for r in reports)
    parts = []
    if streak:
        parts.append(paint(f"🔥 {streak}-day learning streak", "yellow"))
    if total_topics:
        parts.append(f"{total_topics} topic{'s' if total_topics != 1 else ''}")
    if due_count:
        parts.append(paint(f"{due_count} review{'s' if due_count != 1 else ''} due", "red"))
    elif reports:
        parts.append(paint("no reviews due", "green"))
    return "  ".join(parts) if parts else ""


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = [a for a in argv]
    as_json = "--json" in args
    due_only = "--due" in args
    color = "auto"
    clean = []
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--color"):
            if "=" in a:
                color = a.split("=", 1)[1]
            elif i + 1 < len(args) and args[i + 1] in ("auto", "always", "never"):
                color = args[i + 1]
                i += 1
            else:
                color = "always"
        elif not a.startswith("--"):
            clean.append(a)
        i += 1
    if color not in ("auto", "always", "never"):
        print(f"unknown --color value: {color} (auto|always|never)", file=sys.stderr)
        return 1
    set_color(color)
    slug = clean[0] if clean else None

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
        else:
            print_due(due)
        return 0

    if as_json:
        print(json.dumps(reports, indent=2))
    else:
        line = streak_line(reports)
        if line:
            print(line)
        print_table(reports)
    return 0


if __name__ == "__main__":
    sys.exit(main())
