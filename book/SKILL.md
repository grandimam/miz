---
name: book
description: |
  Render a topic's curriculum, working models, and probe/remediation records as a
  publication-quality teaching book via pandoc. Produces book.pdf (and
  book.tex) in ~/.suki/topics/<slug>/book/ - KOMA scrbook, XeLaTeX,
  microtype, Palatino-class typography, table of contents, one part per tier,
  and reusable chapter material for other learners. Use when asked to "make a
  book", "export my curriculum as a book/PDF", "turn this into a study guide",
  or "publish this topic for others".
---

## Preamble (run first)

```bash
TOPIC_SLUG="<slug from user message>"
TOPIC_DIR="$HOME/.suki/topics/$TOPIC_SLUG"
if [ ! -f "$TOPIC_DIR/curriculum.json" ]; then
  echo "NO_CURRICULUM: run curriculum for $TOPIC_SLUG first"
else
  echo "TOPIC_DIR: $TOPIC_DIR"
fi
command -v pandoc >/dev/null 2>&1 && echo "pandoc: ok" || echo "pandoc: MISSING"
command -v xelatex >/dev/null 2>&1 && echo "xelatex: ok" || echo "xelatex: MISSING"
```

If `NO_CURRICULUM`, stop - run `curriculum` first. If `pandoc` or `xelatex`
is missing, tell the user how to install (`brew install pandoc` and a TeX
distribution such as MacTeX/Tex Live) and offer `--tex-only` if only xelatex
is missing.

# Publisher

You render the topic into a reusable teaching volume. The book is a study
guide, not a diary - it should be usable by someone other than the original
learner.

**HARD GATE:** Do NOT modify any state file. You only render. Do NOT change
the curriculum or mastery.

---

## Phase 1: Render

Run the assembler:

```bash
suki book "$TOPIC_SLUG" --keep-md
```

It reads `curriculum.json`, `mastery.json`, `models.json`, `probes.jsonl`,
and `practice.jsonl`, then turns them into a teachable book:

- the curriculum provides the syllabus and chapter sequence
- saved models can contribute concise chapter explanations
- probe/practice history is mined for common pitfalls, weak distinctions, and
  drills worth preserving for future learners

It writes the manuscript markdown, converts it to LaTeX through
`book/template.latex`, and compiles `book.pdf`.

If the user wants a different paper size, add `--paper a4` (default is `a5`,
the book size) or `--paper letter`. For only the `.tex` (e.g. to hand-tune),
add `--tex-only`.

---

## Phase 2: Report

Print:

1. The path to `book.pdf` (and `book.tex` if `--tex-only`).
2. A one-line summary: number of tiers, chapters, mastered count.
3. Where it lives: `$HOME/.suki/topics/<slug>/book/`.
4. That the manuscript markdown is kept for inspection (`--keep-md` was passed)
   and can be removed safely.
5. That the output is a reusable teaching book, not just a session log.

Offer to open it: `open "$TOPIC_DIR/book/book.pdf"`
