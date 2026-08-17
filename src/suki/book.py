"""suki-book: assemble a suki topic into a publication-quality teaching book via pandoc + LaTeX.

Usage:
  suki-book python                 # build book.pdf + book.tex
  suki-book python --paper a4      # a5 (default), a4, or letter
  suki-book python --tex-only      # stop at book.tex, no PDF compile
  suki-book python --keep-md       # keep the intermediate markdown

Reads curriculum.json, mastery.json, probes.jsonl, practice.jsonl from
~/.suki/topics/<slug>/ and writes book/ inside the same directory.
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
HERE = os.path.dirname(os.path.realpath(__file__))

STATUS_LABEL = {
    "not_started": "Not started",
    "in_progress": "In progress",
    "probed": "Probed",
    "mastered": "Mastered",
    "credited": "Credited (prior experience)",
}

GEOMETRY = {
    "a5": ["inner=1.6cm", "outer=2.1cm", "top=2.1cm", "bottom=2.3cm"],
    "a4": ["inner=2.2cm", "outer=2.8cm", "top=2.6cm", "bottom=3.0cm"],
    "letter": ["inner=2.2cm", "outer=2.8cm", "top=2.6cm", "bottom=3.0cm"],
}

FONT_FALLBACKS = {
    "main": ["TeX Gyre Pagella", "Palatino", "Charter", "Georgia", "Source Serif 4", "Liberation Serif", "Times New Roman"],
    "sans": ["TeX Gyre Heros", "Helvetica Neue", "Helvetica", "Arial", "Liberation Sans"],
    "mono": ["TeX Gyre Cursor", "Menlo", "DejaVu Sans Mono", "Consolas", "Liberation Mono"],
}

HEADER_INCLUDES = r"""
\usepackage{microtype}
\usepackage{longtable,booktabs,array,calc}
\usepackage{scrlayer-scrpage}
\pagestyle{scrheadings}
\automark[chapter]{chapter}
\addtokomafont{disposition}{\rmfamily}
\subject{\textsc{The Qalam Series}}
"""


def default_template():
    candidates = [
        os.environ.get("QALAM_BOOK_TEMPLATE"),
        os.path.normpath(os.path.join(HERE, "skills", "book", "template.latex")),  # package data
        os.path.normpath(os.path.join(HERE, "..", "..", "book", "template.latex")),  # repo
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return candidates[1]


DEFAULT_TEMPLATE = default_template()


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


def available_fonts():
    try:
        out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True, timeout=15)
        families = set()
        for line in out.stdout.splitlines():
            for name in line.split(","):
                families.add(name.strip())
        return families
    except (OSError, subprocess.TimeoutExpired):
        return set()


def pick_fonts():
    families = available_fonts()
    chosen = {}
    for key, candidates in FONT_FALLBACKS.items():
        chosen[key] = next((c for c in candidates if c in families), candidates[-1])
    return chosen


def author_name():
    try:
        out = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, timeout=5
        )
        name = out.stdout.strip()
        if name:
            return name
    except (OSError, subprocess.TimeoutExpired):
        pass
    return os.environ.get("USER", "Anonymous")


def chapters_flat(curriculum):
    for tier in curriculum.get("tiers", []):
        for ch in tier.get("chapters", []):
            yield tier, ch


def sentence_list(items):
    items = [str(i).strip() for i in items if str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def shorten(text, limit=180):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:")
    return cut + "..."


def chapter_overview(chapter):
    concepts = chapter.get("concepts", [])
    goals = chapter.get("goals", [])
    title = chapter.get("title", "This chapter")
    if concepts and goals:
        return (
            f"{title} introduces {sentence_list(concepts[:3])}. By the end, the learner should be able to "
            f"{sentence_list(goals[:2]).lower()}. The point is not exposure; it is being able to use these ideas deliberately."
        )
    if concepts:
        return (
            f"{title} is centered on {sentence_list(concepts[:3])}. Work this chapter until those ideas are usable, "
            "not merely recognizable."
        )
    if goals:
        return (
            f"{title} is built around doing, not browsing. By the end, the learner should be able to "
            f"{sentence_list(goals[:2]).lower()}."
        )
    return f"{title} should be studied as a skill-building chapter rather than a survey."


def concept_explanation(chapter, model):
    concepts = chapter.get("concepts", [])
    if model and model.get("model"):
        return shorten(model.get("model", ""), 420)
    if concepts:
        return (
            f"The core of this chapter is understanding {sentence_list(concepts[:4])}. "
            "These ideas should connect to one another as a mechanism or workflow, not as isolated terms."
        )
    return ""


def chapter_emphasis(chapter):
    drills = chapter.get("drills", [])
    checks = chapter.get("mastery_check", [])
    parts = []
    if drills:
        parts.append(
            f"Use the practice work to force decisions and explanations, especially {shorten(drills[0], 120)}"
        )
    if checks:
        parts.append(
            f"The self-checks should be answered with reasoning, not slogans; for example: {shorten(checks[0], 120)}"
        )
    return " ".join(parts)


def build_foreword(curriculum, mastery, probes, practices):
    chapters = mastery.get("chapters", {})
    total = len(chapters)
    counts = {}
    for ch in chapters.values():
        s = ch.get("status", "not_started")
        counts[s] = counts.get(s, 0) + 1
    mastered = counts.get("mastered", 0)
    credited = counts.get("credited", 0)

    next_ch = None
    for _, ch in chapters_flat(curriculum):
        st = chapters.get(ch["id"], {}).get("status", "not_started")
        if st in ("not_started", "in_progress"):
            next_ch = ch
            break

    lines = [
        "# Foreword {.unnumbered}",
        "",
        f"This volume is a structured guide to **{curriculum.get('topic', '')}**.",
        "It is organized as a teachable path from first principles to advanced",
        "practice. Each part is a tier of the curriculum; each chapter packages",
        "goals, core ideas, drills, and self-check questions in an order that",
        "supports cumulative understanding.",
        "",
        "| Tier | Name | Chapters |",
        "|------|------|----------|",
    ]
    for tier in curriculum.get("tiers", []):
        lines.append(f"| {tier.get('tier', '')} | {tier.get('name', '')} | {len(tier.get('chapters', []))} |")
    lines += [
        "",
        f"**Coverage snapshot.** {total} total chapters, with {mastered + credited} already validated"
        + (f" ({credited} credited from prior experience)" if credited else "")
        + ".",
    ]
    if next_ch:
        lines.append(f"For the original learner, the next unfinished chapter is {next_ch['id']}, *{next_ch['title']}*.")
    else:
        lines.append("The original learner completed every chapter; the book remains as a reusable path for others.")
    lines += [
        "",
        f"The guide was refined using {len(probes)} probe sessions and {len(practices)} remediation sessions.",
        "",
    ]
    return "\n".join(lines)


def chapter_teaching_material(cid, mastery, probes, practices, models):
    chapter_state = mastery.get("chapters", {}).get(cid, {})
    cprobes = [p for p in probes if p.get("chapter") == cid]
    cpractices = [p for p in practices if p.get("chapter") == cid]
    model = models.get(cid)

    lines = []

    pitfalls = []
    seen = set()
    for probe in cprobes:
        for result in probe.get("results", []):
            if result.get("verdict") == "SOLID":
                continue
            note = (result.get("note") or result.get("q") or "").strip()
            if note and note not in seen:
                seen.add(note)
                pitfalls.append(note)
    for practice in cpractices:
        for target in practice.get("targets", []):
            target = (target or "").strip()
            if target and target not in seen:
                seen.add(target)
                pitfalls.append(target)

    if pitfalls:
        lines += ["### Common pitfalls", ""]
        lines += [f"- {p}" for p in pitfalls[:6]]
        lines += [""]

    if model and model.get("open_questions"):
        lines += ["### Questions to extend the chapter", ""]
        lines += [f"- {q}" for q in model.get("open_questions", []) if q]
        lines += [""]

    status = chapter_state.get("status")
    if status:
        label = STATUS_LABEL.get(status, status)
        lines += [f"*Validation status in the source learning run: {label}.*", ""]

    return lines


def build_body(curriculum, mastery, probes, practices, models):
    lines = []
    for tier in curriculum.get("tiers", []):
        lines += [f"# Tier {tier.get('tier', '')} — {tier.get('name', '')}", ""]
        lines += [
            f"This tier develops the {tier.get('name', '').lower()} layer of the topic. "
            "Study the chapters in order; later chapters assume the earlier ones have been worked through actively.",
            "",
        ]
        for ch in tier.get("chapters", []):
            lines += [f"## {ch['id']} {ch.get('title', '')}", ""]
            lines += [
                "### Overview",
                "",
                chapter_overview(ch),
                "",
            ]
            explanation = concept_explanation(ch, models.get(ch["id"]))
            if explanation:
                lines += ["### Teach the idea", "", explanation, ""]
            if ch.get("goals"):
                lines += ["### Goals", ""] + [f"- {g}" for g in ch["goals"]] + [""]
            if ch.get("concepts"):
                lines += ["### Core ideas", ""] + [f"- {c}" for c in ch["concepts"]] + [""]
            if ch.get("drills"):
                lines += ["### Practice", ""] + [f"{i}. {d}" for i, d in enumerate(ch["drills"], 1)] + [""]
            if ch.get("mastery_check"):
                lines += ["### Check yourself", ""] + [f"{i}. {q}" for i, q in enumerate(ch["mastery_check"], 1)] + [""]
            emphasis = chapter_emphasis(ch)
            if emphasis:
                lines += ["### Teaching emphasis", "", emphasis, ""]
            est = ch.get("est_hours")
            if est:
                lines += [f"*Estimated effort: {est} hours.*", ""]
            lines += chapter_teaching_material(ch["id"], mastery, probes, practices, models)

    lines += [r"\backmatter", "", r"\chapter*{How To Use This Book}", r"\markboth{How To Use This Book}{}", ""]
    lines += [
        "Work the chapters in order. For each chapter:",
        "",
        "1. Read the overview and goals.",
        "2. Make sure you can explain each core idea in your own words.",
        "3. Do the practice tasks without skipping the hard ones.",
        "4. Use the check-yourself questions to verify understanding.",
        "5. Revisit the common pitfalls before moving on.",
        "",
    ]
    return "\n".join(lines)


def run_pandoc(args_list):
    proc = subprocess.run(args_list, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(f"pandoc failed (exit {proc.returncode})")


def pandoc_latex_fragment(markdown_text):
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--top-level-division=chapter"],
        input=markdown_text, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(f"pandoc failed (exit {proc.returncode})")
    return proc.stdout


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Render a suki topic as a LaTeX book.")
    ap.add_argument("slug")
    ap.add_argument("--paper", choices=sorted(GEOMETRY), default="a5")
    ap.add_argument("--tex-only", action="store_true", help="emit book.tex without compiling")
    ap.add_argument("--keep-md", action="store_true", help="keep intermediate markdown")
    ap.add_argument("--engine", default=os.environ.get("QALAM_PDF_ENGINE", "xelatex"))
    args = ap.parse_args(argv)

    if not shutil.which("pandoc"):
        sys.exit("pandoc is not installed (brew install pandoc)")
    template = os.environ.get("QALAM_BOOK_TEMPLATE", DEFAULT_TEMPLATE)
    if not os.path.isfile(template):
        sys.exit(f"template not found: {template}")

    topic_dir = os.path.join(SUKI_HOME, "topics", args.slug)
    curriculum = load_json(os.path.join(topic_dir, "curriculum.json"))
    if not curriculum:
        sys.exit(f"NO_CURRICULUM: run the curriculum skill for {args.slug} first")
    mastery = load_json(os.path.join(topic_dir, "mastery.json")) or {"chapters": {}}
    models = load_json(os.path.join(topic_dir, "models.json")) or {}
    probes = load_jsonl(os.path.join(topic_dir, "probes.jsonl"))
    practices = load_jsonl(os.path.join(topic_dir, "practice.jsonl"))

    out_dir = os.path.join(topic_dir, "book")
    os.makedirs(out_dir, exist_ok=True)
    book_md = os.path.join(out_dir, "book.md")
    foreword_tex = os.path.join(out_dir, "foreword.tex")
    with open(foreword_tex, "w") as f:
        f.write(pandoc_latex_fragment(build_foreword(curriculum, mastery, probes, practices)))
    with open(book_md, "w") as f:
        f.write(build_body(curriculum, mastery, probes, practices, models))

    fontsize = "10pt" if args.paper == "a5" else "11pt"
    today = dt.date.today().strftime("%B %d, %Y")
    fonts = pick_fonts()
    mainfont = os.environ.get("QALAM_MAINFONT", fonts["main"])
    sansfont = os.environ.get("QALAM_SANSFONT", fonts["sans"])
    monofont = os.environ.get("QALAM_MONOFONT", fonts["mono"])
    common = [
        "pandoc", book_md,
        "--template", template,
        "--top-level-division=part",
        "--include-before-body", foreword_tex,
        "--toc",
        "-V", "toc-depth=0",
        "-V", "documentclass=scrbook",
        "-V", f"fontsize={fontsize}",
        "-V", f"papersize={args.paper}",
        "-V", "classoption=openright",
        "-V", "classoption=titlepage",
        "-V", "has-frontmatter=true",
        "-V", "indent=true",
        "-V", "linestretch=1.05",
        "-V", "colorlinks=true",
        "-V", f"mainfont={mainfont}",
        "-V", f"sansfont={sansfont}",
        "-V", f"monofont={monofont}",
        "-V", f"header-includes={HEADER_INCLUDES.strip()}",
        "-M", f"title={curriculum.get('topic', args.slug)}",
        "-M", "subtitle=Structured Guide and Practice Manual",
        "-M", f"author={author_name()}",
        "-M", f"date={today}",
    ]
    for g in GEOMETRY[args.paper]:
        common += ["-V", f"geometry={g}"]

    tex_path = os.path.join(out_dir, "book.tex")
    run_pandoc(common + ["-s", "-o", tex_path])
    print(f"wrote {tex_path}")

    if args.tex_only:
        return

    if not shutil.which(args.engine):
        sys.exit(f"{args.engine} not found — install a TeX distribution or use --tex-only")
    pdf_path = os.path.join(out_dir, "book.pdf")
    run_pandoc(common + ["--pdf-engine", args.engine, "-o", pdf_path])
    print(f"wrote {pdf_path}")

    if not args.keep_md:
        os.remove(book_md)
        os.remove(foreword_tex)


if __name__ == "__main__":
    main()