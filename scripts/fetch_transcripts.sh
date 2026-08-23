#!/usr/bin/env bash
# Fetch auto-caption transcripts + metadata for a slate of videos.
# Subtitles only — no video or audio is downloaded.
# Safe to re-run: --no-overwrites skips anything already fetched.
#
# Usage:
#   bash scripts/fetch_transcripts.sh <slug>                                # the original slate
#   bash scripts/fetch_transcripts.sh <slug> libraries/<slug>/ingest_state/video_ids_added.txt
#
# add_videos.py writes ingest_state/video_ids_added.txt, so pass that after adding links.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLUG="${1:?Usage: bash scripts/fetch_transcripts.sh <slug> [batch-file]}"
LIB="$ROOT/libraries/$SLUG"
RAW="$LIB/sources/raw"
BATCH="${2:-$LIB/ingest_state/video_ids.txt}"

if [ ! -d "$LIB" ]; then
  echo "No such library: $SLUG (expected $LIB)" >&2
  exit 1
fi

if [ ! -f "$BATCH" ]; then
  echo "No batch file at: $BATCH" >&2
  echo "Run add_videos.py first, or pass an explicit batch file." >&2
  exit 1
fi

echo "batch file : $BATCH ($(grep -c . "$BATCH") ids)"
mkdir -p "$RAW"

yt-dlp \
  --skip-download \
  --write-auto-subs \
  --sub-langs "en-orig,en" \
  --sub-format json3 \
  --write-info-json \
  --no-overwrites \
  --ignore-errors \
  --no-warnings \
  --sleep-requests 1.5 \
  --sleep-interval 2 \
  --max-sleep-interval 5 \
  --retries 5 \
  --extractor-retries 3 \
  -o "$RAW/%(id)s.%(ext)s" \
  --batch-file "$BATCH"

echo
echo "=== fetch summary ==="
echo "info.json files : $(ls "$RAW"/*.info.json 2>/dev/null | wc -l | tr -d ' ')"
echo "caption files   : $(ls "$RAW"/*.json3 2>/dev/null | wc -l | tr -d ' ')"
