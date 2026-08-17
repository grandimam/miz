---
name: career
description: |
  The career layer of miz: profile building, honest job-fit analysis,
  company-modeled interview prep, gap closing, and application tracking.
  All state lives under ~/.miz/. Use /miz career init to set up, /miz career add
  <type> to add data, /miz career prep <company> for intel, /miz career analyze
  <company> for fit, /miz career learn <company> to close gaps, and /miz career
  tracker to track applications.
---

# Career

Your career, reflected honestly.

This skill is the career layer of the miz stack: profile, honest fit analysis,
company-modeled interview prep, gap closing, and tracking. All state lives
under `~/.miz/`.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions
- **Bullets** for lists: `•`

## Commands

### `/miz career` (no args)

Show a brief career overview: profile stats, job pipeline, prep companies,
tracker summary. Point to next actions.

### `/miz career init`

First-time setup. Creates `~/.miz/` directories, initializes profile files,
guides user through adding resume.

Read `agents/setup.md` and follow its instructions.

### `/miz career status`

Show a brief career overview (same as `/miz career` with no args).

---

### Add Commands

All `/miz career add` commands process immediately.

#### `/miz career add resume`

Add a resume and merge into profile.

Read `agents/add.md` and follow its instructions.

#### `/miz career add job [url]`

Add a job description, analyze fit, derive positioning, research company.

- If URL provided → fetch and analyze automatically
- If no URL → prompt for URL or paste JD text

Read `agents/add.md` and follow its instructions.

#### `/miz career add brag`

Capture a professional achievement.

Read `agents/add.md` and follow its instructions.

#### `/miz career add doc`

Add a tech spec, RFC, design doc, or work sample.

Read `agents/add.md` and follow its instructions.

---

### Tracker Commands

#### `/miz career tracker`

View and update the applications tracker.

Read `agents/tracker.md` and follow its instructions.

**Subcommands:**
- `/miz career tracker` — Show tracker table
- `/miz career tracker update <job-id> --status <status>` — Update job status
- `/miz career tracker update <job-id> --stage <stage>` — Update interview stage
- `/miz career tracker update <job-id> --outcome <outcome>` — Update stage outcome
- `/miz career tracker note <job-id> <note>` — Update notes

**Statuses:** `saved`, `applied`, `interviewing`, `offered`, `accepted`, `rejected`, `withdrawn`

**Stages:** `phone`, `coding`, `system-design`, `behavioral`, `hiring-manager`, `final`

**Outcomes:** `pending`, `passed`, `failed`

---

### Interview Prep Commands

#### `/miz career prep <company>`

Start interview prep for a company. Shows menu to pick interview type.

Read `agents/prep.md` and follow its instructions.

If no company provided, list available companies:
```
───────────────────────────────────────
🎤 **Interview Prep**

Available companies (from jobs in pipeline):

| Company | Jobs | Intel |
|---------|------|-------|
| stripe | 2 | ✓ |
| careem | 1 | ✓ |
| talabat | 1 | ⏳ |

Which company? Enter the name:
```

#### `/miz career prep <company> behavioral`

Behavioral interview practice.

Read `agents/learn.md` and follow its instructions.

Features:
- Questions aligned with company values
- Answers suggested from YOUR proof points
- STAR format coaching
- Feedback from company's perspective

#### `/miz career prep <company> coding`

Coding interview practice.

Read `agents/learn.md` and follow its instructions.

Features:
- Questions from company's known patterns
- Fallback to general question bank
- Hints and walkthroughs
- Complexity analysis

#### `/miz career prep <company> system-design`

System design interview practice.

Read `agents/learn.md` and follow its instructions.

Features:
- Problems relevant to company domain
- Discussion-based format
- Trade-off analysis
- Company-specific considerations

---

### Learning Commands

#### `/miz career learn`

Show skills dashboard with progress across all skills.

Read `agents/learn.md` and follow its instructions.

```
───────────────────────────────────────
📚 **Skills Dashboard**

| Skill | Level | Progress | Due |
|-------|-------|----------|-----|
| python | proficient | 65% | 2 topics |
| system-design | familiar | 40% | 1 topic |
| databases | familiar | — | untested |

**Today's review:**
• python/concurrency (due)
• system-design/components (due)

───────────────────────────────────────
```

#### `/miz career learn <skill>`

Practice a specific skill.

Read `agents/learn.md` and follow its instructions.

Features:
- Evaluate by topic and subtopic
- Track correct/incorrect answers
- Spaced repetition scheduling
- Identify and drill weak areas

#### `/miz career learn <skill> --topic <topic>`

Focus on a specific topic within a skill.

Example: `/miz career learn python --topic concurrency`

#### `/miz career learn <skill> --review`

Review topics due for spaced repetition.

Prioritizes:
1. Overdue topics
2. Low confidence topics
3. Low score topics

#### `/miz career learn <skill> --assess`

Run a full assessment to establish baseline for a skill.

- ~20 questions across all topics
- Mix of difficulty levels
- Creates initial progress profile

#### `/miz career progress`

Show overall learning progress across all skills.

```
───────────────────────────────────────
📈 **Learning Progress**

**Python** (proficient → expert)
███████████████░░░░░ 75%
Weak: concurrency, metaclasses

**System Design** (familiar → proficient)
████████░░░░░░░░░░░░ 40%
Weak: databases, caching

**Total:** 127 questions | 89 correct (70%)

───────────────────────────────────────
```

---

### Fetch Commands

#### `/miz career fetch leetcode`

Fetch LeetCode company-tagged questions from community GitHub repos.

Read `agents/add.md` and follow its instructions.

```
───────────────────────────────────────
📦 **Fetching LeetCode questions...**

| Company | Problems | New |
|---------|----------|-----|
| stripe | 45 | 45 |
| google | 892 | 892 |
| meta | 756 | 756 |

Saved to: ~/.miz/learning/community/leetcode/

───────────────────────────────────────
```

#### `/miz career fetch leetcode --company <name>`

Fetch questions for a specific company only.

Example: `/miz career fetch leetcode --company stripe`

#### `/miz career fetch leetcode --list`

List all available companies in the source.

---

### Case Commands

#### `/miz career case <job-id>`

Build the strongest case for a job you want to apply to.

**Prerequisites:** Job must exist in `~/.miz/activity/jobs/` with fit analysis completed.

Read `agents/analyze.md` and follow its instructions.

If no job-id provided, list available jobs:
```
───────────────────────────────────────
📋 **Jobs in pipeline**

| ID | Company | Title | Fit |
|----|---------|-------|-----|
| stripe-staff-backend | Stripe | Staff Backend Engineer | 85% |

Which job? Enter the ID:
```

---

## Data Model

```
~/.miz/profile/                      # MASTER PROFILE
├── identity.json
├── experience.json
├── education.json
├── skills.json
└── proof-points.json

~/.miz/activity/
├── tracker.md                # Applications tracker
└── jobs/*.json               # Analyzed jobs

~/.miz/interview/
├── banks/                    # Generic question banks
│   ├── behavioral.json
│   ├── coding/
│   └── system-design/
├── {company}.json            # Company data + questions
└── sessions/                 # Practice history
    └── {company}-{date}-{type}.json

~/.miz/learning/
├── progress.json             # Overall progress
├── banks/                    # Question banks by skill
│   ├── python/
│   ├── system-design/
│   └── databases/
└── {skill-slug}/             # Per-skill progress
    ├── progress.json
    └── sessions/

~/.miz/sources/
└── resume/                   # User's resumes
```

## Agent Routing

| Command | Agent | Purpose |
|---------|-------|---------|
| `init` | `agents/setup.md` | Setup local environment |
| `add resume` | `agents/add.md` | Parse resume → merge |
| `add job` | `agents/add.md` | Parse JD + company research + fit |
| `add brag` | `agents/add.md` | Capture achievement |
| `add doc` | `agents/add.md` | Extract proof points |
| `add question` | `agents/add.md` | Add interview question |
| `tracker` | `agents/tracker.md` | View/update tracker |
| `case` | `agents/analyze.md` | Build advocacy case |
| `prep` | `agents/prep.md` | Interview prep menu |
| `prep <company> behavioral` | `agents/learn.md` | Behavioral practice |
| `prep <company> coding` | `agents/learn.md` | Coding practice |
| `prep <company> system-design` | `agents/learn.md` | System design practice |
| `prep <company> mock` | `agents/learn.md` | Full mock interview |
| `learn` | `agents/learn.md` | Skills dashboard |
| `learn <skill>` | `agents/learn.md` | Practice skill |
| `progress` | `agents/learn.md` | Overall progress |
| `fetch leetcode` | `agents/add.md` | Fetch company questions |
