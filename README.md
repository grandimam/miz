# Suki

> Build expertise. Validate it. Own it.

```
╭────────────────────────────────────────────╮
│                  s u k i                   │
│   Build expertise. Validate it. Own it.    │
╰────────────────────────────────────────────╯
```

Suki turns an AI coding agent into a learning partner that doesn't trust
you. Not in a moral sense. It refuses to believe you know something just
because you read it, watched a course, or nodded along with a tutorial.

Learning isn't consuming content. It's being forced to say it back, from
your own head, until it holds. Suki makes you do that, then it remembers
what you're weak at and brings it back before it fades.

**🔒 Local-first** · **🛡️ Private by default** · **🧩 3 steps, one command** · **🐍 Python 3 + your agent**

## The loop: curriculum → probe → book

```
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
   ┌──────────┐     ┌──────────┐     ┌──────────┐      │
   │ curriculum│ ──► │  probe   │ ──► │   book   │      │
   │ build the │     │  test it │     │ publish  │──────┘
   │  path     │     │  & fix   │     │   it     │
   └──────────┘     └──────────┘     └──────────┘
```

- **`/suki curriculum <topic>`** — design the definitive learning path: the
  chapters, the order, what "mastered" means for your topic.
- **`/suki probe <topic> [ch]`** — build and verify understanding chapter by
  chapter. Force a restatement, test it, repair the cracks, then schedule
  reviews so it doesn't rot.
- **`/suki book <topic>`** — render your curriculum, working models, and
  probe history into a publication-quality teaching book.

Work compounds: each step writes an artifact to `~/.suki/topics/<slug>/`
that the next step reads. Probe again next week, and the book reflects it.

## 📐 Build a curriculum

```
/suki curriculum active-directory

  → tier 1:  The basics (what AD is, how a domain works)
  → tier 2:  Core mechanics (Kerberos, tickets, trusts)
  → tier 3:  Attacks (Kerberoasting, golden tickets, delegation)
  → tier 4:  Defenses + detection
  → tier 5:  Expert edge (red-team tradecraft, real-world ops)

  + what "mastered" means at every chapter
  + the order that actually builds understanding
```

Suki designs the path from absolute basics to the deepest expert end of the
field, then writes it as chapter-by-chapter markdown plus a
`curriculum.json` that every later step reads.

| Command | What it does |
|---------|--------------|
| `/suki curriculum <topic>` | Design a definitive learning path: chapters, order, mastery checks |
| `/suki learn <draft>` | Review a chapter draft from a serious learner's perspective |

## 🔬 Probe your understanding

```
/suki probe active-directory 1.1

  "Explain Kerberos authentication in your own words."

  → you state your picture
  → suki probes it for cracks
  → weak spot? a targeted drill fixes it right there
  → mastered? revisit in 3 → 10 → 30 → 90 days
```

The model has to be in **your** words, not the book's. If it doesn't hold
up, the gap is exposed and repaired inline. What you're weak at is
remembered and resurfaced before it fades. Nothing is graded against you;
everything is recorded as an artifact that compounds.

| Command | What it does |
|---------|--------------|
| `/suki probe <topic> [ch]` | Build + verify understanding chapter by chapter; repair cracks; spaced repetition |

## 📖 Create a book

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
╭──────────────────────────────────────────╮
│                  s u k i                    │
│   Build expertise. Validate it. Own it.  │
╰──────────────────────────────────────────╯

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
/suki curriculum python    # build the path
/suki probe python 1.1     # build + verify understanding
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

- `suki install [--opencode|--claude|--codex|--all]` — link skills into your agent
- `suki topics` — list topics
- `suki status [topic]` — progress + spaced-repetition due status
- `suki book <topic>` — render a topic as a book

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
