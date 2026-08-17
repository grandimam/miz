# Miz

> Stop applying to jobs you won't get.

Career tool built on Claude Code. Tells you the truth about your fit, helps you close gaps, and prepares you for interviews the way that company actually asks them.

```
SETUP → ADD → PREP → ANALYZE → LEARN ←──┐
               │        │        │       │
               │        │        ├── Work on gap (Socratic)
               │        │        ├── Checkpoint mock
               │        │        ├── Exposed? ──────────┘
               │        │        └── Full mock → Ready!
               │        │
               │        └── Fit + Gaps + Positioning
               │
               └── Intel (values, process, questions)
```

- **Profile** = who you are (facts, grows over time)
- **Prep** = company intel (values, questions, process)
- **Analyze** = fit score + gaps + positioning
- **Learn** = close gaps through Socratic practice + mock validation

## Structure

```
profile/                      # MASTER PROFILE (merged from all resumes)
├── identity.json             # Name, email, location, links
├── experience.json           # Work history (merged, deduped)
├── education.json            # Degrees, certifications
├── skills.json               # Expert/proficient/familiar (union)
└── proof-points.json         # Quantified achievements (merged)

activity/                     # JOBS + TRACKING
├── tracker.md                # Applications tracker (status + outcomes)
└── jobs/
    └── {job-id}.json         # Analyzed jobs (JD + requirements)

prep/                         # INTERVIEW PREP (per-company)
└── {company-slug}/
    ├── intel.json            # Company values, process, questions
    ├── analysis.json         # Fit score, gaps, positioning
    ├── stories/              # Prepared stories (artifacts)
    │   ├── failure.md
    │   ├── leadership.md
    │   └── ...
    └── sessions/             # Mock interview sessions
        └── {date}-mock.json

sources/                      # RAW INPUTS
├── manifest.json
├── resume/
└── work-samples/

agents/                       # AGENTS (6 total)
├── setup.md                  # First-time init
├── add.md                    # Add data (resume, job, brag, doc)
├── prep.md                   # Collect company intel
├── analyze.md                # Fit + gaps + positioning
├── learn.md                  # Close gaps + mock (continuous loop)
└── tracker.md                # Track applications

generated/
└── {job-id}/
    └── {date}-resume.md
```

## Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| `setup.md` | First-time init, create directories | `/miz init` |
| `add.md` | Add data (resume, job, brag, doc) | `/miz add <type>` |
| `prep.md` | Collect company intel (web search + user input) | `/miz prep <company>` |
| `analyze.md` | Fit score + gaps + positioning | `/miz analyze <company>` |
| `learn.md` | Close gaps (Socratic) + mock validation | `/miz learn <company>` |
| `tracker.md` | Track applications | `/miz tracker` |

## Commands

| Command | Description |
|---------|-------------|
| `/miz` | Status overview |
| `/miz init` | First-time setup |
| `/miz add resume` | Add resume (merges into profile) |
| `/miz add job` | Add job posting, derive positioning |
| `/miz add doc` | Add work sample (tech spec, RFC, etc.) |
| `/miz prep <company>` | Collect company intel |
| `/miz analyze <company>` | Analyze fit + gaps + positioning |
| `/miz learn <company>` | Close gaps, run mocks |
| `/miz tracker` | View/update applications |

## Workflow

### Phase 1: Setup + Profile

```
/miz init          → Create directories
/miz add resume    → Parse resume, merge into profile
/miz add brag      → Add achievements
```

### Phase 2: Add Job + Prep

```
/miz add job       → Parse JD, save requirements
/miz prep <company> → Research company (web search + user input)
```

Prep collects:
- Company values (with sources)
- Interview process (rounds, format)
- Real interview questions (behavioral, coding, system design)
- Tech stack and context
- Insider tips

### Phase 3: Analyze

```
/miz analyze <company>
```

Produces:
- **Fit score** — Do you meet the requirements?
- **Deal-breakers** — Mandatory requirements you're missing
- **Gaps** — What you need to work on (prioritized)
- **Strengths** — What to lead with
- **Positioning** — How to present yourself (if applying)

### Phase 4: Learn (Continuous Loop)

```
/miz learn <company>
```

The learn phase is a continuous loop:

1. **Work on gaps** — Socratic practice for each gap type:
   - Behavioral → Build stories with STAR structure
   - Values → Map proof points to company values
   - Technical → Knowledge check + application
   - System design → Design problems with trade-offs

2. **Checkpoint mock** — Quick validation (3-4 questions)
   - Tests closed gaps
   - Exposes weak areas
   - Reopens gaps if needed

3. **Full mock** — Complete interview simulation
   - All rounds based on company process
   - Realistic pressure and time constraints
   - Detailed feedback

4. **Loop** — If mock exposes issues, go back to step 1

```
Work on gap → Checkpoint → Exposed? → Work on gap → ...
                              ↓
                         Full mock
                              ↓
                     ✓ Ready for interview
```

## Data Formats

### Profile

| File | Purpose | Key Fields |
|------|---------|------------|
| `identity.json` | Contact info | name, email, location, linkedin, github |
| `experience.json` | Work history | company, role, dates, highlights, skills |
| `skills.json` | Skills inventory | expert, proficient, familiar, learning |
| `proof-points.json` | Achievements | id, summary, metrics, skills, story_ready |

### Job (`activity/jobs/{id}.json`)

```json
{
  "id": "company-role-slug",
  "company": "Company Name",
  "title": "Job Title",
  "requirements": {
    "must_have": ["requirement 1", "requirement 2"],
    "nice_to_have": ["requirement 3"]
  }
}
```

### Company Intel (`prep/{company}/intel.json`)

```json
{
  "company": "Company Name",
  "slug": "company-slug",
  "collected_at": "2026-05-02",

  "values": [
    {
      "name": "Value Name",
      "description": "Description",
      "source": "https://..."
    }
  ],

  "process": {
    "rounds": [
      {
        "name": "Round Name",
        "duration": "45 min",
        "focus": "What they test"
      }
    ],
    "style": "collaborative, focus on tradeoffs"
  },

  "questions": [
    {
      "text": "Question text",
      "type": "behavioral|coding|system_design",
      "source": "glassdoor.com/..."
    }
  ],

  "tech_stack": {
    "languages": ["Python", "Go"],
    "databases": ["PostgreSQL", "Redis"],
    "infrastructure": ["AWS", "Kubernetes"]
  },

  "insights": [
    {
      "text": "Insider tip",
      "source": "blind.com/..."
    }
  ],

  "sources": ["list of all URLs used"]
}
```

### Analysis (`prep/{company}/analysis.json`)

```json
{
  "company": "company-slug",
  "job_id": "job-id",
  "analyzed_at": "2026-05-02",

  "fit": {
    "score": 75,
    "requirements_met": 6,
    "requirements_partial": 2,
    "requirements_missed": 1,
    "deal_breakers": ["Banking domain"],
    "verdict": "Strong technical fit but missing mandatory requirement"
  },

  "gaps": [
    {
      "id": "gap-001",
      "title": "No failure story",
      "priority": "critical",
      "category": "behavioral",
      "status": "open",
      "evidence": ["3 questions about failures in collected questions"],
      "how_to_close": "Prepare a real failure story with learnings"
    }
  ],

  "strengths": [
    {
      "area": "Technical depth",
      "evidence": "10 years experience, multiple proof points at scale"
    }
  ],

  "positioning": {
    "headline": "10-year backend engineer scaling transaction systems",
    "lead_with": ["Scale experience", "Reliability focus"],
    "bridges": [
      {
        "gap": "Banking domain",
        "reframe": "Ad-tech revenue systems have same requirements"
      }
    ],
    "cover_letter_hook": "I've spent 10 years building systems where every transaction matters..."
  }
}
```

### Story Artifact (`prep/{company}/stories/failure.md`)

```markdown
# Failure Story

## The Story

{Structured STAR story}

## Key Points

- {point 1}
- {point 2}

## Company Framing

{How to frame for this specific company}

## Follow-up Answers

**Q: What would you do differently?**
A: {prepared answer}

**Q: How do you know you've changed?**
A: {prepared answer}
```

## Tracker

The tracker (`activity/tracker.md`) tracks application status:

```markdown
| Company | Role | Fit | Status | Stage | Outcome | Notes |
|---------|------|-----|--------|-------|---------|-------|
| Company A | Staff Backend | 85% | interviewing | system-design | pending | Round 3 Monday |
| Company B | Senior SWE | 78% | rejected | coding | failed | Struggled with DP |
| Company C | Platform Lead | 90% | offer | final | passed | Negotiating |
```

**Statuses:** `saved`, `applied`, `interviewing`, `offered`, `accepted`, `rejected`, `withdrawn`

**Stages:** `phone`, `coding`, `system-design`, `behavioral`, `hiring-manager`, `final`

**Outcomes:** `pending`, `passed`, `failed`

## Conventions

- **JSON** for all structured data
- **Markdown** for narratives and story artifacts
- File names: `kebab-case.json`
- IDs: `{company}-{slug}` (e.g., `stripe-staff-backend`)
- Company slugs: `kebab-case` (e.g., `stripe`, `dt-one`)
- Dates: `YYYY-MM-DD` or `YYYY-MM`

## Principles

1. **Brutal honesty first** — Know the truth about your fit before you apply
2. **Accumulate, don't overwrite** — Each resume adds to master profile
3. **Company-modeled prep** — Practice the way that company actually interviews
4. **Socratic learning** — User does the thinking, tool guides
5. **Continuous loop** — Mock → expose → fix → mock again until ready
6. **Transparent sources** — Every piece of data has a reference
7. **Privacy by default** — All data stays local
8. **Gaps can reopen** — If mock exposes weakness, gap goes back to open
