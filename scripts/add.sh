#!/usr/bin/env bash
# Add one or more videos to the library — everything mechanical, in one command.
#
# Usage:
#   bash scripts/add.sh https://youtu.be/XXXXXXXXXXX [more urls...]
#   pbpaste | bash scripts/add.sh          # from the clipboard
#
# Fetches captions, normalizes them, and reports which videos still need a
# note written. Stops there: writing the note is judgment, not plumbing.
# Safe to re-run — anything already fetched or already written is skipped.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BATCH="$ROOT/scripts/video_ids_added.txt"
# Clear last run's batch first: add_videos.py only rewrites this file when it has
# something to fetch, so a stale one would silently re-fetch the previous slate.
rm -f "$BATCH"

echo "── 1/3  registering links ──────────────────────────────"
if [ "$#" -gt 0 ]; then
  printf '%s\n' "$@" | python3 scripts/add_videos.py
else
  python3 scripts/add_videos.py
fi

if [ ! -s "$BATCH" ]; then
  echo
  echo "Nothing new to fetch — everything given is already in the corpus."
else
  echo
  echo "── 2/3  fetching captions ──────────────────────────────"
  bash scripts/fetch_transcripts.sh "$BATCH" 2>&1 | tail -5
fi

echo
echo "── 3/3  normalizing ────────────────────────────────────"
python3 scripts/normalize.py | tail -6

echo
echo "── videos still needing a note ─────────────────────────"
python3 - <<'PY'
import json
from pathlib import Path

root = Path.cwd()
manifest = json.loads((root / "source_transcripts/manifest.json").read_text(encoding="utf-8"))
written = {p.stem for p in (root / "notes").glob("*.md")}

deferred_file = root / "scripts/deferred_videos.txt"
deferred_text = deferred_file.read_text(encoding="utf-8") if deferred_file.exists() else ""

todo = [v for v in manifest["videos"]
        if v["id"] not in written and v["id"] not in deferred_text]

if not todo:
    print("  none — every fetched video has a note or is deferred.")
else:
    todo.sort(key=lambda v: v["upload_date"], reverse=True)
    for v in todo:
        print(f"  {v['id']}  {v['upload_date']}  {v['duration']:>6}  {v['title'][:58]}")
    print(f"\n  {len(todo)} to write. Transcripts are in source_transcripts/clean/")
    print("  Write notes/<id>.md for each, then: bash scripts/publish.sh")

# Keep notes_todo.txt in step so the list survives the shell session.
(root / "scripts/notes_todo.txt").write_text(
    "".join(f"{v['id']}\t{v['title']}\n" for v in todo), encoding="utf-8")
PY
