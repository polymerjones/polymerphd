#!/usr/bin/env python3
"""Slice a named section out of every note into one staging file.

The notes share six universal section headings (Central claim, Glossary terms
introduced, Symptoms and body signals addressed, Analogies worth reusing,
Source-stated confidence, Conflicts with other sources). Slicing them lets the
reduce phase read one dimension across all 58 videos without loading every note
in full. Nothing is rewritten here -- text is copied verbatim, with the video id
and title attached so every line stays traceable.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "scratch_sections"

TARGET = sys.argv[1]


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


def section(text, heading):
    pat = re.compile(r"^## " + re.escape(heading) + r"\s*$", re.M)
    m = pat.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return (rest[: nxt.start()] if nxt else rest).strip()


def main():
    OUT.mkdir(exist_ok=True)
    slug = re.sub(r"\W+", "_", TARGET.lower()).strip("_")
    chunks = []
    missing = []
    for path in sorted(NOTES.glob("*.md")):
        fm, body = parse(path)
        sec = section(body, TARGET)
        if sec is None:
            missing.append(path.stem)
            continue
        chunks.append(
            f"### {fm.get('title', path.stem)}\n"
            f"`{fm.get('id', path.stem)}` · {fm.get('upload_date', 'not available')}\n\n{sec}\n"
        )
    dest = OUT / f"{slug}.md"
    dest.write_text(
        f"# Section slice: {TARGET}\n\nFrom {len(chunks)} of {len(list(NOTES.glob('*.md')))} notes.\n\n"
        + "\n---\n\n".join(chunks)
        + "\n",
        encoding="utf-8",
    )
    words = len(dest.read_text(encoding="utf-8").split())
    print(f"{dest} — {len(chunks)} notes, {words:,} words" + (f", missing: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
