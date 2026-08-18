# Security Policy

Suki is local-first and privacy-by-default. User data (curricula, probe
history, books, career data) lives under `~/.suki/` on the user's machine and
is never transmitted anywhere except to the LLM/harness the user runs or via a
deliberate web fetch.

## Reporting a vulnerability

Suki has no server, no telemetry, and no third-party data storage, so most
security concerns are local. Still, if you find a vulnerability — anything that
could leak, corrupt, or delete a user's data under `~/.suki/`, or that sends
their data somewhere unintended — please report it privately.

- **Do not** open a public issue for security bugs.
- **Do** open a private security advisory at
  <https://github.com/grandimam/suki/security/advisories/new>, or email the
  maintainers via the GitHub profile.

You should expect an acknowledgement within 3 business days and a first
assessment within a week.

## Scope

In scope:

- The `suki` CLI (`src/suki/`)
- The skills (`home/`, `career/`, `curriculum/`, `learn/`, `probe/`, `book/`,
  `resume/`)
- Anything that reads, writes, or merges files under `~/.suki/`

Out of scope (responsibility of their owners):

- The LLM/harness the user runs, and any plugins for it
- Pandoc / LaTeX rendering toolchains
- Third-party packages

## Reporting a vulnerability: what to include

- Affected files / skill and the versions you tested
- Steps to reproduce (keep it minimal)
- Impact: what data is exposed, corrupted, or lost
- A suggested fix if you have one

Thanks for helping keep Suki honest and private.