#!/usr/bin/env bash
# Add one or more sources to a library — everything mechanical, in one command.
#
# Usage:
#   bash scripts/add.sh <slug> https://youtu.be/XXXXXXXXXXX [more urls...]
#   pbpaste | bash scripts/add.sh <slug>          # from the clipboard
#
# Dispatches by input shape: a YouTube URL/id goes through the caption-fetch
# pipeline below. Other kinds (PDF, EPUB, website, plain text) have their own
# add_<kind>.py scripts once a library needs them — see CLAUDE.md.
#
# Fetches captions, normalizes them, and reports which videos still need a
# note written. Stops there: writing the note is judgment, not plumbing.
# Safe to re-run — anything already fetched or already written is skipped.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SLUG="${1:?Usage: bash scripts/add.sh <slug> [input...]}"
shift
LIB="$ROOT/libraries/$SLUG"

if [ ! -d "$LIB" ]; then
  echo "No such library: $SLUG (expected $LIB)" >&2
  exit 1
fi

mkdir -p "$LIB/ingest_state"
BATCH="$LIB/ingest_state/video_ids_added.txt"
# Clear last run's batch first: add_videos.py only rewrites this file when it has
# something to fetch, so a stale one would silently re-fetch the previous slate.
rm -f "$BATCH"

echo "── 1/3  registering links ──────────────────────────────"
if [ "$#" -gt 0 ]; then
  printf '%s\n' "$@" | python3 scripts/add_videos.py "$SLUG"
else
  python3 scripts/add_videos.py "$SLUG"
fi

if [ ! -s "$BATCH" ]; then
  echo
  echo "Nothing new to fetch — everything given is already in the corpus."
else
  echo
  echo "── 2/3  fetching captions ──────────────────────────────"
  bash scripts/fetch_transcripts.sh "$SLUG" "$BATCH" 2>&1 | tail -5
fi

echo
echo "── 3/3  normalizing ────────────────────────────────────"
python3 scripts/normalize.py "$SLUG" | tail -6

echo
echo "── sources still needing a note ────────────────────────"
python3 - "$SLUG" <<'PY'
import json
import sys
from pathlib import Path

root = Path.cwd()
slug = sys.argv[1]
lib = root / "libraries" / slug

manifest = json.loads((lib / "sources" / "manifest.json").read_text(encoding="utf-8"))
written = {p.stem for p in (lib / "notes").glob("*.md")}

deferred_file = lib / "deferred_sources.txt"
deferred_text = deferred_file.read_text(encoding="utf-8") if deferred_file.exists() else ""

todo = [s for s in manifest["sources"]
        if s["id"] not in written and s["id"] not in deferred_text]

if not todo:
    print("  none — every fetched source has a note or is deferred.")
else:
    todo.sort(key=lambda s: s.get("upload_date", ""), reverse=True)
    for s in todo:
        stamp = s.get("upload_date", "")
        length = s.get("duration", "")
        print(f"  {s['id']}  {stamp}  {length:>6}  {s['title'][:58]}")
    print(f"\n  {len(todo)} to write. Clean source text is in libraries/{slug}/sources/clean/")
    print(f"  Write libraries/{slug}/notes/<id>.md for each, then: bash scripts/publish.sh")

# Keep notes_todo.txt in step so the list survives the shell session.
(lib / "ingest_state").mkdir(exist_ok=True)
(lib / "ingest_state" / "notes_todo.txt").write_text(
    "".join(f"{s['id']}\t{s['title']}\n" for s in todo), encoding="utf-8")
PY
