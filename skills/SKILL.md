# Miz

Your career, reflected.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions
- **Bullets** for lists: `•`

## Commands

On EVERY invocation, first check if `profile/identity.json` exists.

If file does not exist, show welcome:

```
╭─────────────────────────────────────╮
│  miz                         │
│  Your career, reflected.            │
╰─────────────────────────────────────╯

Welcome! I don't have your profile yet.

→ Run `/miz init` to get started
```

### Available Commands

#### `/miz` (no args)

Show current status:
1. Check if `profile/identity.json` exists
2. If NO → show welcome message above
3. If YES → read profile files and show rich status dashboard:

```
╭─────────────────────────────────────╮
│  miz · {Name}                │
╰─────────────────────────────────────╯

**{Current Role}** at {Company}
{Location}

───────────────────────────────────────
📊 **Profile**

• Experience: {X} years across {Y} companies
• Skills: {top 3 expert skills}
• Proof points: {count}
• Sources: {count} files

───────────────────────────────────────
🎯 **Job Pipeline**

• {count} jobs tracked
• {count} with fit analysis

───────────────────────────────────────
🎤 **Interview Prep**

• {count} companies researched
• {count} practice sessions

───────────────────────────────────────
📚 **Learning**

• {count} skills tracked
• {count} topics due for review

───────────────────────────────────────
**Quick actions**

→ `/miz add job` — Analyze a job
→ `/miz prep <company>` — Practice interviews
→ `/miz learn` — Improve your skills
→ `/miz tracker` — View applications
```

#### `/miz init`

First-time setup. Creates directories, initializes profile files, guides user through adding resume.

Read `agents/setup.md` and follow its instructions.

#### `/miz status`

Same as `/miz` with no args.

---

### Add Commands

All `/miz add` commands process immediately.

#### `/miz add resume`

Add a resume and merge into profile.

Read `agents/add-resume.md` and follow its instructions.

#### `/miz add job [url]`

Add a job description, analyze fit, derive positioning, research company.

- If URL provided → fetch and analyze automatically
- If no URL → prompt for URL or paste JD text

Read `agents/add-job.md` and follow its instructions.

#### `/miz add brag`

Capture a professional achievement.

Read `agents/add-brag.md` and follow its instructions.

#### `/miz add doc`

Add a tech spec, RFC, design doc, or work sample.

Read `agents/add-doc.md` and follow its instructions.

---

### Tracker Commands

#### `/miz tracker`

View and update the applications tracker.

Read `agents/tracker.md` and follow its instructions.

**Subcommands:**
- `/miz tracker` — Show tracker table
- `/miz tracker update <job-id> --status <status>` — Update job status
- `/miz tracker update <job-id> --stage <stage>` — Update interview stage
- `/miz tracker update <job-id> --outcome <outcome>` — Update stage outcome
- `/miz tracker note <job-id> <note>` — Update notes

**Statuses:** `saved`, `applied`, `interviewing`, `offered`, `accepted`, `rejected`, `withdrawn`

**Stages:** `phone`, `coding`, `system-design`, `behavioral`, `hiring-manager`, `final`

**Outcomes:** `pending`, `passed`, `failed`

---

### Interview Prep Commands

#### `/miz prep <company>`

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

#### `/miz prep <company> behavioral`

Behavioral interview practice.

Read `agents/behavioral.md` and follow its instructions.

Features:
- Questions aligned with company values
- Answers suggested from YOUR proof points
- STAR format coaching
- Feedback from company's perspective

#### `/miz prep <company> coding`

Coding interview practice.

Read `agents/coding.md` and follow its instructions.

Features:
- Questions from company's known patterns
- Fallback to general question bank
- Hints and walkthroughs
- Complexity analysis

#### `/miz prep <company> system-design`

System design interview practice.

Read `agents/system-design.md` and follow its instructions.

Features:
- Problems relevant to company domain
- Discussion-based format
- Trade-off analysis
- Company-specific considerations

---

### Learning Commands

#### `/miz learn`

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

#### `/miz learn <skill>`

Practice a specific skill.

Read `agents/learn.md` and follow its instructions.

Features:
- Evaluate by topic and subtopic
- Track correct/incorrect answers
- Spaced repetition scheduling
- Identify and drill weak areas

#### `/miz learn <skill> --topic <topic>`

Focus on a specific topic within a skill.

Example: `/miz learn python --topic concurrency`

#### `/miz learn <skill> --review`

Review topics due for spaced repetition.

Prioritizes:
1. Overdue topics
2. Low confidence topics
3. Low score topics

#### `/miz learn <skill> --assess`

Run a full assessment to establish baseline for a skill.

- ~20 questions across all topics
- Mix of difficulty levels
- Creates initial progress profile

#### `/miz progress`

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

#### `/miz fetch leetcode`

Fetch LeetCode company-tagged questions from community GitHub repos.

Read `agents/fetch.md` and follow its instructions.

```
───────────────────────────────────────
📦 **Fetching LeetCode questions...**

| Company | Problems | New |
|---------|----------|-----|
| stripe | 45 | 45 |
| google | 892 | 892 |
| meta | 756 | 756 |

Saved to: learning/community/leetcode/

───────────────────────────────────────
```

#### `/miz fetch leetcode --company <name>`

Fetch questions for a specific company only.

Example: `/miz fetch leetcode --company stripe`

#### `/miz fetch leetcode --list`

List all available companies in the source.

---

### Case Commands

#### `/miz case <job-id>`

Build the strongest case for a job you want to apply to.

**Prerequisites:** Job must exist in `activity/jobs/` with fit analysis completed.

Read `agents/case-agent.md` and follow its instructions.

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
profile/                      # MASTER PROFILE
├── identity.json
├── experience.json
├── education.json
├── skills.json
└── proof-points.json

activity/
├── tracker.md                # Applications tracker
└── jobs/*.json               # Analyzed jobs

interview/
├── banks/                    # Generic question banks
│   ├── behavioral.json
│   ├── coding/
│   └── system-design/
├── {company}.json            # Company data + questions
└── sessions/                 # Practice history
    └── {company}-{date}-{type}.json

learning/
├── progress.json             # Overall progress
├── banks/                    # Question banks by skill
│   ├── python/
│   ├── system-design/
│   └── databases/
└── {skill-slug}/             # Per-skill progress
    ├── progress.json
    └── sessions/

sources/
└── resume/                   # User's resumes
```

## Agent Routing

| Command | Agent | Purpose |
|---------|-------|---------|
| `init` | `agents/setup.md` | Setup local environment |
| `add resume` | `agents/add-resume.md` | Parse resume → merge |
| `add job` | `agents/add-job.md` | Parse JD + company research + fit |
| `add brag` | `agents/add-brag.md` | Capture achievement |
| `add doc` | `agents/add-doc.md` | Extract proof points |
| `add question` | `agents/add-question.md` | Add interview question |
| `tracker` | `agents/tracker.md` | View/update tracker |
| `case` | `agents/case-agent.md` | Build advocacy case |
| `prep` | `agents/prep.md` | Interview prep menu |
| `prep <company> behavioral` | `agents/behavioral.md` | Behavioral practice |
| `prep <company> coding` | `agents/coding.md` | Coding practice |
| `prep <company> system-design` | `agents/system-design.md` | System design practice |
| `prep <company> mock` | `agents/mock-interview.md` | Full mock interview |
| `learn` | `agents/learn.md` | Skills dashboard |
| `learn <skill>` | `agents/learn.md` | Practice skill |
| `progress` | `agents/learn.md` | Overall progress |
| `fetch leetcode` | `agents/fetch.md` | Fetch company questions |
