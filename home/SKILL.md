---
name: suki
description: |
  Suki - a stack for building and validating your expertise. The /suki command is a
  single entry point. Subcommands: /suki curriculum <topic> to design a learning path, 
  /suki learn <draft> to review material, /suki probe <topic> to build + verify understanding, 
  /suki book <topic> to publish a teaching book, and /suki resume to audit, improve, or 
  tailor the resume. All state lives under ~/.suki/. Use /suki with no subcommand for the
  status dashboard.
---

# Suki

Build your curriculum. Then prove you actually understand it, progressively.
The single entry point and router for the suki stack: career tools plus a
personal learning engine, all under `~/.suki/`.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions, `🔥` streak
- **Bullets** for lists: `•`

## Focus preference

Read `~/.suki/profile/prefs.json` (written by `suki focus`). The `focus` value
is `all` (default), `learning`, or `career`. It decides which command blocks
the dashboard leads with:

- `learning` → lead with LEARNING, then PROFILE; collapse CAREER into one hint line.
- `career` → lead with CAREER + RESUME; collapse LEARNING into one hint line.
- `all` → show both blocks as below.

Never print the focused-out block in full; one hint line is enough. If the
file is missing, treat it as `all`.

## Commands

### `/suki` (no args)

Show the suki home page. On EVERY invocation, first check if
`~/.suki/profile/identity.json` exists. There are two states: **first run**
(no profile) and **dashboard** (profile exists).

#### State A — first run (no profile)

Lead with what suki is and what your data promise is. Sell the loop, not the
feature list. Keep the command list short.

```
╭───────────────────────────────────────────────╮
│                    s u k i                    │
│          Build it. Prove it. Retain it.       │
╰───────────────────────────────────────────────╯

Hi. Suki is a learning partner that doesn't trust you — not
in a moral sense. It refuses to believe you know something
just because you read it.

It makes you build the curriculum for any topic, then probes
you on it chapter by chapter: you say it back in your own
words, it pokes at the cracks, repairs the weak spots, and
reschedules the chapters before they fade.

🔒 Everything stays on this machine.
   Curricula, probes, books, career data: none of it ever
   leaves your computer.

──────────────────────────────────────────────────
🚀  Try it in 60 seconds
──────────────────────────────────────────────────
  → /suki curriculum <topic>   build a definitive learning path
  → /suki probe <topic> 1.1    say it back, get probed, repair
  → suki demo                  seed a sample topic and feel the loop
  → /suki career init          set up your career profile (optional)

──────────────────────────────────────────────────
🗺️  Everything else
──────────────────────────────────────────────────
  /suki curriculum  design a path      /suki book  publish a book
  /suki probe       verify a chapter   /suki resume  audit your resume
  /suki learn       review a draft     /suki career  jobs · prep · tracker
```

Read the focus preference. If it is `career`, swap the two blocks and lead
with `/suki career init`. If `learning`, keep as above. If the user hasn't
told you a focus, still offer `/suki career init` as one optional line (as
shown) so career users don't miss it.

If the user doesn't know what topic to pick, suggest `suki demo` so they feel
the probe loop before committing to a real topic.

#### State B — dashboard (profile exists)

Lead with the **next step**, then status, then due reviews. Commands collapse
by focus preference; never render a wall of every subcommand.

```
╭───────────────────────────────────────────────╮
│                    s u k i                    │
│          Build it. Prove it. Retain it.       │
╰───────────────────────────────────────────────╯

**{Name}** · {Current Role} at {Company} · {Location}

──────────────────────────────────────────────────
🎯  Next step
──────────────────────────────────────────────────
  → /suki probe python 1.1   continue where you left off

──────────────────────────────────────────────────
📊  Status
──────────────────────────────────────────────────
  🔥 4-day learning streak
  Learning   3 topics · 1 due for review
  Profile    {X} yrs · {Y} skills · {Z} proof points
  Jobs       {N} tracked · {M} with fit analysis

──────────────────────────────────────────────────
⏳  Due for review
──────────────────────────────────────────────────
  • python 2.3 — {title}          (due today)
  • system-design 1.1 — {title}   (due in 2d)

──────────────────────────────────────────────────
🗺️  Commands
──────────────────────────────────────────────────
LEARNING — build durable expertise
  /suki probe <topic> [ch]   continue learning
  /suki curriculum <topic>   design a new path
  /suki book <topic>         publish a teaching book
  /suki map <topic>          see the whole guide as a tree

CAREER — land the right role   (/suki career for all)
  /suki resume               audit the resume against your profile
```

Rules for State B:

- **Next step** — the most valuable immediate action, always first: the
  oldest due chapter, the next `in_progress`/`not_started` chapter of the
  most active topic, or `/suki career init` if the profile is new. If nothing
  stands out, drop the block entirely.
- **Status** — pull from `~/.suki/`, `~/.suki/profile/`, and
  `~/.suki/topics/*/mastery.json`. Prefer one-line summaries. Add the
  `🔥 N-day learning streak` line when `suki status` reports one (it counts
  consecutive days with a probe session across all topics).
- **Due for review** — list topics with `next_revisit_at` in the past,
  nearest due first. If nothing is due, drop the block entirely.
- **Commands** — collapse by focus:
  - `all` → show both blocks, but the non-focus block is 1-3 lines max (a
    hint + `/suki <block>` to expand). The sample above shows LEARNING full
    and CAREER collapsed; swap when focus is `career`.
  - `learning` → only LEARNING + one career hint line.
  - `career` → only CAREER/RESUME + one learning hint line.
- Never dump more than ~10 command lines. The routing table below is the
  full list; the dashboard is the highlight reel.

If the profile exists but key status files are missing or empty, show `—`
for those rows rather than a number.

### `/suki status`

Same as `/suki` with no args.

## Subcommand Routing

Parse the first word after `/suki` and route to the matching skill. Each
subcommand's instructions live in the corresponding skill; follow that skill
for the remainder.

| Subcommand | Skill to follow | What it does |
|------------|-----------------|--------------|
| `career ...` | career | Profile, job fit, prep, gap closing, tracking |
| `curriculum <topic>` | curriculum | Design a definitive learning path |
| `learn <draft>` | learn | Review material from a learner's perspective |
| `probe <topic> [ch]` | probe | Build + verify understanding, spaced repetition |
| `book <topic>` | book | Render a topic as a teaching book |
| `resume [improve\|tailor <job>]` | resume | Audit, improve, or tailor the resume |
| *(no subcommand)* | suki | Status dashboard |

Routing rules:

- `/suki career ...` → follow the `career` skill for everything after `career`,
  e.g. `/suki career init`, `/suki career add job`, `/suki career prep <company>`.
- `/suki curriculum <topic>` → follow the `curriculum` skill for the topic.
- `/suki learn <draft>` → follow the `learn` skill for the draft.
- `/suki probe <topic> [ch]` → follow the `probe` skill.
- `/suki book <topic>` → follow the `book` skill.
- `/suki resume [improve|tailor <job-id>]` → follow the `resume` skill.
- Unknown or missing subcommand → show the status dashboard above.

CLI extras (tell the user about them when relevant; they do not need a skill):

- `suki demo` — seed a sample topic so a new user feels the probe loop.
- `suki map <topic>` — render the whole guide as a status tree.
- `suki export` / `suki import` — back up or restore `~/.suki`.
- `suki focus [learning|career|all]` — set the dashboard's focus.
- `suki status --due` — just the chapters due for review.
