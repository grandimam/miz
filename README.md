# Suki

**Build the curriculum. Probe it progressively.**

```
╭───────────────────────────────────────────────╮
│                    s u k i                    │
│ Build the curriculum. Probe it progressively. │
╰───────────────────────────────────────────────╯
```

Suki turns an AI coding agent into a learning partner that doesn't trust
you. Not in a moral sense. It refuses to believe you know something just
because you read it, watched a course, or nodded along with a tutorial.

The pattern is simple: **you build the curriculum, then the agent probes you
on it, progressively.** First you design the definitive guide to a topic,
chapter by chapter. Then you work through it, and the agent forces you to say
each chapter back from your own head, pokes at the cracks, repairs them on the
spot, and schedules re-probes before what you learned fades. Each pass builds
on the last. Nothing is graded against you; everything is recorded as an
artifact that compounds.

**🔒 Local-first** · **🛡️ Private by default** · **🧩 2 steps, one command** · **🐍 Python 3 + your agent**

## The loop: build it, then get probed on it

```
   /suki curriculum <topic>        /suki probe <topic> [ch]
   ┌──────────────┐               ┌──────────────┐
   │  design the  │ ─────────────►│  say it back │──────────┐
   │  definitive  │   chapter by  │  probe the   │          │
   │  guide       │   chapter     │  cracks      │          │
   └──────────────┘               └──────────────┘          │
        ▲                                                   │
        │              /suki probe <topic> 1.1            next
        └────────────  again when it's due                  │
                       (3 → 10 → 30 → 90 days)              ▼
                                                     ┌──────────────┐
                                                     │   mastered   │
                                                     └──────────────┘
```

- **`/suki curriculum <topic>`**: design the definitive learning path: the
  parts, the chapters, the order, what "mastered" means at every chapter. The
  agent authors it like a field expert writing a real guide, from absolute
  basics to the deepest expert end of the topic, then writes it as
  chapter-by-chapter markdown plus a `curriculum.json` every later step reads.
- **`/suki probe <topic> [ch]`**: build and verify understanding chapter by
  chapter. The agent forces a restatement of *your* picture, probes it for
  cracks, and grades it honestly. Weak spots are repaired inline with
  targeted mini-drills, then the chapter is scored and scheduled for review
  at 3 → 10 → 30 → 90 days so it doesn't rot.

Work compounds: each step writes an artifact to `~/.suki/topics/<slug>/` that
the next step reads. Probe again next week, and the loop knows exactly what
you were weak at and brings it back before it fades.

## 📐 Step 1: Build the curriculum

```
/suki curriculum active-directory

  → the agent designs the whole book first
      · the thesis: what the field is fundamentally about
      · the ontology: the entities and forces that organize it
      · the recurring ideas that unify distant chapters
      · what "expert" actually means at the deep end

  → table of contents: parts → chapters → estimated hours
  → then it authors each chapter like a definitive guide:
      · real mechanisms, worked examples, failure modes
      · drills that make you do, not just read
      · mastery_check questions probe will use later

  → you confirm the TOC, the agent writes in order
```

Suki doesn't hand you a syllabus. It writes a guide that compresses the field
into a coherent way of seeing, the kind of book that takes a complete
beginner all the way to expert judgment, and stays useful as a reference after
you've mastered it. Every chapter carries its own drills and mastery checks,
so the next step has something real to test you on.

| Command | What it does |
|---------|--------------|
| `/suki curriculum <topic>` | Design a definitive learning path: parts, chapters, order, mastery checks |
| `/suki learn <draft>` | Review a chapter draft from a serious learner's perspective (runs inside curriculum) |

## 🔬 Step 2: Get probed, progressively

```
/suki probe active-directory 1.1

  "Explain Kerberos authentication in your own words."

  → you state your picture
  → suki probes it, one question at a time
      SOLID    correct, with reasoning
      SHALLOW  right words, no understanding  → one targeted follow-up
      WRONG    incorrect or "I don't know"    → repair inline
  → weak spot? a mini-drill fixes it right there
  → mastered? revisit in 3 → 10 → 30 → 90 days
```

The model has to be in **your** words, not the book's. The agent never writes
the answer for you: it forces a restatement, scores it honestly, and if it
doesn't hold up, exposes the gap and repairs it right there. Your weak spots
are remembered and resurfaced before they fade. Mastered chapters stay on the
revisit schedule; everything else comes back for another round.

| Command | What it does |
|---------|--------------|
| `/suki probe <topic> [ch]` | Build + verify understanding chapter by chapter; repair cracks; spaced repetition |

## 📖 The payoff: a book you can prove you hold

```
/suki book active-directory     # -> ~/.suki/topics/active-directory/book/book.pdf

  → your curriculum, as one part per tier
  → your working models, persisted
  → your probe + remediation history
  → typeset with pandoc + LaTeX (KOMA scrbook, Palatino)
```

Everything you built and validated becomes a real teaching book: the same
material other learners can use, and the proof of what you actually hold.

| Command | What it does |
|---------|--------------|
| `/suki book <topic>` | Render the topic as a publication-quality teaching book |

## See it in action

One command, `/suki`, is the status dashboard and the router to everything
else. It knows where you left off and what's due next.

```
╭───────────────────────────────────────────────╮
│                    s u k i                    │
│ Build the curriculum. Probe it progressively. │
╰───────────────────────────────────────────────╯

📊  Status
────────────────────────────────────────────
  Learning  3 topics · 1 due for review

⏳  Due for review
────────────────────────────────────────────
  • active-directory 2.1 (Kerberos auth)  due today
  • python 3.1 (Asyncio)                  due in 2d

Next step
  → /suki probe active-directory 2.1
────────────────────────────────────────────
```

## Quick start

```bash
pip install suki
suki install --all     # links the skills into opencode, claude, and codex
```

That's it. Restart your agent, then:

```bash
suki demo                  # optional: feel the loop on a sample topic first
/suki curriculum python    # build the definitive guide
/suki probe python 1.1     # say it back, get probed, repair, schedule
/suki probe python 1.1     # again when it's due: the loop, forever
/suki book python          # publish what you mastered
```

## 🧠 The skills

| Skill | Role |
|-------|------|
| `suki` | Status dashboard + router (single entry point) |
| `curriculum` | Design a definitive learning path |
| `learn` | Review material from a learner's perspective |
| `probe` | Build + verify understanding, repair cracks, spaced repetition |
| `book` | Render a topic as a teaching book |

## 🗂️ State

Everything lives under `~/.suki/`, one folder per topic. Current state is
JSON; history is append-only JSONL. Nothing is ever deleted, so the full
arc of your learning is recoverable.

```
~/.suki/
└── topics/<slug>/        # curriculum.json, mastery.json, probes, book/
```

The `suki` CLI manages the stack:

- `suki install [--opencode|--claude|--codex|--all]`: link skills into your agent
- `suki topics`: list topics
- `suki status [topic]`: progress bars + spaced-repetition due status (+ `--due`, `--json`, `--color`)
- `suki map <topic>`: render the whole guide as a status tree
- `suki demo [--force]`: seed a sample topic and feel the loop in 60 seconds
- `suki export` / `suki import <file>`: back up or restore `~/.suki` (import never clobbers)
- `suki focus [learning|career|all]`: choose what the dashboard leads with
- `suki book <topic>`: render a topic as a book (+ `--preview <tier>` for a fast single-tier draft)

## 📦 Install

```bash
pip install suki
suki install --all
```

That's the whole setup. `pip install suki` gives you the `suki` command;
`suki install` links all five skills (`suki`, `curriculum`, `learn`,
`probe`, `book`) into your agent. Default to `--all`, or pick just your
agent with `--opencode`, `--claude`, or `--codex`.

Restart your agent after installing, then use `/suki` as the single entry
point. It routes subcommands: `/suki curriculum <topic>`,
`/suki learn <draft>`, `/suki probe <topic> [ch]`, `/suki book <topic>`,
or `/suki` alone for the status dashboard.

**From source (contributing):**

```bash
git clone <this repo> && cd suki
pip install -e .
```

## ⚙️ Requirements

The core skills need nothing beyond the agent and the `suki` CLI (Python 3).

`/suki book` also needs `pandoc` and a LaTeX distribution with `xelatex`:

```bash
brew install pandoc
brew install --cask mactex-no-gui   # or any TeX Live install
```

## 🔐 Privacy

Everything stays on your machine. Curriculum, probe history, and the books
you publish: none of it leaves your computer. The only external calls are
the LLM/harness and web fetches.

## 🧭 Philosophy

1. **Brutal honesty first**: Know the truth about your model
2. **The model is in your words**: You restate it; it becomes yours
3. **Learn for keeps**: Spaced repetition over cramming
4. **Everything is an artifact**: Named files, compounded across sessions
5. **Privacy by default**: Your data never leaves your machine
