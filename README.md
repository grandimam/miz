# Miz

> Build expertise. Validate it. Own it.

Miz is two layers that feed each other. The **learning engine** turns an AI
coding agent into a learning partner that takes you from shaky first intuition
to durable, owned mastery of any topic. The **career layer** applies that
expertise to the job market — honest fit analysis, company-modeled interview
prep, gap closing, and tracking.

All local. All private. All yours.

```
LEARNING ENGINE (any topic)          CAREER LAYER (job hunting)
─────────────────────────────        ─────────────────────────────
curriculum → learn                   /miz career: init → add → prep → analyze
     ↓        ↓                     → learn → tracker
probe (build + verify)               (fit, gaps, mocks, outcomes)
     ↓
book (publish)
```

`/miz` is the single command: it routes subcommands to the other skills.

---

## The learning engine

Most learning tooling evaluates you (quizzes) or dumps content at you
(courses). Miz does the part in between: it helps you *construct* the picture
in your head, layer by layer, then tests whether that picture actually holds
up, drills the cracks it finds, and resurfaces the knowledge before it fades.
You build it. The agent holds the structure.

```
curriculum   design the path: definitive guide architecture, book parts, chapters
   |  (writes README.md + curriculum.json + mastery.json)
   v
learn        review chapter drafts from the learner's perspective
   |
   v
probe        surface your picture, test it, repair cracks inline
   |  (writes probes.jsonl; updates mastery.json with revisit metadata)
   |  if not mastered -> probe again on the same chapter
   v
book         render the topic as a publication-quality teaching book
```

The loop is the same no matter the topic: a language, a framework, a subfield,
a craft. Skills do not exist in isolation — each writes an artifact to
`~/.miz/` that the next one reads, so the work compounds across sessions.

### Learning commands

| Command | Role | Reads | Writes |
|---------|------|-------|--------|
| `/miz curriculum <topic>` | Designer | nothing (the seed) | `README.md`, `curriculum.json`, `mastery.json` |
| `/miz learn <draft>` | Learner-side reviewer | draft chapter, sequence context | usually no durable artifact by default |
| `/miz probe <topic> [ch]` | Examiner-coach | `curriculum.json`, `mastery.json`, prior `models.json`, recent `probes.jsonl` | `probes.jsonl`, `mastery.json`, optional `models.json`, `models.jsonl`, `practice.jsonl` |
| `/miz book <topic>` | Publisher | `curriculum.json`, `mastery.json`, `models.json`, `*.jsonl` | `book/book.pdf`, `book/book.tex` |

`/miz probe` forces you to state your picture, tests it, and runs tight repairs
inline before deciding whether the chapter is mastered. Mastered chapters get
spaced-repetition revisit metadata (3 → 10 → 30 → 90 days) so knowledge
doesn't quietly rot.

```
/miz curriculum python
/miz probe python 1.2
/miz book python
```

### Make a book

Once a topic has accumulated work, `/book` renders it as a
publication-quality LaTeX teaching book (KOMA `scrbook` via XeLaTeX with
microtype, real TOC, auto-detected fonts). It's built from the curriculum plus
the refinements found during probing — pitfalls, weak distinctions, and drills
worth teaching explicitly. A study guide, not a session transcript.

```
/miz book python              # -> ~/.miz/topics/python/book/book.pdf
/miz book python --paper a4   # a5 (book size, default), a4, or letter
/miz book python --tex-only   # stop at book.tex to hand-tune the LaTeX
```

---

## The career layer

Job hunting is broken: you apply to jobs you're not qualified for, skip jobs
you'd be perfect for, prep with generic questions, forget your own
accomplishments, and cram before interviews. Every career tool tells you what
you want to hear. Miz tells you the truth.

### 1. Brutal honesty first

```
Fit Score: 65%

| Requirement        | Met? | Evidence                        |
|--------------------|------|---------------------------------|
| 8+ years backend   | ✓    | 10 years across 3 companies     |
| Banking domain     | ✗    | No banking experience           |
| Kafka at scale     | ✓    | 1B+ events/day in previous role |
| Team leadership    | ◐    | Led 3 engineers, not 10+        |

🚨 Deal-Breaker: Banking domain is marked MANDATORY. You don't have it.

Verdict: Strong technical fit, but don't apply unless you can bridge
the banking gap.
```

### 2. Practice the way that company asks

When you add a job, Miz researches the company — careers page, engineering
blog, Glassdoor — and builds an intel file. Then it asks you questions *the
way they would ask them*, mapped to their actual values and process.

### 3. Answers from YOUR experience

You blank on behavioral questions because you forget your own
accomplishments. Miz doesn't. When you say "help," it searches your profile
and suggests an answer from your actual experience — your stories, your
numbers, their framing.

### 4. Skills that actually stick

Spaced repetition (SM-2). Weak topics come back. Mastered topics fade away.
No more cramming, forget, repeat.

### Career commands

| Command | What it does |
|---------|--------------|
| `/miz` | Status dashboard + router |
| `/miz career` | Career overview |
| `/miz career init` | First-time setup |
| `/miz career add job` | Analyze a job posting (honest) |
| `/miz career add resume` | Add another resume |
| `/miz career add brag` | Capture an achievement |
| `/miz career prep <company>` | Research company + interview prep menu |
| `/miz career analyze <company>` | Fit score + gaps + positioning |
| `/miz career learn <company>` | Close gaps + mock interviews (continuous loop) |
| `/miz career tracker` | View/update applications |
| `/miz resume` | Audit the resume against the profile |
| `/miz resume improve` | Rewrite weak bullets with metrics + keywords |
| `/miz resume tailor <job>` | Tailor the resume to a specific job |

The learn phase is a continuous loop: work on gaps → checkpoint mock →
exposed? → fix → full mock → ready. If a mock exposes a weakness, the gap
reopens.

---

## State

Everything lives under `~/.miz/`, one folder per topic plus the career
folders. Current state is JSON; history is append-only JSONL. Nothing is ever
deleted, so the full arc of your learning and job hunting is recoverable.

```
~/.miz/
├── topics/<slug>/        # learning (curriculum.json, mastery.json, probes, book/)
├── profile/              # career (identity, experience, skills, proof-points)
├── sources/              # raw resumes + work samples
├── activity/             # jobs/ + tracker.md
├── prep/<company>/       # intel, analysis, stories, sessions
├── interview/            # question banks + session history
├── learning/             # per-skill progress + question banks
└── bin/                  # CLI helpers
```

CLI helpers (linked into `~/.miz/bin/`):

- `miz-topics` — list topics
- `miz-status` — progress + spaced-repetition due status
- `miz-book` — render a topic as a book

## Install

```bash
./setup            # auto-link into Codex/Claude/OpenCode if their skill dirs exist
./setup --codex    # force-install into ~/.codex/skills
./setup --opencode # install into ~/.config/opencode/skills + the /miz command
./setup --all      # install into all detected skill dirs
./setup --wire     # append a miz section to this repo's AGENTS.md
```

Installs seven skills: `miz` (the router), `career`, `curriculum`, `learn`,
`probe`, `book`, `resume`. State lives in `~/.miz/`.

Use `/miz` as the single entry point. It routes subcommands:
`/miz career ...`, `/miz curriculum <topic>`, `/miz learn <draft>`,
`/miz probe <topic> [ch]`, `/miz book <topic>`, `/miz resume [improve|tailor
<job>]`, or `/miz` alone for the status dashboard.

For OpenCode: restart opencode after running setup so it picks up the skills
and the `/miz` command.

## Requirements

The core skills need nothing beyond the agent and Python 3 (for the bin
helpers).

`/book` also needs `pandoc` and a LaTeX distribution with `xelatex`:

```bash
brew install pandoc
brew install --cask mactex-no-gui   # or any TeX Live install
```

## Privacy

Everything stays on your machine. Resumes, profile, job postings, interview
practice, curriculum, probe history — none of it leaves your computer. The
only external calls are the LLM/harness and web fetches (to read job postings
and research companies).

## Philosophy

1. **Brutal honesty first** — Know the truth about your fit and your model
2. **The model is in your words** — You restate it; it becomes yours
3. **Your voice, not AI's** — Answers come from your real experience
4. **Company-modeled prep** — Practice the way that company actually asks
5. **Learn for keeps** — Spaced repetition over cramming
6. **Everything is an artifact** — Named files, compounded across sessions
7. **Privacy by default** — Your data never leaves your machine

---

**Miz: Build expertise. Validate it. Own it.**