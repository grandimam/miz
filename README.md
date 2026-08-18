# Suki

**Build it. Prove it. Retain it.**

```
╭───────────────────────────────────────────────╮
│                    s u k i                    │
│          Build it. Prove it. Retain it.       │
╰───────────────────────────────────────────────╯
```

Suki turns an AI coding agent into a learning partner that doesn't trust
you. Not in a moral sense. It refuses to believe you know something just
because you read it, watched a course, or nodded along with a tutorial.

The loop is three moves, and each one compounds on the last.

## BUILD → PROVE → RETAIN

```
/suki curriculum <topic>      /suki probe <topic> [ch]       3 → 10 → 30 → 90 days
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│      BUILD       │        │      PROVE       │        │      RETAIN      │
│  design the      │        │  say it back     │        │  revisit before  │
│  definitive      │ ──────►│  probe the       │ ──────►│  it fades; weak  │
│  guide           │        │  cracks, repair  │        │  spots resurface │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

- **BUILD** — `/suki curriculum <topic>` designs the definitive learning path:
  the parts, the chapters, the order, what "mastered" means at every chapter.
  The agent authors it like a field expert writing a real guide, then writes
  it as chapter-by-chapter markdown plus a `curriculum.json` every later step
  reads.
- **PROVE** — `/suki probe <topic> [ch]` forces you to restate each chapter in
  *your* words, not the book's. The agent probes it one question at a time,
  scores it honestly (SOLID / SHALLOW / WRONG), and repairs weak spots inline
  with targeted mini-drills. It never writes the answer for you.
- **RETAIN** — mastered chapters come back at 3 → 10 → 30 → 90 days. Weak
  spots are remembered and resurfaced before they fade. Every pass writes an
  artifact to `~/.suki/topics/<slug>/` that the next pass reads, so the loop
  keeps going and nothing you learned rots.

That's the whole product. Everything else is garnish.

## Quick start

```bash
pip install suki
suki install --all     # links the skills into opencode, claude, and codex
```

Restart your agent, then:

```bash
suki demo                  # optional: feel the loop on a sample topic first
/suki curriculum python    # BUILD: the definitive guide
/suki probe python 1.1     # PROVE: say it back, get probed, repair
/suki probe python 1.1     # again when it's due: the loop, forever
```

## The skills

| Skill | Role |
|-------|------|
| `suki` | Status dashboard + router (single entry point) |
| `curriculum` | BUILD — design a definitive learning path |
| `learn` | Review material from a learner's perspective (runs inside curriculum) |
| `probe` | PROVE — build + verify understanding, repair cracks, spaced repetition |
| `book` | Bonus — render a topic as a teaching book |

## State

Everything lives under `~/.suki/`, one folder per topic. Current state is
JSON; history is append-only JSONL. Nothing is ever deleted, so the full arc
of your learning is recoverable.

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

## Install

```bash
pip install suki
suki install --all
```

That's the whole setup. `pip install suki` gives you the `suki` command;
`suki install` links all five skills into your agent. Default to `--all`,
or pick just your agent with `--opencode`, `--claude`, or `--codex`.

Restart your agent after installing, then use `/suki` as the single entry
point: `/suki` alone shows the status dashboard, `/suki <subcommand>` routes
to the rest.

**From source (contributing):**

```bash
git clone <this repo> && cd suki
pip install -e .
```

## Requirements

The core skills need nothing beyond the agent and the `suki` CLI (Python 3).

`suki book` also needs `pandoc` and a LaTeX distribution with `xelatex`:

```bash
brew install pandoc
brew install --cask mactex-no-gui   # or any TeX Live install
```

## Privacy

Everything stays on your machine. Curriculum, probe history, and the books
you publish: none of it leaves your computer. The only external calls are
the LLM/harness and web fetches.

## Philosophy

1. **Brutal honesty first**: Know the truth about your model
2. **The model is in your words**: You restate it; it becomes yours
3. **Learn for keeps**: Spaced repetition over cramming
4. **Everything is an artifact**: Named files, compounded across sessions
5. **Privacy by default**: Your data never leaves your machine