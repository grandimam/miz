# Miz

> Build expertise. Validate it. Own it.

```
╭────────────────────────────────────────────╮
│                  m i z                      │
│   Build expertise. Validate it. Own it.    │
╰────────────────────────────────────────────╯
```

Miz turns an AI coding agent into a learning partner that doesn't trust
you. Not in a moral sense. It refuses to believe you know something just
because you read it, watched a course, or nodded along with a tutorial.

Learning isn't consuming content. It's being forced to say it back, from
your own head, until it holds. Miz makes you do that, then it remembers
what you're weak at and brings it back before it fades. Then it helps you
use all of that to land the right job.

**🔒 Local-first** · **🛡️ Private by default** · **🧩 7 skills, one command** · **🐍 Python 3 + your agent**

---

## See it in action

One command, `/miz`, is the status dashboard and the router to everything
else. It knows where you left off and what's due next.

```
╭──────────────────────────────────────────╮
│                  m i z                    │
│   Build expertise. Validate it. Own it.  │
╰──────────────────────────────────────────╯

**Gaurav** · Security Engineer at Armor Defense Inc. · Pune, MH, India

────────────────────────────────────────────
📊  Status
────────────────────────────────────────────
  Profile   1 role · 30 skills · 10 proof points
  Jobs      4 tracked · 2 with fit analysis
  Prep      2 companies · 5 sessions
  Learning  3 topics · 1 due for review

────────────────────────────────────────────
⏳  Due for review
────────────────────────────────────────────
  • active-directory 2.1 (Kerberos auth)  due today
  • python 3.1 (Asyncio)                  due in 2d

────────────────────────────────────────────
Next step
  → /miz probe active-directory 2.1
────────────────────────────────────────────
```

## Quick start

```bash
pip install miz
miz install --all     # links the skills into opencode, claude, and codex
```

That's it. Restart your agent, then:

```bash
/miz career init      # build your profile (2 min)
/miz curriculum python    # start learning anything
/miz probe python 1.1     # build + verify understanding
```

---

## Two layers that feed each other

```
LEARNING ENGINE (any topic)          CAREER LAYER (job hunting)
─────────────────────────────        ─────────────────────────────
curriculum → learn                   /miz career: init → add → prep → analyze
     ↓        ↓                     → learn → tracker
probe (build + verify)               (fit, gaps, mocks, outcomes)
     ↓
book (publish)
```

Everything you learn feeds your career. Everything you do in your career
feeds what you learn. The same DNA powers both: brutal honesty, Socratic
practice, spaced repetition, and artifacts on disk that compound across
sessions.

---

## 📚 The learning engine

Most learning tooling either evaluates you (quizzes) or dumps content at
you (courses). Miz does the part in between: it helps you *construct* the
picture in your head, layer by layer, then tests whether that picture
actually holds up, drills the cracks it finds, and resurfaces the knowledge
before it fades. You build it. The agent holds the structure.

### How a learning session goes

```
/miz curriculum active-directory   → design the path: the chapters, the
                                     order, what "mastered" means

/miz learn draft.md                → review a chapter you wrote, from a
                                     serious learner's perspective: is the
                                     order right? are the examples real?

/miz probe active-directory 1.1    → force a restatement: explain the
                                     chapter in your own words, test it,
                                     repair the cracks inline
                                     → not mastered? probe again
                                     → mastered? revisit in 3 → 10 → 30 → 90
                                       days so it doesn't quietly rot

/miz book active-directory         → render curriculum + probe history as a
                                     publication-quality teaching book
```

The loop is the same no matter the topic: a language, a framework, a
subfield, a craft. Skills do not exist in isolation; each writes an
artifact to `~/.miz/` that the next one reads, so your work compounds
across sessions.

| Command | What it does |
|---------|--------------|
| `/miz curriculum <topic>` | Design a definitive learning path: chapters, order, mastery checks |
| `/miz learn <draft>` | Review a chapter draft from a learner's perspective |
| `/miz probe <topic> [ch]` | Build + verify understanding chapter by chapter; repair cracks; spaced repetition |
| `/miz book <topic>` | Render the topic as a publication-quality teaching book |

```
/miz curriculum python
/miz probe python 1.2
/miz book python              # -> ~/.miz/topics/python/book/book.pdf
```

---

## 🎯 The career layer

Job hunting is broken: you apply to jobs you're not qualified for, skip
jobs you'd be perfect for, prep with generic questions, forget your own
accomplishments, and cram before interviews. Every career tool tells you
what you want to hear. Miz tells you the truth: about your fit, your gaps,
and your resume.

### How a job hunt goes

```
/miz career init                 → set up your profile, add your resume,
                                   merge it into a master profile

/miz career add resume           → parse a resume, merge into profile
/miz career add job <url>        → parse the JD, research the company,
                                   derive your positioning for it
/miz career analyze crowdstrike  → honest fit score: requirements × your
                                   evidence, deal-breakers called out

/miz career prep crowdstrike     → company-modeled interview prep: how they
                                   actually ask, mapped to their values
/miz career learn crowdstrike    → close gaps (Socratic) + checkpoint and
                                   full mocks. Exposed in a mock? The gap
                                   reopens. Fix → mock again → ready.

/miz resume                      → audit your resume against your profile
/miz resume improve              → rewrite weak bullets with your real metrics
/miz resume tailor <job>         → tailor the resume to a specific job

/miz career tracker              → track applications + outcomes
```

The learn phase is a continuous loop:

```
Work on gap → Checkpoint → Exposed? → Work on gap → ...
                              ↓
                         Full mock
                              ↓
                     ✓ Ready for interview
```

### Brutal honesty first

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

### Practice the way that company asks

When you add a job, Miz researches the company (careers page, engineering
blog, Glassdoor) and builds an intel file. Then it asks you questions *the
way they would ask them*, mapped to their actual values and process.

### Answers from YOUR experience

You blank on behavioral questions because you forget your own
accomplishments. Miz doesn't. When you say "help," it searches your profile
and suggests an answer from your actual experience: your stories, your
numbers, their framing.

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

---

## 🧠 The seven skills

| Skill | Layer | Role |
|-------|-------|------|
| `miz` | umbrella | Status dashboard + router (single entry point) |
| `career` | career | Profile, job-fit, prep, gap closing, tracking |
| `resume` | career | Audit, improve, and tailor the resume |
| `curriculum` | learning | Design a definitive learning path |
| `learn` | learning | Review material from a learner's perspective |
| `probe` | learning | Build + verify understanding, repair cracks, spaced repetition |
| `book` | learning | Render a topic as a teaching book |

---

## 🗂️ State

Everything lives under `~/.miz/`, one folder per topic plus the career
folders. Current state is JSON; history is append-only JSONL. Nothing is
ever deleted, so the full arc of your learning and job hunting is
recoverable.

```
~/.miz/
├── topics/<slug>/        # learning (curriculum.json, mastery.json, probes, book/)
├── profile/              # career (identity, experience, skills, proof-points)
├── sources/              # raw resumes + work samples
├── activity/             # jobs/ + tracker.md
├── prep/<company>/       # intel, analysis, stories, sessions
├── interview/            # question banks + session history
└── learning/             # per-skill progress + question banks
```

The `miz` CLI manages the stack:

- `miz install [--opencode|--claude|--codex|--all]` — link skills into your agent
- `miz topics` — list topics
- `miz status [topic]` — progress + spaced-repetition due status
- `miz book <topic>` — render a topic as a book

---

## 📦 Install

```bash
pip install miz
miz install --all
```

That's the whole setup. `pip install miz` gives you the `miz` command;
`miz install` links all seven skills (`miz`, `career`, `curriculum`,
`learn`, `probe`, `book`, `resume`) into your agent. Default to `--all`, or
pick just your agent with `--opencode`, `--claude`, or `--codex`.

Restart your agent after installing, then use `/miz` as the single entry
point. It routes subcommands: `/miz career ...`, `/miz curriculum <topic>`,
`/miz learn <draft>`, `/miz probe <topic> [ch]`, `/miz book <topic>`,
`/miz resume [improve|tailor <job>]`, or `/miz` alone for the status
dashboard.

**From source (contributing):**

```bash
git clone <this repo> && cd miz
pip install -e .
```

## ⚙️ Requirements

The core skills need nothing beyond the agent and the `miz` CLI (Python 3).

`/book` also needs `pandoc` and a LaTeX distribution with `xelatex`:

```bash
brew install pandoc
brew install --cask mactex-no-gui   # or any TeX Live install
```

## 🔐 Privacy

Everything stays on your machine. Resumes, profile, job postings, interview
practice, curriculum, probe history: none of it leaves your computer. The
only external calls are the LLM/harness and web fetches (to read job
postings and research companies).

## 🧭 Philosophy

1. **Brutal honesty first**: Know the truth about your fit and your model
2. **The model is in your words**: You restate it; it becomes yours
3. **Your voice, not AI's**: Answers come from your real experience
4. **Company-modeled prep**: Practice the way that company actually asks
5. **Learn for keeps**: Spaced repetition over cramming
6. **Everything is an artifact**: Named files, compounded across sessions
7. **Privacy by default**: Your data never leaves your machine

---

**Miz: Build expertise. Validate it. Own it.**