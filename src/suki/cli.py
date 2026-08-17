"""suki: single CLI for the suki stack.

Usage:
  suki                      install skills into agent dirs (auto-detect)
  suki install [--opencode|--claude|--codex|--all]
  suki topics [--verbose]   list topics under ~/.suki/topics/
  suki status [topic] [--json|--due]
  suki book <topic> [--paper a5|a4|letter] [--tex-only] [--keep-md]
"""
import os
import sys
from pathlib import Path

from . import book as book_mod
from . import status as status_mod
from . import topics as topics_mod

SUKI_HOME = Path(os.environ.get("SUKI_HOME", Path.home() / ".suki"))
SKILLS = [
    ("suki", "home"),
    ("career", "career"),
    ("curriculum", "curriculum"),
    ("learn", "learn"),
    ("probe", "probe"),
    ("book", "book"),
    ("resume", "resume"),
]
OPENCODE_COMMAND = """---
description: Suki - a stack for building and validating expertise. Router: /suki career <args>, /suki curriculum <topic>, /suki learn <draft>, /suki probe <topic> [ch], /suki book <topic>, /suki resume [improve|tailor <job>], or /suki alone for the status dashboard.
---
Follow the suki skill and route this subcommand: $ARGUMENTS
"""


def skill_src_dir():
    """The directory holding the skill folders (installed package or repo)."""
    candidates = [
        Path(__file__).resolve().parent / "skills",
        Path(__file__).resolve().parent.parent.parent,  # repo root (src/suki/cli.py -> suki/)
    ]
    for c in candidates:
        if (c / "home" / "SKILL.md").is_file():
            return c
    raise FileNotFoundError("cannot locate the suki skills (expected a skills/ folder)")


def install_to(dest):
    dest.mkdir(parents=True, exist_ok=True)
    src = skill_src_dir()
    for name, _ in SKILLS:
        link = dest / name
        if link.is_symlink() or link.exists():
            if link.is_dir() and not link.is_symlink():
                print(f"skipping {link}: non-symlink dir exists")
                continue
            link.unlink()
        os.symlink(src / name, link)
        print(f"linked {link}")


def prune_stale(dest):
    if not dest.is_dir():
        return
    keep = {name for name, _ in SKILLS}
    for entry in dest.iterdir():
        if entry.name in keep:
            continue
        if entry.is_symlink():
            entry.unlink()
            print(f"pruned stale {entry}")


def install_opencode_command(dest):
    dest.mkdir(parents=True, exist_ok=True)
    stale = ["career", "curriculum", "learn", "probe", "book", "resume"]
    for name in stale:
        p = dest / f"{name}.md"
        if p.is_file():
            p.unlink()
            print(f"removed old command {p}")
    (dest / "suki.md").write_text(OPENCODE_COMMAND)
    print(f"wrote opencode command -> {dest / 'suki.md'}")


def cmd_install(argv):
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    targets = {
        "opencode": Path.home() / ".config" / "opencode",
        "claude": Path.home() / ".claude",
        "codex": codex_home,
    }

    argv = [a.lstrip("-") for a in argv]
    if not argv:
        for label, base in list(targets.items()):
            if base.is_dir():
                argv.append(label)
    if not argv:
        print("no agent config dirs found under your home; pass --opencode / --claude / --codex / --all")
        return 1
    if "all" in argv:
        argv = list(targets.keys())

    for label in argv:
        if label not in targets:
            print(f"unknown target: {label} (expected one of: opencode, claude, codex, all)")
            return 1
        dest = targets[label] / "skills"
        install_to(dest)
        if label == "opencode":
            install_opencode_command(targets[label] / "command")

    SUKI_HOME.mkdir(parents=True, exist_ok=True)
    print(f"state lives in {SUKI_HOME}/")
    print(f"skills: {' '.join(name for name, _ in SKILLS)}")
    print("restart your agent to pick up the skills")
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv or argv[0] == "install":
        return cmd_install(argv[1:])

    cmd, rest = argv[0], argv[1:]
    if cmd == "topics":
        return topics_mod.main(rest)
    if cmd == "status":
        return status_mod.main(rest)
    if cmd == "book":
        return book_mod.main(rest)
    print(f"unknown subcommand: {cmd}")
    print("usage: suki [install|topics|status|book]")
    return 1


if __name__ == "__main__":
    sys.exit(main())