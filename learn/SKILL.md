---
name: learn
description: |
  Review a draft chapter, lesson, or guide section from a serious learner's
  perspective so it actually teaches. Use when you want a structured audit for
  prerequisite jumps, unclear terminology, weak examples, vague drills, missing
  compression, or places where authoritative prose still fails to teach the
  model cleanly. Runs inside the curriculum workflow.
---

# Learn Review

Use this skill to critique teaching material as a demanding learner rather than
as a subject-matter author.

The goal is not stylistic editing for its own sake. The goal is to find where a
smart, motivated learner would still fail to build the intended mental model.

## Inputs

Provide the learn review with:

- the draft chapter or section
- the topic and intended audience
- the chapter's place in the sequence
- any relevant whole-book architecture or recurring ideas
- any neighboring chapters that matter for prerequisite context

## What to audit

Check for:

- hidden prerequisite jumps
- unclear, unstable, or overloaded terminology
- places where the prose sounds confident but is not yet cognitively clear
- examples that illustrate content without actually teaching the model
- missing contrasts, boundary cases, or bridge explanations
- drills that are vague, passive, or disconnected from the chapter's core idea
- compression that fails to leave the learner with durable takeaways

## Output shape

Return a concise audit with these sections:

1. `Verdict`
   One short paragraph on whether the chapter would actually teach a serious
   learner well at this point in the sequence.

2. `Findings`
   A flat list of the most important teaching problems, ordered by severity.
   Focus on comprehension risk, not line editing.

3. `Revision priorities`
   A short list of the highest-leverage fixes.

4. `Keep`
   Briefly note what is already teaching well so revisions do not destroy it.

## Rules

- Review from the learner's perspective, not as a co-author trying to show off
  expertise.
- Prefer conceptual clarity over prose polish.
- Be specific about where understanding breaks.
- Distinguish between "missing information" and "bad sequencing."
- Do not rewrite the whole chapter unless explicitly asked. Diagnose first.
- Keep the audit private working material unless the user asks to see it.
