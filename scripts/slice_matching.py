#!/usr/bin/env python3
"""Slice every section whose heading matches a regex, across all notes.

Practice and protocol material lives under video-specific headings ("The
protocol", "The three-minute protocol", "Practices, by time of day", ...), so a
fixed-heading slice cannot reach it. This copies the matching sections verbatim,
grouped by video, so 04_RESTORATIVE_PRACTICES.md can be written from one file
without loading all 58 notes in full.

Usage: slice_matching.py <regex> <out_dir> <out_name>
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"

PATTERN = re.compile(sys.argv[1], re.I)
OUT = Path(sys.argv[2])
NAME = sys.argv[3]


def parse(path):
    text = path.read_text(encoding="utf-8")
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            km = re.match(r"^(\w+): (.*)$", line)
            if km:
                fm[km.group(1)] = km.group(2).strip().strip('"')
        text = text[m.end():]
    return fm, text


def sections(text):
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    # parts[0] is the preamble; then alternating heading, body
    for i in range(1, len(parts), 2):
        yield parts[i].strip(), parts[i + 1].strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chunks, hit = [], 0
    for path in sorted(NOTES.glob("*.md")):
        fm, body = parse(path)
        matched = [(h, b) for h, b in sections(body) if PATTERN.search(h)]
        if not matched:
            continue
        hit += 1
        block = "\n\n".join(f"**{h}**\n\n{b}" for h, b in matched)
        chunks.append(
            f"### {fm.get('title', path.stem)}\n"
            f"`{fm.get('id', path.stem)}` · {fm.get('upload_date', 'not available')}\n\n{block}\n"
        )
    dest = OUT / NAME
    dest.write_text(
        f"# Matched sections: /{PATTERN.pattern}/\n\nFrom {hit} of "
        f"{len(list(NOTES.glob('*.md')))} notes.\n\n" + "\n---\n\n".join(chunks) + "\n",
        encoding="utf-8",
    )
    print(f"{dest} — {hit} notes, {len(dest.read_text(encoding='utf-8').split()):,} words")


if __name__ == "__main__":
    main()
