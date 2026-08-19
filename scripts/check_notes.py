#!/usr/bin/env python3
"""Validate notes against the schema and the corpus's provenance rules.

The build scripts already refuse to write on a malformed note. This runs the
same class of checks earlier and adds the one that matters most to this
project: every [mm:ss] anchor must actually exist in the transcript it claims
to cite. A plausible-looking timestamp that no transcript contains is a
fabricated citation, which is the one failure the package cannot absorb.

Checks, per note:
  - the six universal sections are present
  - the four frontmatter facets are present
  - every declared system is in the controlled vocabulary
  - no timestamp runs past the end of its video
  - every timestamp appears verbatim in source_transcripts/clean/<id>.txt
  - every cross-referenced video id has a note, or was deliberately deferred

Usage:
  python3 scripts/check_notes.py              # all notes
  python3 scripts/check_notes.py KTwE1rj8-Ek  # one or more ids
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UNIVERSAL = [
    "Central claim",
    "Symptoms and body signals addressed",
    "Glossary terms introduced",
    "Analogies worth reusing",
    "Source-stated confidence",
    "Conflicts with other sources",
]
FACETS = ["subjects", "systems", "practices", "concepts"]


def load_systems():
    """Controlled vocabulary, taken from the built dataset when available."""
    data = ROOT / "app" / "data.json"
    if data.exists():
        return set(json.loads(data.read_text(encoding="utf-8"))["vocab"]["systems"])
    # Fall back to whatever the notes themselves already agree on.
    seen = set()
    for note in (ROOT / "notes").glob("*.md"):
        fm = note.read_text(encoding="utf-8").split("---")[1]
        if "systems:" in fm:
            block = fm.split("systems:")[1].split("practices:")[0]
            seen.update(re.findall(r"^  - (.+)$", block, re.M))
    return seen


def check(path, manifest, note_ids, systems, deferred):
    vid = path.stem
    text = path.read_text(encoding="utf-8")
    problems = []

    headings = [l[3:].strip() for l in text.splitlines() if l.startswith("## ")]
    for section in UNIVERSAL:
        if section not in headings:
            problems.append(f"missing section: {section}")

    parts = text.split("---")
    fm = parts[1] if len(parts) > 2 else ""
    for facet in FACETS:
        if f"{facet}:" not in fm:
            problems.append(f"missing frontmatter facet: {facet}")

    if "systems:" in fm and "practices:" in fm:
        block = fm.split("systems:")[1].split("practices:")[0]
        for s in re.findall(r"^  - (.+)$", block, re.M):
            if s not in systems:
                problems.append(f"system off-vocabulary: {s}")

    stamps = set(re.findall(r"\[(\d{2}):(\d{2})\]", text))

    entry = manifest.get(vid)
    if entry is None:
        problems.append("id not present in manifest.json")
    else:
        limit = entry.get("duration_seconds") or 0
        for m, s in sorted(stamps):
            if int(m) * 60 + int(s) > limit:
                problems.append(f"timestamp past end of video: [{m}:{s}] (video is {entry['duration']})")

    transcript = ROOT / "source_transcripts" / "clean" / f"{vid}.txt"
    if not transcript.exists():
        problems.append("no cleaned transcript on disk")
    else:
        body = transcript.read_text(encoding="utf-8")
        for m, s in sorted(stamps):
            if f"[{m}:{s}]" not in body:
                problems.append(f"timestamp not in transcript: [{m}:{s}]")

    for ref in sorted(set(re.findall(r"`([A-Za-z0-9_-]{11})`", text)) - {vid}):
        # A deferred video is a legitimate reference: it was fetched and read,
        # then set aside as physics-framed rather than written up.
        if ref not in note_ids and ref not in deferred:
            problems.append(f"cross-reference has no note: {ref}")

    return problems


def main():
    manifest = {v["id"]: v for v in
                json.loads((ROOT / "source_transcripts" / "manifest.json")
                           .read_text(encoding="utf-8"))["videos"]}
    note_ids = {p.stem for p in (ROOT / "notes").glob("*.md")}
    systems = load_systems()

    deferred_file = ROOT / "scripts" / "deferred_videos.txt"
    deferred = set(re.findall(r"[A-Za-z0-9_-]{11}",
                              deferred_file.read_text(encoding="utf-8"))) \
        if deferred_file.exists() else set()

    wanted = sys.argv[1:]
    paths = ([ROOT / "notes" / f"{v}.md" for v in wanted] if wanted
             else sorted((ROOT / "notes").glob("*.md")))

    failed = 0
    for path in paths:
        if not path.exists():
            print(f"FAIL {path.stem}\n  - no such note")
            failed += 1
            continue
        problems = check(path, manifest, note_ids, systems, deferred)
        if problems:
            failed += 1
            print(f"FAIL {path.stem}")
            for p in problems:
                print(f"  - {p}")

    print(f"\n{len(paths) - failed}/{len(paths)} notes pass.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
