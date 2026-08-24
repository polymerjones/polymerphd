#!/usr/bin/env python3
"""List every video on a YouTube channel, for classifying before ingestion.

Wraps a single yt-dlp --flat-playlist call against a channel's uploads tab and
writes the result to ingest_state/channel_full.tsv (id, availability, duration
in seconds, title — tab-separated, no header). Nothing is fetched or written
to the library's sources/ — this is a listing step only, meant to run before
deciding (by hand, or with a per-library classifier like classify_channel.py)
which ids actually go into add.sh.

This is the same yt-dlp invocation that produced restorative-physiology's
channel_full.tsv, made reusable and slug-parameterized instead of one-off.

Usage:
  python3 scripts/list_channel.py <slug> <channel_url>
  python3 scripts/list_channel.py dupuytren https://www.youtube.com/@DupuytrenFoundation
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import require_slug  # noqa: E402

PRINT_TEMPLATE = "%(id)s\t%(availability)s\t%(duration)s\t%(title)s"


def main():
    lib, rest = require_slug(sys.argv[1:],
                              "Usage: python3 scripts/list_channel.py <slug> <channel_url>")
    if not rest:
        sys.exit("Usage: python3 scripts/list_channel.py <slug> <channel_url>")
    channel_url = rest[0].rstrip("/")
    videos_url = channel_url if channel_url.endswith("/videos") else channel_url + "/videos"

    state_dir = lib.ingest_state_dir
    state_dir.mkdir(parents=True, exist_ok=True)
    out = state_dir / "channel_full.tsv"

    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", PRINT_TEMPLATE, videos_url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"yt-dlp failed ({result.returncode}):\n{result.stderr}")

    out.write_text(result.stdout, encoding="utf-8")

    rows = [line for line in result.stdout.splitlines() if line.strip()]
    total_seconds = 0.0
    for line in rows:
        parts = line.split("\t")
        if len(parts) >= 3:
            try:
                total_seconds += float(parts[2])
            except ValueError:
                pass

    print(f"Wrote {out} — {len(rows)} videos, ~{total_seconds / 3600:.1f} h total runtime")


if __name__ == "__main__":
    main()
