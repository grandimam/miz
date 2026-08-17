#!/usr/bin/env bash
# Create a realistic fixture topic under $SUKI_HOME for testing.
# Usage: SUKI_HOME=<dir> test/make_fixture.sh [slug]
set -e
SLUG="${1:-python}"
[ -n "$SUKI_HOME" ] || { echo "set SUKI_HOME first" >&2; exit 1; }
DIR="$SUKI_HOME/topics/$SLUG"
mkdir -p "$DIR"

cat > "$DIR/README.md" <<'EOF'
# Python

## Table of contents

### Tier 1: Foundation
- 1.1 Setup & syntax
- 1.2 Control flow

### Tier 2: Competence
- 2.1 Functions & scope
EOF

cat > "$DIR/curriculum.json" <<'EOF'
{"topic":"Python","slug":"python","version":1,"created_at":"2026-08-01T09:00:00Z","goal_depth":"mastery",
"tiers":[
 {"tier":1,"name":"Foundation","chapters":[
   {"id":"1.1","title":"Setup & syntax","goals":["Run Python interactively","Read basic error messages"],"concepts":["interpreter","REPL","syntax errors"],"drills":["Install Python and run a hello script","Deliberately break the script and read the traceback"],"mastery_check":["What does the REPL do?","How do you read a traceback bottom-up?"],"est_hours":2},
   {"id":"1.2","title":"Control flow","goals":["Write if/else and loops"],"concepts":["conditionals","for/while","break/continue"],"drills":["FizzBuzz","Sum a list with a loop"],"mastery_check":["When does a while loop terminate?"],"est_hours":3}]},
 {"tier":2,"name":"Competence","chapters":[
   {"id":"2.1","title":"Functions & scope","goals":["Define functions","Understand scope"],"concepts":["def","arguments","LEGB"],"drills":["Refactor a script into functions"],"mastery_check":["Explain LEGB rule"],"est_hours":4}]}]}
EOF

cat > "$DIR/mastery.json" <<'EOF'
{"slug":"python","updated_at":"2026-08-09T10:00:00Z","chapters":{
 "1.1":{"status":"mastered","score":1.0,"probed_at":"2026-08-02T10:00:00Z","mastered_at":"2026-08-02T10:00:00Z"},
 "1.2":{"status":"in_progress","score":0.5,"probed_at":"2026-08-09T10:00:00Z"},
 "2.1":{"status":"not_started","score":null,"probed_at":null}}}
EOF

cat > "$DIR/probes.jsonl" <<'EOF'
{"at":"2026-08-02T10:00:00Z","chapter":"1.1","results":[{"q":"What does the REPL do?","verdict":"SOLID","note":""},{"q":"How do you read a traceback bottom-up?","verdict":"SOLID","note":""}],"outcome":"mastered"}
{"at":"2026-08-09T10:00:00Z","chapter":"1.2","results":[{"q":"When does a while loop terminate?","verdict":"SHALLOW","note":"recited definition, could not apply"}],"outcome":"in_progress"}
EOF

cat > "$DIR/practice.jsonl" <<'EOF'
{"at":"2026-08-09T14:00:00Z","chapter":"1.2","targets":["while loop conditions"],"reps":[{"drill":"Predict loop iterations before running","note":"improved after 2 reps"}],"ready_for_probe":false}
EOF

echo "fixture ready at $DIR"
