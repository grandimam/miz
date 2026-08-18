# Contributing to Suki

Thanks for wanting to contribute. Suki is a stack of AI-agent skills that turns
an agent into a learning partner plus a career tool. Before you open a PR,
read this and the repo's `AGENTS.md` — it's the working guide for anyone
touching the source.

## Ground rules

1. **Never clobber user data.** Current state is JSON; history is append-only
   JSONL. Nothing is deleted. When in doubt, merge and append.
2. **Privacy by default.** All user data stays under `~/.suki/` on the user's
   machine. Never add a feature that sends user data anywhere except the
   LLM/harness or a deliberate web fetch.
3. **Brutal honesty.** Skills tell users the truth about fit and about their
   model. Never fabricate metrics, achievements, or mastery.
4. **The model is in the user's words.** `probe` forces restatement; never
   write the answer for the user.
5. **Accumulate, don't overwrite.** Every skill writes a named artifact that
   the next one reads. Preserve that chain.

## How to contribute

- **Bugs and feature requests**: open an issue using the provided templates.
- **Code**: open a PR against `main`. Keep it small and focused; one PR per
  change. Reference the issue it fixes.
- **Docs**: README says what the tool does; `SKILL.md` says how it behaves.
  Keep them in sync with the structure map in `AGENTS.md`.

## Setting up

```bash
git clone git@github.com:grandimam/suki.git
cd suki
pip install -e .       # or: pip install .
suki install --all     # link the skills into your agent
```

## Testing

Every change must pass the test harness:

```bash
bash test/run.sh
```

It validates every `SKILL.md` frontmatter, the full skill set, and the `suki`
CLI. It sets its own `SUKI_HOME` to a temp dir, so it never touches
`~/.suki/`. Make sure your change doesn't break it.

## Adding a new skill

Follow the checklist in `AGENTS.md` (Editing skills):

1. Add the folder + `SKILL.md` (frontmatter `name` must equal the folder name,
   `description` required and front-loaded with trigger keywords).
2. Register it in `src/suki/cli.py` (`SKILLS` array).
3. Wire it into `home/SKILL.md` routing and both dashboard command lists.
4. Update `test/run.sh`.

## Style and conventions

- JSON for structured data; Markdown for narratives and artifacts.
- File names `kebab-case.json`; dates `YYYY-MM-DD` or `YYYY-MM`.
- Job IDs `{company}-{slug}`; company slugs `kebab-case`.
- One folder per topic slug under `~/.suki/topics/`.
- No comments in code unless they earn their place.

## Code of conduct

All contributions are subject to our [Code of Conduct](CODE_OF_CONDUCT.md).
Be respectful, give and take feedback generously, and focus on what's best for
the project.