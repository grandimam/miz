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

Build your own curriculum. Then prove you actually understand it. The single entry point and router for the suki stack: career tools plus a personal learning engine, all under `~/.suki/`.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions
- **Bullets** for lists: `•`

## Commands

### `/suki` (no args)

Show the suki home page. On EVERY invocation, first check if
`~/.suki/profile/identity.json` exists. There are two states: **first run**
(no profile) and **dashboard** (profile exists).

#### State A — first run (no profile)

```
╭──────────────────────────────────────────╮
│                  s u k i                 │
│   Build expertise. Validate it. Own it.  │
╰──────────────────────────────────────────╯

Welcome to suki — your career, reflected honestly.

────────────────────────────────────────────
🚀  Quick start
────────────────────────────────────────────
  → /suki career init         Set up your career profile
  → /suki curriculum <topic>  Start learning any topic

────────────────────────────────────────────
🗺️  Commands
────────────────────────────────────────────

CAREER — land the right role
  /suki career               overview · jobs · prep · tracker
  /suki career init          first-time setup
  /suki career add job       analyze a job posting
  /suki career add resume    add a resume
  /suki career prep <co>     interview prep for a company
  /suki career analyze <co>  honest fit analysis
  /suki career learn <co>    close gaps + mock interviews
  /suki career tracker       applications tracker

RESUME — present yourself
  /suki resume               audit the resume against your profile
  /suki resume improve       rewrite weak bullets
  /suki resume tailor <job>  tailor to a specific job

LEARNING — build durable expertise
  /suki curriculum <topic>   design a learning path
  /suki probe <topic> [ch]   build + verify understanding
  /suki learn <draft>        review material as a learner
  /suki book <topic>         publish a teaching book
```

#### State B — dashboard (profile exists)

```
╭──────────────────────────────────────────╮
│                  s u k i                    │
│   Build expertise. Validate it. Own it.  │
╰──────────────────────────────────────────╯

**{Name}** · {Current Role} at {Company} · {Location}

────────────────────────────────────────────
📊  Status
────────────────────────────────────────────
  Profile   {X} yrs · {Y} skills · {Z} proof points
  Jobs      {N} tracked · {M} with fit analysis
  Prep      {N} companies · {M} sessions
  Learning  {N} topics · {M} due for review

────────────────────────────────────────────
⏳  Due for review
────────────────────────────────────────────
  • python 2.3 — {title}          (due today)
  • system-design 1.1 — {title}   (due in 2d)

────────────────────────────────────────────
🗺️  Commands
────────────────────────────────────────────

CAREER — land the right role
  /suki career               overview · jobs · prep · tracker
  /suki career add job       analyze a job posting
  /suki career prep <co>     interview prep for a company
  /suki career learn <co>    close gaps + mock interviews

RESUME — present yourself
  /suki resume               audit the resume against your profile
  /suki resume improve       rewrite weak bullets
  /suki resume tailor <job>  tailor to a specific job

LEARNING — build durable expertise
  /suki probe <topic> [ch]   continue learning
  /suki curriculum <topic>   design a new path
  /suki learn <draft>        review material as a learner
  /suki book <topic>         publish a teaching book

────────────────────────────────────────────
Next step
  → /suki probe python 1.1   continue where you left off
```

Rules for State B:

- **Status** — pull from `~/.suki/profile/`, `~/.suki/activity/`, and
  `~/.suki/topics/*/mastery.json`. Prefer one-line summaries over separate
  sections.
- **Due for review** — list topics with `next_revisit_at` in the past,
  nearest due first. If nothing is due, drop the block entirely.
- **Commands** — always render the full list from the routing table below.
- **Next step** — the most valuable immediate action: the oldest due chapter,
  the next `in_progress`/`not_started` chapter of the most active topic, or
  `/suki career` if the profile is new. If nothing stands out, drop it.

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
