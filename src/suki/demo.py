"""suki-demo: seed a sample micro-topic so new users can feel the loop fast.

Usage:
  suki demo                      # seed the sample topic
  suki demo --force              # overwrite an existing demo topic

Creates ~/.suki/topics/demo/ with a tiny curriculum + mastery so the user can
immediately run /suki probe demo 1.1 without building anything first.
"""
import argparse
import datetime as dt
import json
import os
import shutil
import sys

SUKI_HOME = os.environ.get("SUKI_HOME", os.path.expanduser("~/.suki"))
TOPICS_DIR = os.path.join(SUKI_HOME, "topics")

SLUG = "demo"
TOPIC = "Demo: State Machines"


def iso_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def build_curriculum():
    return {
        "topic": TOPIC,
        "slug": SLUG,
        "version": 1,
        "created_at": iso_now(),
        "goal_depth": "mastery",
        "tiers": [
            {
                "tier": 1,
                "name": "Foundations",
                "chapters": [
                    {
                        "id": "1.1",
                        "title": "What is a state machine",
                        "goals": ["Recognize state machines in everyday systems", "Name states, transitions, and events"],
                        "concepts": ["state", "event", "transition", "initial state"],
                        "drills": ["List 3 everyday systems that are state machines"],
                        "mastery_check": ["In your own words, what is a state?", "What makes a transition fire?"],
                        "est_hours": 1,
                    },
                    {
                        "id": "1.2",
                        "title": "Modeling with states",
                        "goals": ["Sketch a state machine from a description"],
                        "concepts": ["state diagram", "guarded transitions", "self-loop"],
                        "drills": ["Draw the states of a vending machine"],
                        "mastery_check": ["Where would you use a self-loop?"],
                        "est_hours": 1,
                    },
                ],
            },
            {
                "tier": 2,
                "name": "Practice",
                "chapters": [
                    {
                        "id": "2.1",
                        "title": "Your first machine",
                        "goals": ["Design a state machine from a real scenario"],
                        "concepts": ["reachability", "deadlock", "termination"],
                        "drills": ["Model a turnstile"],
                        "mastery_check": ["What is reachability and why does it matter?"],
                        "est_hours": 1,
                    }
                ],
            },
        ],
    }


def build_mastery(curriculum):
    chapters = {}
    for tier in curriculum["tiers"]:
        for ch in tier["chapters"]:
            chapters[ch["id"]] = {"status": "not_started", "score": None, "probed_at": None}
    return {"slug": SLUG, "updated_at": iso_now(), "chapters": chapters}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser(description="Seed the demo topic.")
    ap.add_argument("--force", action="store_true", help="overwrite an existing demo topic")
    args = ap.parse_args(argv)

    target = os.path.join(TOPICS_DIR, SLUG)
    if os.path.exists(target):
        if not args.force:
            print(f"demo topic already exists at {target}; use --force to reseed")
            return 1
        shutil.rmtree(target)

    os.makedirs(target, exist_ok=True)
    curriculum = build_curriculum()
    with open(os.path.join(target, "curriculum.json"), "w") as f:
        json.dump(curriculum, f, indent=2)
    with open(os.path.join(target, "mastery.json"), "w") as f:
        json.dump(build_mastery(curriculum), f, indent=2)

    print(f"seeded demo topic at {target}")
    print("try: /suki probe demo 1.1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
