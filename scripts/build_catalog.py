#!/usr/bin/env python3
"""
Generate 09_SOURCE_CATALOG.md mechanically from the per-video note frontmatter.

Building the catalog from notes/ rather than by hand makes it complete by
construction: every ingested video appears exactly once, and no video can be
cited in the package that was not actually processed.

Reads  notes/<id>.md            (YAML frontmatter)
       source_transcripts/manifest.json
Writes restorative_vitality_knowledge/09_SOURCE_CATALOG.md
"""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
MANIFEST = ROOT / "source_transcripts" / "manifest.json"
OUT = ROOT / "restorative_vitality_knowledge" / "09_SOURCE_CATALOG.md"

FIELDS = ("subjects", "systems", "practices", "concepts")


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: missing YAML frontmatter")
    _, fm, _ = text.split("---", 2)
    data = yaml.safe_load(fm)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: frontmatter is not a mapping")
    return data


def as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value]


def bullets(items):
    return ", ".join(items) if items else "none recorded"


def main():
    if not NOTES.exists() or not any(NOTES.glob("*.md")):
        sys.exit("No notes found — run the extraction pass first.")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {v["id"]: v for v in manifest["videos"]}

    entries = []
    problems = []
    for note in sorted(NOTES.glob("*.md")):
        fm = parse_frontmatter(note)
        vid = fm.get("id")
        if vid not in by_id:
            problems.append(f"{note.name}: id '{vid}' is not in the manifest")
            continue
        meta = by_id[vid]
        entries.append({
            "id": vid,
            "title": meta["title"],
            "url": meta["url"],
            "upload_date": meta["upload_date"],
            "duration": meta["duration"],
            "source_file": f"source_transcripts/clean/{vid}.txt",
            **{f: as_list(fm.get(f)) for f in FIELDS},
        })

    if problems:
        sys.exit("Catalog build failed:\n  " + "\n  ".join(problems))

    entries.sort(key=lambda e: e["title"].lower())

    lines = [
        "# 09 — Source Catalog",
        "",
        "Every transcript ingested into this knowledge package, with the subjects, "
        "body systems, practices, and concepts each one covers.",
        "",
        f"**Channel:** The Feynman Way — https://www.youtube.com/@The_Feynman_Way  ",
        f"**Videos catalogued:** {len(entries)}",
        "",
        "Entries are alphabetical by title. Use the video ID to trace any claim in the "
        "other files back to its source.",
        "",
        "---",
        "",
    ]

    for i, e in enumerate(entries, 1):
        lines += [
            f"## {i}. {e['title']}",
            "",
            f"- **Video ID:** `{e['id']}`",
            f"- **URL:** {e['url']}",
            f"- **Upload date:** {e['upload_date']}",
            f"- **Duration:** {e['duration']}",
            f"- **Source file:** `{e['source_file']}`",
            f"- **Main subjects:** {bullets(e['subjects'])}",
            f"- **Body systems:** {bullets(e['systems'])}",
            f"- **Recommended practices:** {bullets(e['practices'])}",
            f"- **Important concepts:** {bullets(e['concepts'])}",
            "",
        ]

    # Reverse index: system -> videos, so the GPT can find sources by system.
    lines += ["---", "", "## Index by body system", ""]
    index = {}
    for e in entries:
        for s in e["systems"]:
            index.setdefault(s.strip().lower(), []).append(e)
    for system in sorted(index):
        titles = ", ".join(f"{v['title']} (`{v['id']}`)" for v in index[system])
        lines += [f"**{system}** — {titles}", ""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} — {len(entries)} entries, {len(index)} systems indexed.")


if __name__ == "__main__":
    main()
