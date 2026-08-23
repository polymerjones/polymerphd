#!/usr/bin/env bash
# Rebuild every output from every library's notes, then push so the shared link updates.
#
# Usage:
#   bash scripts/publish.sh                 # rebuild, show what changed, don't push
#   bash scripts/publish.sh --push          # rebuild and push to GitHub
#
# Run after writing or editing any note. The build scripts refuse to write if a
# note is malformed, so a bad note fails here rather than shipping.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PUSH=0
[ "${1:-}" = "--push" ] && PUSH=1

LIBRARIES=("$ROOT"/libraries/*/library.json)
if [ ! -e "${LIBRARIES[0]}" ]; then
  echo "No libraries found under $ROOT/libraries/*/library.json" >&2
  exit 1
fi

echo "── 1/3  source catalogs ────────────────────────────────"
for cfg in "${LIBRARIES[@]}"; do
  slug="$(basename "$(dirname "$cfg")")"
  python3 scripts/build_catalog.py "$slug"
done

echo
echo "── 2/3  offline web app ────────────────────────────────"
python3 scripts/build_app_data.py

echo
echo "── 3/3  iOS project ────────────────────────────────────"
python3 scripts/make_xcodeproj.py | tail -4

echo
echo "── changed ─────────────────────────────────────────────"
git status --porcelain | sed 's/^/  /'

if [ "$PUSH" -eq 1 ]; then
  if [ -z "$(git status --porcelain)" ]; then
    echo
    echo "Nothing to publish — no files changed."
    exit 0
  fi
  NEW=$(git status --porcelain libraries/*/notes/ | grep -c '^??' || true)
  echo
  echo "── publishing ──────────────────────────────────────────"
  git add -A
  git commit -q -m "Add ${NEW} note(s) and rebuild outputs"
  git push -q origin main
  echo "  pushed. https://polymerjones.github.io/polymerphd/ updates in ~1 min."
else
  echo
  echo "Reviewed and happy? Publish with:  bash scripts/publish.sh --push"
fi
