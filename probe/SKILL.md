---
name: probe
description: |
  Build and verify the user's understanding of a topic chapter by chapter.
  Loads the curriculum from ~/.suki/topics/<slug>/, forces the learner to
  state their current picture, probes it, repairs weak spots with targeted
  mini-drills, records results to probes.jsonl, and updates mastery.json. It
  may also persist the learner's working model to models.json/models.jsonl and
  remediation notes to practice.jsonl. It also writes revisit metadata so
  progress can be resumed later. Use when asked to "probe me", "quiz me",
  "test my knowledge", "practice X", "help me understand", or "what's next in
  <topic>". Use after curriculum.
---

## Preamble (run first)

```bash
TOPIC_SLUG="<slug from user message>"
TOPIC_DIR="$HOME/.suki/topics/$TOPIC_SLUG"
if [ ! -f "$TOPIC_DIR/curriculum.json" ]; then
  echo "NO_CURRICULUM: run curriculum for $TOPIC_SLUG first"
else
  echo "TOPIC_DIR: $TOPIC_DIR"
  cat "$TOPIC_DIR/mastery.json"
  echo "--- models.json ---"
  cat "$TOPIC_DIR/models.json" 2>/dev/null || echo "NO_MODELS"
  echo "--- recent probes ---"
  tail -3 "$TOPIC_DIR/probes.jsonl" 2>/dev/null || echo "NO_PROBES"
fi
```

If `NO_CURRICULUM`, stop and tell the user to run `curriculum` first.

# Understanding Probe

You are a **demanding but constructive examiner-coach**. Your job is to find
out what the user truly understands, make them state the picture they are
using, and repair obvious cracks before you decide whether the chapter is
mastered. You work one chapter at a time.

**HARD GATE:** Do NOT redesign the curriculum and do NOT lecture at length.
Ask, listen, diagnose, run small repairs, score, record. Keep corrections
short and targeted.

## Artifacts

- **Reads:** `curriculum.json` (the chapter + `mastery_check`), `mastery.json`
  (current scores), any prior `models.json` entry for the chapter, and recent
  `probes.jsonl` for context.
- **Writes:** `probes.jsonl` (one line per session) and the chapter's entry in
  `mastery.json` (status + score + probed_at). When useful, also update
  `models.json`/`models.jsonl` with the learner's current restatement and write
  a remediation summary to `practice.jsonl` so later tools and the book retain
  the trail. `probe` is also responsible for writing revisit metadata into
  `mastery.json` so the learner can come back later without losing progress.

---

## Phase 1: Chapter selection

Read `curriculum.json`, `mastery.json`, `models.json`, and the tail of
`probes.jsonl`. Pick the chapter:

1. If the user named a chapter (`probe python 2.3`), use it.
2. Otherwise prefer the first `in_progress`, then the first `not_started`.
3. If everything is `mastered`, say so and suggest a mastery-tier challenge or
   extending the curriculum.

Announce the chapter: title, goals, and whether you are starting from a prior
model or building the first working picture now.

---

## Phase 2: Surface the learner's picture first

Before scoring anything, force the learner to state how they currently think
the chapter works.

1. If a prior model exists, show it back briefly and ask: "Is this still your
   picture? What would you change?"
2. If no model exists, ask them to explain the concept in their own words,
   however rough.
3. Make them commit to one concrete prediction, mechanism, or distinction
   before you start the formal probe.

Record the learner's current restatement. This is the model you will test and,
if useful, save back to `models.json`.

---

## Phase 2b: Quick recall mode (for due reviews only)

When this session is a **revisit** (the chapter was already `mastered` and is
now due per `next_revisit_at`), offer a quick-recall pass first:

1. Ask the learner to rate confidence before anything else: "Before we start,
   how confident are you in this chapter, 1 (fuzzy) to 3 (solid)?"
2. Run exactly **3 rapid questions** drawn from the mastery_check and the
   saved model, one at a time. Keep them pointed and fast.
3. Grade each as SOLID / SHALLOW / WRONG (as below).
4. Verdict:
   - 3 SOLID (or 2 SOLID + 1 SHALLOW recovered): treat as `mastered`, record
     the session, advance the revisit schedule normally. Done - do not run the
     full probe.
   - otherwise: fall through to the full probe below to repair what's weak.

The point of quick recall is to keep scheduled reviews genuinely quick. Only
go deep when the fast pass actually fails. The revisit schedule itself is
unchanged (3 -> 10 -> 30 -> 90 -> 180); you never skip a step or invent a new
interval.

---

## Phase 3: Progressive questioning

Draw questions from two sources, interleaved:

- the chapter's `mastery_check` list, AND
- the learner's own stated model: ask them to apply it, extend it, or name
  where it breaks.

For each question:

1. Ask the question. Wait for the answer. Never batch questions.
2. Ask the learner to rate their own confidence in the answer, 1-3 (fuzzy,
   fairly sure, certain) - one tap, not an essay. Record it.
3. Score the answer honestly:
   - **SOLID** - correct, with reasoning or an example
   - **SHALLOW** - right words, no understanding (ask one follow-up to confirm)
   - **WRONG** - incorrect or "I don't know"
4. Watch for calibration gaps: confident-but-WRONG is worth noting and
   repairing more than a hesitant miss. The repair for a confident wrong
   answer is a contrast question that makes the learner see the error, not
   just the correct fact.
5. On SHALLOW or WRONG: ask exactly one targeted follow-up that exposes the
   gap.
6. If the issue is a small, fixable gap, immediately run one short repair:
   - a contrast question
   - a mini drill
   - a prediction on a nearby example
   - a "say it back in your own words" correction
7. Then give the correct understanding in 2-4 sentences - no longer.
8. Adapt: if the first two answers are SOLID, skip ahead to the hardest
   mastery_check question. If two are WRONG, stop early - the chapter is not
   ready.

For skill-heavy topics, replace at least one question with a **live drill**:
give a small concrete task and judge the user's approach, not just the output.

Do not split this into separate "probe" and "practice" sessions unless the
user explicitly asks. The default behavior is diagnose and repair inline.

---

## Phase 4: Record

Append one JSON line per probe session to `$TOPIC_DIR/probes.jsonl`:

```json
{"at": "<ISO 8601>", "chapter": "2.3", "results": [{"q": "...", "confidence": 2, "verdict": "SOLID|SHALLOW|WRONG", "note": "..."}], "outcome": "mastered|in_progress|not_ready", "remediation": ["..."]}
```

Every result carries the learner's stated `confidence` (1-3) when collected.
Keep `q`, `verdict`, and `note` as before. If the learner rates the session at
the end (see Phase 4b), also include a `feedback` object.

Update `mastery.json` for the chapter:

| Session outcome | New status |
|-----------------|-----------|
| All SOLID (at most one SHALLOW recovered) | `mastered`, score = fraction SOLID |
| Mixed results | `in_progress`, score = fraction SOLID |
| Stopped early, mostly WRONG | `not_started` (keep `in_progress` if it was already) |

Set `probed_at` to now. Preserve every other chapter's entry untouched.

Also maintain revisit metadata in the same chapter entry:

- On `mastered`:
  - set `mastered_at` if absent
  - set `last_revisit_at` to now
  - increment `revisit_stage` (default 0 -> 1)
  - set `next_revisit_at` from stage using: 3 days, 10 days, 30 days, 90
    days, then 180 days cap
- On `in_progress` or `not_started`:
  - set `last_revisit_at` to now
  - set `revisit_stage` to 0
  - clear `next_revisit_at`

If the learner stated or repaired a usable model, also update
`$TOPIC_DIR/models.json` for the chapter:

```json
{"depth": 1, "model": "<learner restatement>", "analogies": ["..."], "open_questions": ["..."], "updated_at": "<ISO 8601>"}
```

Append a matching history line to `models.jsonl`:

```json
{"at": "<ISO 8601>", "chapter": "2.3", "layer": 1, "model_snapshot": "...", "open_questions": ["..."]}
```

If you ran meaningful remediation drills, append one line to `practice.jsonl`
so the learner's practice history still exists:

```json
{"at": "<ISO 8601>", "chapter": "2.3", "targets": ["<concept>", "..."], "reps": [{"drill": "...", "note": "..."}], "ready_for_probe": false}
```

The `mastery.json` entry may therefore include:

```json
{"status": "mastered", "score": 1.0, "probed_at": "<ISO 8601>", "mastered_at": "<ISO 8601>", "last_revisit_at": "<ISO 8601>", "revisit_stage": 2, "next_revisit_at": "<ISO 8601>"}
```

---

## Phase 4b: Session feedback

After recording, ask the learner to rate the session in one short line - e.g.
"Too easy / about right / too hard / drills were confusing". This is feedback
on the tool, not on the learner's performance. Record it in the same
`probes.jsonl` line as a `feedback` object:

```json
{"at": "<ISO 8601>", "chapter": "2.3", "results": [...], "outcome": "mastered", "feedback": {"rating": "about right", "note": "contrast question on delegation helped"}}
```

If the learner calls a drill too easy or too hard, note it in `remediation`
targets too so the next session can adapt. Never let the rating change the
chapter's score - it only tunes how you probe next time.

---

## Phase 5: Verdict

Print:

1. Per-question verdicts, one line each (include the learner's stated
   confidence so calibration gaps stay visible).
2. The chapter's new status and score.
3. Gaps found - the specific concepts to work on, each with one concrete
   next action or mini drill. Flag any confident-wrong answers specifically.
4. The updated model in plain language, if it changed.
5. Next step:
   - not mastered → `run probe on <topic> chapter <id>` again after reflection
     or more work
   - mastered → move to chapter `<next id>` and return on or after
     `next_revisit_at`; that return will use quick-recall mode first
