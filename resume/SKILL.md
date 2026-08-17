---
name: resume
description: |
  Audit, improve, and tailor the user's resume against their own profile and
  target jobs. Loads the resume from ~/.suki/sources/resume/ and the master
  profile from ~/.suki/profile/, scores every bullet for measurable impact,
  rewrites weak bullets (metrics, STAR, action verbs, keywords), checks ATS
  parsing, and tailors the resume to a specific job posting in
  ~/.suki/activity/jobs/. Use when asked to "improve my resume", "rewrite my
  resume", "make my resume better", "check my resume", "tailor my resume for
  <company>", or "fix my resume". Subcommands: /suki resume, /suki resume
  improve, /suki resume tailor <job-id>, /suki resume audit.
---

# Resume

Your resume, made honest and effective.

This skill is the resume layer of the suki stack: it audits, rewrites, and
tailors your resume against the facts you've already captured in your
profile. All state lives under `~/.suki/`.

## UX Guidelines

Always use rich formatting for a polished terminal experience:

- **Box borders** for headers: `╭───╮ │ │ ╰───╯`
- **Separators** between sections: `───────────────────────────────────────`
- **Icons** for status: `✓` success, `⏳` loading, `→` actions
- **Bullets** for lists: `•`

## Principle: from profile, not from scratch

Your profile (`~/.suki/profile/*.json`) is the source of truth for what you
actually did. The resume should be a *projection* of the profile — the same
facts, selected and compressed for the reader. Never invent achievements,
metrics, or titles that are not in the profile. If the profile lacks a metric
you need, say so and mark it `[needs number]` rather than fabricating it.

## Commands

### `/suki resume` (no args)

Full audit of the latest resume against the profile.

1. Find the most recent resume in `~/.suki/sources/resume/` (prefer the
   newest file, any of `.md`, `.txt`, `.pdf`, `.docx`). If none exists, tell
   the user to add one first: `→ /suki career add resume`.
2. Load profile files: `identity.json`, `experience.json`, `education.json`,
   `skills.json`, `proof-points.json`.
3. Audit against the profile and render the scorecard.

### `/suki resume audit`

Same as `/suki resume` with no args.

### `/suki resume improve`

Rewrite the resume in place of the weak spots found by the audit.

- Preserve the resume's structure and the user's voice.
- Upgrade every weak bullet to: **action verb + what + measurable impact**.
- Inject keywords from `skills.json` and the profile naturally.
- Add a one-line headline under the name pulled from identity + current role.
- Do NOT invent facts. Use metrics from proof-points.json; mark missing ones
  `[needs number]`.
- Output the full improved resume as markdown, then save a copy to
  `~/.suki/sources/resume/{date}-improved.md` (append, never clobber).

### `/suki resume tailor <job-id>`

Tailor the resume to a specific job posting.

- Load `~/.suki/activity/jobs/{job-id}.json`.
- Reorder skills and highlights so the job's `must_have` requirements come
  first; demote or trim content that is not relevant.
- Map each `must_have` requirement to the strongest matching proof point.
- Call out honestly (in a hidden note to the user, not on the resume) which
  `must_have` items have no supporting evidence — those are gaps to close in
  prep, not things to fake on the resume.
- Save as `~/.suki/sources/resume/{date}-{job-id}-tailored.md`.

If no job-id provided, list available jobs in `~/.suki/activity/jobs/`:
```
───────────────────────────────────────
📋 **Jobs in pipeline**

| ID | Company | Title | Fit |
|----|---------|-------|-----|
| crowdstrike-red-team | CrowdStrike | Red Team Operator | — |

Which job? Enter the ID:
───────────────────────────────────────
```

## Audit Scorecard

Render this after every audit:

```
───────────────────────────────────────
📋 **Resume Audit** · {source file}
───────────────────────────────────────

**Contact & headline**
  ✓ name, email, location present
  ✗ headline missing (add a one-liner: role + top metric)

**Bullets**
  7 bullets scored · 3 strong / 2 weak / 2 no-metric
  • [WEAK] "Responsible for testing apps" → add action verb + impact
  • [NO METRIC] "Improved security posture" → needs a number

**Skills coverage**
  24 profile skills · 14 on resume · 10 missing
  missing: cloud-red-teaming, kerberos-internals ...

**Consistency vs profile**
  ✓ all resume facts trace to profile
  ✗ resume says "Penetration Tester", profile says "Security Engineer"

**ATS check**
  ✓ single-column layout, standard section headers
  ✗ skills in a two-column table (may confuse parsers)

**Score: 6/10**
───────────────────────────────────────
Next: → /suki resume improve   Rewrite the weak spots
───────────────────────────────────────
```

Rules for the scorecard:

- **Contact & headline** — 2 points if email/location present and headline
  exists; deduct for a missing headline or stale contact info.
- **Bullets** — every bullet gets strong / weak / no-metric. A strong bullet
  has an action verb, a specific thing, and an impact. Score = strong/total.
- **Skills coverage** — report profile skills missing from the resume. These
  are *keywords*; missing keywords cost ATS hits.
- **Consistency** — every resume claim must trace to a profile entry. Flag
  titles, dates, or companies that mismatch the profile. Never let the resume
  contradict the profile — an interviewer who spots it burns your credibility.
- **ATS** — flag two-column tables, images, tables for skills, missing
  standard section headers (Experience, Education, Skills).

## Where things live

```
~/.suki/profile/                # source of truth (read-only)
├── identity.json
├── experience.json
├── education.json
├── skills.json
└── proof-points.json

~/.suki/activity/jobs/*.json    # job postings to tailor against

~/.suki/sources/resume/         # resumes (append-only)
├── {date}-{name}-resume.pdf   # original
├── {date}-improved.md         # improved version
└── {date}-{job-id}-tailored.md # tailored version
```

## Honesty rules

1. **Never fabricate.** No invented metrics, employers, titles, or dates.
   Proof points are the only source of numbers.
2. **Mark missing metrics** as `[needs number]` — the user fills them in from
   memory, then they belong on the resume.
3. **Keep it truthful.** If the profile and resume disagree, the resume is
   wrong — fix it, don't hide it.
4. **Tailoring ≠ lying.** Reordering and emphasis are fine; claiming skills
   you don't have is not.