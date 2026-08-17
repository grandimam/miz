---
name: miz
description: |
  Miz - a stack for building and validating expertise. The /miz command is the
  single entry point and router. Subcommands: /miz career ... (profile,
  job-fit analysis, interview prep, gap closing, tracking), /miz curriculum
  <topic> to design a learning path, /miz learn <draft> to review material,
  /miz probe <topic> to build + verify understanding, /miz book <topic> to
  publish a teaching book, and /miz resume to audit, improve, or tailor the
  resume. All state lives under ~/.miz/. Use /miz with no subcommand for the
  status dashboard.
---

# Miz

> Build expertise. Validate it. Own it.

The single entry point and router for the miz stack: career tools plus a
personal learning engine, all under `~/.miz/`.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions
- **Bullets** for lists: `•`

## Commands

### `/miz` (no args)

Show the miz home page. On EVERY invocation, first check if
`~/.miz/profile/identity.json` exists. There are two states: **first run**
(no profile) and **dashboard** (profile exists).

#### State A — first run (no profile)

```
╭──────────────────────────────────────────╮
│                  m i z                    │
│   Build expertise. Validate it. Own it.  │
╰──────────────────────────────────────────╯

Welcome to miz — your career, reflected honestly.

────────────────────────────────────────────
🚀  Quick start
────────────────────────────────────────────
  → /miz career init         Set up your career profile
  → /miz curriculum <topic>  Start learning any topic

────────────────────────────────────────────
🗺️  Commands
────────────────────────────────────────────

CAREER — land the right role
  /miz career               overview · jobs · prep · tracker
  /miz career init          first-time setup
  /miz career add job       analyze a job posting
  /miz career add resume    add a resume
  /miz career prep <co>     interview prep for a company
  /miz career analyze <co>  honest fit analysis
  /miz career learn <co>    close gaps + mock interviews
  /miz career tracker       applications tracker

RESUME — present yourself
  /miz resume               audit the resume against your profile
  /miz resume improve       rewrite weak bullets
  /miz resume tailor <job>  tailor to a specific job

LEARNING — build durable expertise
  /miz curriculum <topic>   design a learning path
  /miz probe <topic> [ch]   build + verify understanding
  /miz learn <draft>        review material as a learner
  /miz book <topic>         publish a teaching book
```

#### State B — dashboard (profile exists)

```
╭──────────────────────────────────────────╮
│                  m i z                    │
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
  /miz career               overview · jobs · prep · tracker
  /miz career add job       analyze a job posting
  /miz career prep <co>     interview prep for a company
  /miz career learn <co>    close gaps + mock interviews

RESUME — present yourself
  /miz resume               audit the resume against your profile
  /miz resume improve       rewrite weak bullets
  /miz resume tailor <job>  tailor to a specific job

LEARNING — build durable expertise
  /miz probe <topic> [ch]   continue learning
  /miz curriculum <topic>   design a new path
  /miz learn <draft>        review material as a learner
  /miz book <topic>         publish a teaching book

────────────────────────────────────────────
Next step
  → /miz probe python 1.1   continue where you left off
```

Rules for State B:

- **Status** — pull from `~/.miz/profile/`, `~/.miz/activity/`, and
  `~/.miz/topics/*/mastery.json`. Prefer one-line summaries over separate
  sections.
- **Due for review** — list topics with `next_revisit_at` in the past,
  nearest due first. If nothing is due, drop the block entirely.
- **Commands** — always render the full list from the routing table below.
- **Next step** — the most valuable immediate action: the oldest due chapter,
  the next `in_progress`/`not_started` chapter of the most active topic, or
  `/miz career` if the profile is new. If nothing stands out, drop it.

If the profile exists but key status files are missing or empty, show `—`
for those rows rather than a number.

### `/miz status`

Same as `/miz` with no args.

## Subcommand Routing

Parse the first word after `/miz` and route to the matching skill. Each
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
| *(no subcommand)* | miz | Status dashboard |

Routing rules:

- `/miz career ...` → follow the `career` skill for everything after `career`,
  e.g. `/miz career init`, `/miz career add job`, `/miz career prep <company>`.
- `/miz curriculum <topic>` → follow the `curriculum` skill for the topic.
- `/miz learn <draft>` → follow the `learn` skill for the draft.
- `/miz probe <topic> [ch]` → follow the `probe` skill.
- `/miz book <topic>` → follow the `book` skill.
- `/miz resume [improve|tailor <job-id>]` → follow the `resume` skill.
- Unknown or missing subcommand → show the status dashboard above.