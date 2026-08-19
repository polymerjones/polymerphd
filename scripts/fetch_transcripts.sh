#!/usr/bin/env bash
# Fetch auto-caption transcripts + metadata for the selected video slate.
# Subtitles only — no video or audio is downloaded.
# Safe to re-run: --no-overwrites skips anything already fetched.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW="$ROOT/source_transcripts/raw"
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
  --batch-file "$ROOT/scripts/video_ids.txt"

echo
echo "=== fetch summary ==="
echo "info.json files : $(ls "$RAW"/*.info.json 2>/dev/null | wc -l | tr -d ' ')"
echo "caption files   : $(ls "$RAW"/*.json3 2>/dev/null | wc -l | tr -d ' ')"
