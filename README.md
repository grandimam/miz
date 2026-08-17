# Miz

> Stop applying to jobs you won't get.

You've applied to 50 jobs. Heard back from 3. Bombed an interview because you blanked on a behavioral question you should've nailed.

**The problem isn't your experience. It's that you don't know yourself well enough and every tool out there lies to you.**

Miz tells you the truth. It knows your experience better than you do. It tells you which jobs you'll actually get (and which ones you won't). And when you blank in an interview, it reminds you: "Remember that time you reduced latency by 40x? Use that."

All local. All private. All yours.

## The Problem

**Job hunting is broken:**

- You apply to jobs you're not qualified for (wasting everyone's time)
- You skip jobs you'd be perfect for (because the JD sounds intimidating)
- You prep with generic interview questions (that don't match how the company actually interviews)
- You forget your own accomplishments (and undersell yourself)
- You cram before interviews, forget everything, repeat

**Every career tool tells you what you want to hear. Miz tells you the truth.**

## What Makes It Different

### 1. Brutal Honesty First

Most tools validate you. Miz confronts you.

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
the banking gap. You'll waste their time and yours.
```

Stop spray-and-praying. Know your fit before you apply.

---

### 2. Practice The Way That Company Asks

Generic prep is lazy:

> "Tell me about a time you showed leadership."

That's not how real companies interview. Each has their own values, their own style, their own signals they look for.

When you add a job, Miz researches the company—scrapes their careers page, engineering blog, Glassdoor reviews—and builds an intel file. Then it asks you questions _the way they would ask them_:

```
┌──────────────────────────────────────────────────────────────────┐
│  INTERVIEWER (based on company research)                         │
│                                                                  │
│  "Your target company values 'ownership'—seeing things through  │
│   from start to finish. Tell me about a time you took full      │
│   ownership of a project, including the parts outside your      │
│   comfort zone."                                                 │
└──────────────────────────────────────────────────────────────────┘
```

Practice like it's the real thing. Because it basically is.

---

### 3. Answers From YOUR Experience

You blank on behavioral questions because you forget your own accomplishments.

Miz doesn't. When you say "help," it searches your profile and suggests an answer from your actual experience:

```
📌 Suggested proof point from your profile:

"Redesigned data pipeline, reducing P95 latency from 200ms to 5ms"

STAR Format:

• Situation: The platform was hitting latency issues at scale.
             The team was okay with 200ms P95.

• Task: Maintain SLAs while traffic grew 10x.

• Action: Pushed back. Redesigned with batching + caching.
          Refused to accept 200ms when 5ms was achievable.

• Result: P95 dropped to 5ms. Zero incidents in 6 months.

Company Angle (based on their values):
"I wasn't satisfied with 'good enough.' That aligns with your
target company's focus on engineering excellence."
```

Your stories. Your numbers. Their framing.

---

### 4. Skills That Actually Stick

You cram before interviews. Forget everything after. Repeat.

Miz uses spaced repetition (SM-2 algorithm). As you practice, it tracks what you know and what you don't. Topics you're weak on come back. Topics you've mastered fade away.

```
📊 Your Progress (example after a few sessions)

| Topic          | Score | Confidence | Next Review |
|----------------|-------|------------|-------------|
| basics         | 95%   | ✓ high     | —           |
| data-structures| 85%   | ✓ high     | in 7 days   |
| concurrency    | 45%   | ✗ low      | TODAY       |
| advanced       | 30%   | ✗ low      | TODAY       |

Recommendation: Review concurrency (due today, low confidence)
```

No more cramming. Just steady improvement.

## How It Works

### Step 1: Build Your Profile

```bash
/miz init
```

Paste your resume. Miz extracts everything: experience, skills, quantified achievements. Add multiple resumes—they merge together, building a complete picture of your career.

### Step 2: Analyze Jobs (Get the Truth)

```bash
/miz add job
```

Paste any job description. Get:

- **Fit score** — Honest assessment, not validation
- **Deal-breakers** — Mandatory requirements you're missing
- **Company intel** — Their values, interview process, what they look for

### Step 3: Practice Interviews (Company-Modeled)

```bash
/miz prep <company> behavioral
/miz prep <company> coding
/miz prep <company> system-design
```

Practice with an interviewer who asks questions based on the company's researched values and interview style. Get feedback. Get better.

### Step 4: Master Your Skills (Spaced Repetition)

```bash
/miz learn <skill>
/miz learn <skill> --review
```

Evaluate your knowledge. Drill weak areas. Track progress over time.

### Step 5: Track Everything (See Patterns)

```bash
/miz tracker
```

See all your applications in one place:

```
| Company   | Role           | Fit | Status       | Stage         | Outcome |
|-----------|----------------|-----|--------------|---------------|---------|
| Company A | Staff Backend  | 85% | interviewing | system-design | pending |
| Company B | Senior SWE     | 78% | rejected     | coding        | failed  |
| Company C | Platform Lead  | 90% | offer        | final         | passed  |
```

See patterns. "I keep failing coding rounds" → focus your practice there.

---

## Who This Is For

- **Senior engineers (5+ years)** actively job hunting
- People who've applied to 20+ jobs with low response rates
- People who blank on behavioral questions they should nail
- People frustrated with generic "tell me about a time" prep
- Privacy-conscious professionals who don't want career data in some startup's cloud

## Who This Is NOT For

- Entry-level engineers (you need more experience to have proof points)
- People who want to be told they're great (you'll get honest feedback instead)
- Non-technical roles (this is built for software engineers)
- Passive job seekers (this is for active hunting)

## Commands

| Command                                    | What it does                   |
| ------------------------------------------ | ------------------------------ |
| `/miz`                              | Status dashboard               |
| `/miz init`                         | First-time setup               |
| `/miz add job`                      | Analyze a job posting (honest) |
| `/miz add resume`                   | Add another resume             |
| `/miz add brag`                     | Capture an achievement         |
| `/miz prep <company>`               | Interview prep menu            |
| `/miz prep <company> behavioral`    | Behavioral practice            |
| `/miz prep <company> coding`        | Coding practice                |
| `/miz prep <company> system-design` | System design practice         |
| `/miz learn <skill>`                | Practice a skill               |
| `/miz learn <skill> --review`       | Spaced repetition review       |
| `/miz case <job-id>`                | Build advocacy case            |
| `/miz resume <job-id>`              | Generate tailored resume       |
| `/miz tracker`                      | View/update applications       |
| `/miz progress`                     | Learning dashboard             |

## Installation

```bash
# Install Claude Code
npm install -g @anthropic/claude-code

# Clone miz
git clone https://github.com/grandimam/miz.git
cd miz

# Start
claude
```

That's it. `/miz` is now available.

## Privacy

Everything stays on your machine. Your resumes, your profile, your interview practice—none of it leaves your computer.

The only external calls:

- LLM/Harness
- Web fetches (to read job postings and research companies)

Your career data is yours alone.

## Philosophy

1. **Brutal honesty first** — Know the truth about your fit before you apply
2. **Your voice, not AI's** — Answers come from your real experience, not generated fluff
3. **Company-modeled prep** — Practice the way that company actually interviews
4. **Learn for keeps** — Spaced repetition over cramming
5. **Privacy by default** — Your career data never leaves your machine

---

## The Difference

| Generic Prep               | Miz                                                                        |
| -------------------------- | --------------------------------------------------------------------------------- |
| "You're a great fit!"      | "Fit: 65%. Banking is mandatory. You don't have it."                              |
| "Tell me about leadership" | Questions shaped by the company's actual values (researched when you add a job)  |
| Generic STAR answers       | Your actual proof points, pulled from your profile                                |
| Cram, forget, repeat       | Spaced repetition—weak topics come back until you know them                       |
| Data in someone's cloud    | Everything local, everything yours                                                |

---

**Miz: The career tool that tells you the truth.**
