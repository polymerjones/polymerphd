#!/usr/bin/env python3
"""Add pasted YouTube links to a library's corpus, skipping anything already covered.

Accepts URLs or bare IDs, in any mixture, from a file or stdin. Handles the usual
YouTube URL shapes (watch?v=, youtu.be/, /shorts/, /live/, extra query params) and
ignores blank lines, comments and duplicates within the paste itself.

Reports four buckets so nothing is silently dropped:
  already fetched  - raw captions + metadata on disk, nothing to do
  already listed   - in ingest_state/video_ids_full.txt but not yet downloaded
  new              - appended to video_ids_full.txt and written to a fetch batch
  previously excluded - matches an id classify_channel.py deliberately excluded,
                        so the user can overrule that call knowingly

Writes the new ids to <library>/ingest_state/video_ids_added.txt for yt-dlp --batch-file.
Never deletes or rewrites existing transcripts.

Usage:
  python3 scripts/add_videos.py <slug> links.txt
  pbpaste | python3 scripts/add_videos.py <slug>
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import require_slug  # noqa: E402

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
    lib, rest = require_slug(sys.argv[1:],
                              "Usage: python3 scripts/add_videos.py <slug> [links.txt]")
    state_dir = lib.ingest_state_dir
    state_dir.mkdir(parents=True, exist_ok=True)
    full = state_dir / "video_ids_full.txt"
    excluded = state_dir / "excluded_videos.tsv"
    batch = state_dir / "video_ids_added.txt"
    full.touch(exist_ok=True)

    text = Path(rest[0]).read_text(encoding="utf-8") if rest else sys.stdin.read()
    pasted = list(extract(text))
    if not pasted:
        print("No video ids found in input.")
        return

    listed = [l.strip().split("=")[-1] for l in full.read_text(encoding="utf-8").splitlines()
              if l.startswith("http")]
    listed_set = set(listed)

    excluded_map = {}
    if excluded.exists():
        for line in excluded.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                excluded_map[parts[0]] = parts[1]

    fetched = {p.name.split(".")[0] for p in lib.raw_dir.glob("*.json3")} & \
              {p.name.split(".")[0] for p in lib.raw_dir.glob("*.info.json")}

    buckets = {"already fetched": [], "already listed": [], "previously excluded": [], "new": []}
    for vid in pasted:
        if vid in fetched:
            buckets["already fetched"].append(vid)
        elif vid in listed_set:
            buckets["already listed"].append(vid)
        elif vid in excluded_map:
            buckets["previously excluded"].append(vid)
        else:
            buckets["new"].append(vid)

    for name, ids in buckets.items():
        if not ids:
            continue
        print(f"\n{name} ({len(ids)}):")
        for vid in ids:
            note = f"  — excluded as: {excluded_map[vid]}" if name == "previously excluded" else ""
            print(f"  {vid}{note}")

    to_fetch = buckets["new"] + buckets["previously excluded"]
    if buckets["new"]:
        with full.open("a", encoding="utf-8") as fh:
            for vid in buckets["new"]:
                fh.write(f"https://www.youtube.com/watch?v={vid}\n")
        print(f"\nAppended {len(buckets['new'])} id(s) to {full.name}")

    if to_fetch:
        batch.write_text("".join(f"https://www.youtube.com/watch?v={v}\n" for v in to_fetch),
                          encoding="utf-8")
        print(f"Wrote {len(to_fetch)} id(s) to {batch.name} — ready to fetch.")
    else:
        print("\nNothing new to fetch; everything pasted is already covered.")


if __name__ == "__main__":
    main()
