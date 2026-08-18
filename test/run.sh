#!/usr/bin/env bash
# suki tests — no external deps beyond python3 (for yaml) and the tools themselves.
set -e
FAIL=0
ok() { echo "  ok: $1"; }
bad() { echo "FAIL: $1"; FAIL=1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export SUKI_HOME="$(mktemp -d)"
echo "SUKI_HOME=$SUKI_HOME"

echo "1. all SKILL.md frontmatter is valid YAML and name matches expected skill name"
expect_name() {
  case "$1" in
    home) echo suki ;;
    career) echo career ;;
    curriculum) echo curriculum ;;
    learn) echo learn ;;
    probe) echo probe ;;
    book) echo book ;;
    resume) echo resume ;;
  esac
}
for f in "$ROOT"/*/SKILL.md; do
  dir="$(basename "$(dirname "$f")")"
  want="$(expect_name "$dir")"
  if [ -z "$want" ]; then bad "$f: unexpected skill folder"; continue; fi
  out=$(python3 - "$f" "$want" <<'PY'
import yaml, sys, glob
content = open(sys.argv[1]).read()
parts = content.split("---", 2)
if len(parts) < 3: sys.exit("no frontmatter")
fm = yaml.safe_load(parts[1])
if "name" not in fm: sys.exit("no name")
if "description" not in fm: sys.exit("no description")
if fm["name"] != sys.argv[2]: sys.exit(f"name {fm['name']!r} != expected {sys.argv[2]!r}")
PY
  ) || bad "$f: $out" && ok "$dir"
done

echo "2. skills list is complete"
expected="book career curriculum learn probe resume suki"
got=$(grep -h '^name:' "$ROOT"/*/SKILL.md | awk '{print $2}' | sort | tr '\n' ' ')
[ "$got" = "$expected " ] && ok "7 skills present" || bad "skill set mismatch: got [$got]"

echo "3. fixtures + bin helpers"
SUKI_HOME="$SUKI_HOME" "$ROOT/test/make_fixture.sh" python >/dev/null
PY() { PYTHONPATH="$ROOT/src" python3 -m suki.cli "$@"; }
count=$(SUKI_HOME="$SUKI_HOME" PY topics | grep -c python)
[ "$count" = "1" ] && ok "suki topics lists python" || bad "suki topics"

progress=$(SUKI_HOME="$SUKI_HOME" PY status python 2>/dev/null | grep -o '[0-9.]*%')
[ -n "$progress" ] && ok "suki status shows progress ($progress)" || bad "suki status no progress"

echo "4. missing topic is a clean error"
if SUKI_HOME="$SUKI_HOME" PY status nope >/tmp/qs.out 2>&1; [ $? -eq 1 ]; then ok "exit 1 for missing topic"; else bad "status missing topic"; fi

echo "5. status --due lists reviews in aligned columns"
due=$(SUKI_HOME="$SUKI_HOME" PY status --due 2>/dev/null)
echo "$due" | grep -q 'python' && ok "suki status --due lists python" || bad "status --due no output"
echo "$due" | grep -q $'\t' && bad "status --due still tab-separated" || ok "status --due uses aligned columns"

echo "6. demo seeds a topic"
SUKI_HOME="$SUKI_HOME" PY demo >/dev/null
[ -f "$SUKI_HOME/topics/demo/curriculum.json" ] && ok "demo seeds curriculum.json" || bad "demo no curriculum.json"
if SUKI_HOME="$SUKI_HOME" PY demo >/tmp/qdemo.out 2>&1; then bad "demo clobbered existing topic"; else ok "demo refuses to clobber"; fi

echo "7. map renders the guide as a tree"
mout=$(SUKI_HOME="$SUKI_HOME" PY map python 2>/dev/null)
echo "$mout" | grep -q 'Tier 1' && ok "suki map shows Tier 1" || bad "suki map no tiers"
echo "$mout" | grep -q '1.1' && ok "suki map shows chapter 1.1" || bad "suki map no chapters"

echo "8. focus persists and reads back"
SUKI_HOME="$SUKI_HOME" PY focus learning >/dev/null
[ "$(SUKI_HOME="$SUKI_HOME" PY focus | grep -o 'learning')" = "learning" ] && ok "suki focus persists" || bad "suki focus no persist"

echo "9. export/import round-trips without clobbering"
EXP="$SUKI_HOME/backup.tgz"
SUKI_HOME="$SUKI_HOME" PY export "$EXP" >/dev/null
[ -f "$EXP" ] && ok "suki export writes a tarball" || bad "suki export no tarball"
NEWHOME="$(mktemp -d)"
SUKI_HOME="$NEWHOME" PY import "$EXP" >/dev/null
[ -f "$NEWHOME/topics/python/curriculum.json" ] && ok "suki import restores topics" || bad "suki import missing topics"
SUKI_HOME="$NEWHOME" PY import "$EXP" >/tmp/qimp.out 2>&1
grep -q 'skipped' /tmp/qimp.out && ok "suki import skips existing" || bad "suki import clobbered existing"

echo "10. book renders to tex without a pdf engine needed (--tex-only)"
SUKI_HOME="$SUKI_HOME" PY book python --tex-only >/tmp/qb.out 2>&1
book="$SUKI_HOME/topics/python/book/book.tex"
[ -f "$book" ] && ok "book.tex produced ($book)" || { bad "no book.tex"; cat /tmp/qb.out; }
grep -q 'Tier 1' "$book" && ok "book.tex contains Tier 1" || bad "book.tex missing Tier 1"

echo "11. book --preview renders a single tier"
SUKI_HOME="$SUKI_HOME" PY book python --tex-only --preview 1 >/tmp/qbp.out 2>&1
grep -q 'Tier 1' "$book" && ok "book --preview renders tier 1" || { bad "book --preview failed"; cat /tmp/qbp.out; }

echo
if [ "$FAIL" = "1" ]; then echo "RESULT: FAIL"; exit 1; fi
echo "RESULT: all tests passed"
