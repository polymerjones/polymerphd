#!/usr/bin/env python3
"""
Normalize yt-dlp json3 auto-captions into readable transcripts.

Reads  libraries/<slug>/sources/raw/<id>.en-orig.json3  (falls back to .en.json3)
       libraries/<slug>/sources/raw/<id>.info.json
Writes libraries/<slug>/sources/clean/<id>.txt
       libraries/<slug>/sources/manifest.json   (metadata for the source catalog)

Originals in raw/ are read-only — never modified.

Usage:
  python3 scripts/normalize.py <slug>
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import require_slug  # noqa: E402

ANCHOR_EVERY_SEC = 60

# Sound-effect and non-speech caption tags.
TAG_RE = re.compile(r"\[[^\]]{0,40}\]")

# Channel boilerplate: subscription asks, like prompts, generic sign-offs.
BOILERPLATE_PATTERNS = [
    r"\b(?:please\s+)?(?:don'?t forget to\s+)?(?:like(?:,| and)?\s+)?subscribe\b[^.?!]*[.?!]",
    r"\bhit the (?:like|bell|notification)[^.?!]*[.?!]",
    r"\bring the bell\b[^.?!]*[.?!]",
    r"\bsmash that like\b[^.?!]*[.?!]",
    r"\bleave a comment\b[^.?!]*[.?!]",
    r"\blet me know in the comments\b[^.?!]*[.?!]",
    r"\bcheck the (?:link|description) below\b[^.?!]*[.?!]",
    r"\bthis (?:video|channel) is (?:not|for) (?:medical|educational)[^.?!]*[.?!]",
]
BOILERPLATE_RE = re.compile("|".join(BOILERPLATE_PATTERNS), re.IGNORECASE)


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def caption_path(raw_dir, vid):
    """Prefer the original-language track over the machine-translated one."""
    for suffix in (".en-orig.json3", ".en.json3"):
        p = raw_dir / f"{vid}{suffix}"
        if p.exists():
            return p
    return None


def extract_events(data):
    """Yield (start_seconds, text) from json3, dropping rolling-window duplicates."""
    for ev in data.get("events", []):
        # aAppend events re-send the tail of the previous caption line.
        if ev.get("aAppend"):
            continue
        segs = ev.get("segs")
        if not segs:
            continue
        text = "".join(seg.get("utf8", "") for seg in segs)
        text = text.replace("\n", " ").strip()
        if not text:
            continue
        yield ev.get("tStartMs", 0) / 1000.0, text


def dedupe_consecutive(events):
    """Drop lines identical to, or fully contained in, the line just before."""
    out = []
    for start, text in events:
        if out:
            prev = out[-1][1]
            if text == prev or text in prev:
                continue
        out.append((start, text))
    return out


def clean_text(text):
    text = TAG_RE.sub(" ", text)
    text = BOILERPLATE_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def mmss(seconds):
    return f"{int(seconds) // 60:02d}:{int(seconds) % 60:02d}"


def build_body(events):
    """Join caption lines into flowing paragraphs with periodic [mm:ss] anchors."""
    paragraphs = []
    current = []
    next_anchor = 0.0

    for start, text in events:
        if start >= next_anchor:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            current.append(f"[{mmss(start)}]")
            next_anchor = start + ANCHOR_EVERY_SEC
        current.append(text)

    if current:
        paragraphs.append(" ".join(current))

    cleaned = []
    for para in paragraphs:
        # Keep the anchor, clean only the prose after it.
        m = re.match(r"^(\[\d{2}:\d{2}\])\s*(.*)$", para, re.DOTALL)
        if m:
            anchor, prose = m.group(1), clean_text(m.group(2))
            if prose:
                cleaned.append(f"{anchor} {prose}")
        else:
            prose = clean_text(para)
            if prose:
                cleaned.append(prose)
    return "\n\n".join(cleaned)


def fmt_date(raw):
    if raw and len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return "not available"


def main():
    lib, _ = require_slug(sys.argv[1:], "Usage: python3 scripts/normalize.py <slug>")
    raw_dir, clean_dir = lib.raw_dir, lib.clean_dir
    clean_dir.mkdir(parents=True, exist_ok=True)

    info_files = sorted(raw_dir.glob("*.info.json"))
    if not info_files:
        sys.exit("No .info.json files found — run fetch_transcripts.sh first.")

    existing = lib.load_manifest()
    # Keep any non-youtube sources (pdf/website/text) already in the manifest untouched.
    other_sources = [s for s in existing.get("sources", []) if s.get("kind") != "youtube"]

    sources = []
    skipped = []

    for info_path in info_files:
        vid = info_path.name[: -len(".info.json")]
        info = read_json(info_path)

        title = info.get("title") or "not available"
        duration = info.get("duration")
        url = info.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}"
        dur_str = mmss(duration) if duration else "not available"

        cap = caption_path(raw_dir, vid)
        if cap is None:
            skipped.append({"id": vid, "title": title, "url": url,
                             "duration_seconds": duration, "duration": dur_str,
                             "reason": "no captions"})
            continue

        events = dedupe_consecutive(extract_events(read_json(cap)))
        body = build_body(events)
        if not body.strip():
            skipped.append({"id": vid, "title": title, "url": url,
                             "duration_seconds": duration, "duration": dur_str,
                             "reason": "empty transcript"})
            continue

        date = fmt_date(info.get("upload_date"))

        header = (
            f"TITLE: {title}\n"
            f"VIDEO ID: {vid}\n"
            f"URL: {url}\n"
            f"UPLOAD DATE: {date}\n"
            f"DURATION: {dur_str}\n"
            f"CAPTION TRACK: {cap.name.split('.')[-2]}\n"
            f"{'=' * 70}\n\n"
        )
        (clean_dir / f"{vid}.txt").write_text(header + body + "\n", encoding="utf-8")

        sources.append({
            "id": vid,
            "kind": "youtube",
            "title": title,
            "url": url,
            "upload_date": date,
            "duration_seconds": duration,
            "duration": dur_str,
            "word_count": len(body.split()),
            "clean_file": f"clean/{vid}.txt",
            "anchor": {
                "kind": "timestamp", "format": "mm:ss",
                "bound_field": "duration_seconds", "bound": duration,
            },
        })

    sources.sort(key=lambda r: r["title"].lower())
    lib.save_manifest({"sources": other_sources + sources, "skipped": skipped})

    total_words = sum(r["word_count"] for r in sources)
    print(f"normalized : {len(sources)}")
    print(f"skipped    : {len(skipped)}")
    for s in skipped:
        print(f"  - {s['id']}: {s['reason']}")
    print(f"total words: {total_words:,}")
    print(f"manifest   : {lib.manifest_path}")


if __name__ == "__main__":
    main()
