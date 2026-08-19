#!/usr/bin/env python3
"""Add pasted YouTube links to the corpus, skipping anything already covered.

Accepts URLs or bare IDs, in any mixture, from a file or stdin. Handles the usual
YouTube URL shapes (watch?v=, youtu.be/, /shorts/, /live/, extra query params) and
ignores blank lines, comments and duplicates within the paste itself.

Reports four buckets so nothing is silently dropped:
  already fetched  - raw captions + metadata on disk, nothing to do
  already listed   - in video_ids_full.txt but not yet downloaded
  new              - appended to video_ids_full.txt and written to a fetch batch
  previously excluded - matches an id classify_channel.py deliberately excluded,
                        so the user can overrule that call knowingly

Writes the new ids to scripts/video_ids_added.txt for yt-dlp --batch-file.
Never deletes or rewrites existing transcripts.

Usage:
  python3 scripts/add_videos.py links.txt
  pbpaste | python3 scripts/add_videos.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FULL = ROOT / "scripts" / "video_ids_full.txt"
EXCLUDED = ROOT / "scripts" / "excluded_videos.tsv"
BATCH = ROOT / "scripts" / "video_ids_added.txt"
RAW = ROOT / "source_transcripts" / "raw"

# 11-char YouTube id, as it appears in every URL shape the site uses.
ID = r"[A-Za-z0-9_-]{11}"
PATTERNS = [
    re.compile(rf"(?:v=|/shorts/|/live/|/embed/|youtu\.be/)({ID})"),
    re.compile(rf"^({ID})$"),
]


def extract(text):
    """Yield ids in paste order, de-duplicated, from URLs or bare ids."""
    seen = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for pat in PATTERNS:
            m = pat.search(line)
            if m:
                vid = m.group(1)
                if vid not in seen:
                    seen.add(vid)
                    yield vid
                break
        else:
            print(f"  ?  could not read an id from: {line[:70]}", file=sys.stderr)


def main():
    text = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    pasted = list(extract(text))
    if not pasted:
        print("No video ids found in input.")
        return

    listed = [l.strip().split("=")[-1] for l in FULL.read_text(encoding="utf-8").splitlines()
              if l.startswith("http")]
    listed_set = set(listed)

    excluded = {}
    if EXCLUDED.exists():
        for line in EXCLUDED.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                excluded[parts[0]] = parts[1]

    fetched = {p.name.split(".")[0] for p in RAW.glob("*.json3")} & \
              {p.name.split(".")[0] for p in RAW.glob("*.info.json")}

    buckets = {"already fetched": [], "already listed": [], "previously excluded": [], "new": []}
    for vid in pasted:
        if vid in fetched:
            buckets["already fetched"].append(vid)
        elif vid in listed_set:
            buckets["already listed"].append(vid)
        elif vid in excluded:
            buckets["previously excluded"].append(vid)
        else:
            buckets["new"].append(vid)

    for name, ids in buckets.items():
        if not ids:
            continue
        print(f"\n{name} ({len(ids)}):")
        for vid in ids:
            note = f"  — excluded as: {excluded[vid]}" if name == "previously excluded" else ""
            print(f"  {vid}{note}")

    to_fetch = buckets["new"] + buckets["previously excluded"]
    if buckets["new"]:
        with FULL.open("a", encoding="utf-8") as fh:
            for vid in buckets["new"]:
                fh.write(f"https://www.youtube.com/watch?v={vid}\n")
        print(f"\nAppended {len(buckets['new'])} id(s) to {FULL.name}")

    if to_fetch:
        BATCH.write_text("".join(f"https://www.youtube.com/watch?v={v}\n" for v in to_fetch),
                         encoding="utf-8")
        print(f"Wrote {len(to_fetch)} id(s) to {BATCH.name} — ready to fetch.")
    else:
        print("\nNothing new to fetch; everything pasted is already covered.")


if __name__ == "__main__":
    main()
