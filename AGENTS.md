# Miz

> Build expertise. Validate it. Own it.

Miz is two layers that feed each other:

```
LEARNING ENGINE (any topic)          CAREER LAYER (job hunting)
─────────────────────────────        ─────────────────────────────
curriculum → learn                   /miz career: init → add → prep → analyze
     ↓        ↓                     → learn → tracker
probe (build + verify)               (fit, gaps, mocks, outcomes)
     ↓
book (publish)
```

- **Learning engine** = build durable, owned expertise in any topic:
  `curriculum` designs the path, `learn` reviews material so it teaches,
  `probe` builds and verifies understanding (Socratic, spaced repetition),
  `book` renders it into a teaching volume. State: `~/.miz/topics/<slug>/`.
- **Career layer** = apply that expertise to the job market:
  `career` handles profile, honest fit analysis, company-modeled interview
  prep, gap closing, mock validation, application tracking. State: `~/.miz/`.
- **Umbrella** = `miz` is the status dashboard and router for the stack.

Both layers share the same DNA: brutal honesty, Socratic practice, spaced
repetition, artifacts on disk that compound across sessions.

## Structure

```
miz/                            # this repo
├── home/                       # the /miz skill (umbrella dashboard + router; installs as `miz`)
│   └── SKILL.md
├── career/                     # the career skill (routed via /miz career)
│   ├── SKILL.md
│   └── agents/                 # setup, add, prep, analyze, learn, tracker
├── curriculum/                 # learning skill (designs a learning path)
│   └── SKILL.md
├── learn/                      # learning skill (reviews material)
│   └── SKILL.md
├── probe/                      # learning skill (builds + verifies understanding)
│   └── SKILL.md
├── book/                       # learning skill (renders a teaching book)
│   ├── SKILL.md
│   └── template.latex
├── resume/                     # career skill (audits, improves, tailors the resume)
│   └── SKILL.md
├── bin/                        # CLI helpers (miz-status, miz-topics, miz-book)
├── test/                       # test harness for skills + bin
├── .codex/                     # Codex hooks
├── AGENTS.md
├── README.md
└── setup                       # installs skills into OpenCode/Claude/Codex
```

All runtime state lives under `~/.miz/`:

```
~/.miz/
├── topics/<slug>/              # LEARNING: one folder per topic
│   ├── curriculum.json         #   the path (source of truth)
│   ├── README.md               #   the path, human-readable
│   ├── mastery.json            #   per-chapter status + revisit metadata
│   ├── models.json             #   per-chapter working model (written by probe)
│   ├── models.jsonl            #   model-history snapshots
│   ├── probes.jsonl            #   probe session history
│   ├── practice.jsonl          #   remediation drills (written by probe)
│   └── book/                   #   rendered book.pdf + book.tex
├── profile/                    # CAREER: master profile
│   ├── identity.json
│   ├── experience.json
│   ├── education.json
│   ├── skills.json
│   └── proof-points.json
├── sources/                    # raw inputs (resumes, work samples)
├── activity/                   # jobs + tracker
│   ├── tracker.md
│   └── jobs/*.json
├── prep/<company-slug>/        # intel, analysis, stories, sessions
├── interview/                  # question banks + session history
├── learning/                   # per-skill progress + question banks
└── bin/                        # linked CLI helpers
```

## Skills

| Skill | Layer | Role | Command |
|-------|-------|------|---------|
| `miz` | umbrella | Status dashboard + router (single entry point) | `/miz` |
| `career` | career | Profile, job-fit, prep, gap closing, tracking | `/miz career ...` |
| `curriculum` | learning | Design a definitive learning path | `/miz curriculum <topic>` |
| `learn` | learning | Review material from a learner's view | `/miz learn <draft>` |
| `probe` | learning | Build + verify understanding, repair cracks, spaced repetition | `/miz probe <topic> [ch]` |
| `book` | learning | Render a topic as a teaching book | `/miz book <topic>` |
| `resume` | career | Audit, improve, and tailor the resume against the profile | `/miz resume [improve\|tailor <job>]` |

## Commands

`/miz` is the single entry point and router.

### Umbrella

| Command | Description |
|---------|-------------|
| `/miz` | Status dashboard + router |
| `/miz status` | Same as `/miz` |

### Career layer (via `/miz career ...`)

| Command | Description |
|---------|-------------|
| `/miz career` | Career overview |
| `/miz career init` | First-time setup |
| `/miz career add resume` | Add resume (merges into profile) |
| `/miz career add job` | Add job posting, derive positioning |
| `/miz career add brag` | Capture an achievement |
| `/miz career add doc` | Add work sample (tech spec, RFC, etc.) |
| `/miz career prep <company>` | Collect company intel |
| `/miz career analyze <company>` | Fit + gaps + positioning |
| `/miz career learn <company>` | Close gaps, run mocks |
| `/miz career tracker` | View/update applications |

### Resume (via `/miz resume ...`)

| Command | Description |
|---------|-------------|
| `/miz resume` | Audit the resume against the profile |
| `/miz resume improve` | Rewrite weak bullets with metrics + keywords |
| `/miz resume tailor <job>` | Tailor the resume to a specific job |

### Learning engine (via `/miz curriculum/learn/probe/book`)

| Command | Description |
|---------|-------------|
| `/miz curriculum <topic>` | Design the path (curriculum.json + mastery.json) |
| `/miz learn <draft>` | Critique material from a learner's perspective |
| `/miz probe <topic> [ch]` | Build + verify understanding chapter by chapter |
| `/miz book <topic>` | Render the topic as a publication-quality book |

`/miz career learn <company>` is skill practice for interviews;
`/miz probe <topic>` is mastery building for any topic. They
share the Socratic + spaced-repetition approach but different state.

## Workflow

### Learning engine (any topic)

```
/miz curriculum python        → design the path (chapters, mastery checks)
/miz learn draft              → review chapters from the learner's view
/miz probe python 1.1         → force a restatement, test it, repair cracks
                                → mastered? sets revisit metadata (3/10/30/90/180d)
/miz book python              → render curriculum + probe history as a book
```

The loop: `curriculum → probe → mastered? → revisit later`. Weak chapters come
back through spaced repetition; the model is always the learner's own words.

### Career layer (job hunting)

```
/miz career init              → create ~/.miz/ + profile
/miz career add resume        → parse resume, merge into profile
/miz career add job           → parse JD, derive positioning
/miz career prep <company>    → research company (values, process, questions)
/miz career analyze <company> → fit score + deal-breakers + gaps + positioning
/miz career learn <company>   → close gaps (Socratic) + checkpoint/full mocks
/miz career tracker           → track applications + outcomes
/miz resume                   → audit resume vs profile
/miz resume improve           → rewrite weak bullets
/miz resume tailor <job>      → tailor to a specific job
```

The learn phase is a continuous loop:

```
Work on gap → Checkpoint → Exposed? → Work on gap → ...
                              ↓
                         Full mock
                              ↓
                     ✓ Ready for interview
```

## Bin helpers

| Helper | Purpose |
|--------|---------|
| `miz-topics` | List topics under `~/.miz/topics/` |
| `miz-status` | Progress + spaced-repetition due status |
| `miz-book` | Assemble a topic into `book.pdf` via pandoc + LaTeX |

## Conventions

- **JSON** for all structured data, **Markdown** for narratives and artifacts
- Current state is JSON; history is append-only JSONL. Nothing is deleted.
- File names: `kebab-case.json`
- Job IDs: `{company}-{slug}`; company slugs: `kebab-case`
- Dates: `YYYY-MM-DD` or `YYYY-MM`
- Learning topics: one folder per slug under `~/.miz/topics/`

## Principles

1. **Brutal honesty first** — Know the truth about fit and about your model
2. **The model is in your words** — `probe` forces you to restate it
3. **Accumulate, don't overwrite** — artifacts merge, never clobber
4. **Company-modeled prep** — Practice the way that company actually asks
5. **Socratic learning** — You do the thinking, the tool guides
6. **Continuous loop** — Probe/mock → expose → fix → again until ready
7. **Gaps can reopen** — Weakness exposed later reopens the gap
8. **Memory is an artifact** — revisit metadata + JSONL history make progress durable
9. **Transparent sources** — Every career data point has a reference
10. **Privacy by default** — Everything stays local under `~/.miz/`