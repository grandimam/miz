# Miz (working instructions)

> Build expertise. Validate it. Own it.

This file is for AI agents working **on this repo** (the miz source), not for
users of the tool. Users read `README.md`; agents read this. If the two
disagree, trust the SKILL.md files, then this file.

Miz is a stack of skills that turns an AI agent into a learning partner plus
a career tool. Each skill is a folder with a `SKILL.md` that the runtime
loads as instructions. Skills share no code; they communicate through
artifacts on disk under `~/.miz/`.

## Repo map

```
miz/                            # this repo (source of the skills)
├── home/                       # umbrella router skill (installs as `miz`)
│   └── SKILL.md
├── career/                     # career layer (routed via /miz career ...)
│   ├── SKILL.md                #   the router for career subcommands
│   └── agents/                 #   one .md per subcommand (setup, add, prep, ...)
├── curriculum/                 # learning: design a learning path
├── learn/                      # learning: review material as a learner
├── probe/                      # learning: build + verify understanding
├── book/                       # learning: render a topic as a book
├── resume/                     # career: audit/improve/tailor the resume
├── src/miz/                    # Python package (the pip-installable `miz` CLI)
│   ├── cli.py                  #   installer + CLI router (install/topics/status/book)
│   ├── topics.py / status.py   #   miz topics, miz status
│   └── book.py                 #   miz book
├── pyproject.toml              # pip packaging (bundles skill dirs via force-include)
├── test/                       # test harness (run: bash test/run.sh)
├── README.md                   # user-facing documentation
└── AGENTS.md                   # this file
```

Install path: `pip install .` (or `pip install -e .`) then `miz install
--all`. The CLI lives in `src/miz/cli.py`; it links the skill dirs into the
agent's skill directory. Do not re-add a bash installer.

Runtime state the skills read/write lives **outside** this repo, under
`~/.miz/`. Never create or test against state inside the repo. See each
skill's SKILL.md for the exact files it touches.

## Hard rules (non-negotiable)

1. **Never clobber user data.** Current state is JSON; history is append-only
   JSONL. Nothing is deleted. When in doubt, merge and append.
2. **Privacy by default.** All user data stays under `~/.miz/` on the user's
   machine. The only external calls are the LLM/harness and web fetches.
3. **Brutal honesty.** Skills tell the user the truth about fit and about
   their model. Never fabricate metrics, achievements, or mastery.
4. **The model is in the user's words.** `probe` forces restatement; do not
   write the answer for the user.
5. **Accumulate, don't overwrite.** Every skill writes a named artifact that
   the next one reads. Preserve that chain.

## Conventions

- **JSON** for all structured data; **Markdown** for narratives and artifacts.
- Current state is JSON; history is append-only JSONL. Nothing is deleted.
- File names: `kebab-case.json`; dates: `YYYY-MM-DD` or `YYYY-MM`.
- Job IDs: `{company}-{slug}`; company slugs: `kebab-case`.
- Learning topics: one folder per slug under `~/.miz/topics/`.
- Skill folders: `SKILL.md` exactly, frontmatter `name` must equal the folder
  name, `description` required and front-loaded with trigger keywords.

## Editing skills

- Each skill's `SKILL.md` is the source of truth for its behavior. If a
  command's behavior lives in `career/agents/*.md`, that agent file is
  authoritative for that subcommand.
- Adding a new skill? Add the folder + `SKILL.md`, register it in
  `src/miz/cli.py` (the `SKILLS` array), wire it into `home/SKILL.md` routing
  and both dashboard command lists, then update `test/run.sh`.
- Keep README (what it does) and SKILL.md (how it behaves) in sync with this
  file's structure map.

## Verification

- Run `bash test/run.sh` after any change. It validates every `SKILL.md`
  frontmatter, the full skill set, and the `miz` CLI.
- The test harness sets its own `MIZ_HOME` to a temp dir; it never touches
  `~/.miz/`.
- `miz install` is idempotent and prunes stale skill dirs; run
  `pip install -e . && miz install --opencode` after skill changes if you
  want them live in OpenCode.

## Principles

1. **Brutal honesty first** — know the truth about fit and about the model
2. **The model is in the user's words** — the user restates it; it becomes theirs
3. **Accumulate, don't overwrite** — artifacts merge, never clobber
4. **Company-modeled prep** — practice the way that company actually asks
5. **Socratic learning** — the user thinks; the tool guides
6. **Continuous loop** — probe/mock → expose → fix → again until ready
7. **Gaps can reopen** — a weakness exposed later reopens the gap
8. **Memory is an artifact** — revisit metadata + JSONL history make progress durable
9. **Transparent sources** — every career data point has a reference
10. **Privacy by default** — everything stays local under `~/.miz/`