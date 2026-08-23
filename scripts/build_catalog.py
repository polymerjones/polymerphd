#!/usr/bin/env python3
"""
Generate a library's source catalog mechanically from its per-source note frontmatter.

Building the catalog from notes/ rather than by hand makes it complete by
construction: every ingested source appears exactly once, and no source can be
cited in the package that was not actually processed.

Reads  libraries/<slug>/notes/<id>.md            (YAML frontmatter)
       libraries/<slug>/sources/manifest.json
Writes libraries/<slug>/knowledge/<catalog_file>  (library.json's catalog_file, default 09_SOURCE_CATALOG.md)

Usage:
  python3 scripts/build_catalog.py <slug>
"""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import require_slug  # noqa: E402


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


def catalog_heading(catalog_file):
    stem = catalog_file.rsplit(".", 1)[0]
    if "_" in stem:
        num, rest = stem.split("_", 1)
        return f"# {num} — {rest.replace('_', ' ').title()}"
    return f"# {stem.replace('_', ' ').title()}"


def attribution_line(lib):
    attr = lib.config.get("attribution")
    if not attr:
        return None
    name, url = attr.get("name"), attr.get("url")
    label = "Channel" if attr.get("style") == "youtube_channel" else "Source"
    if name and url:
        return f"**{label}:** {name} — {url}  "
    if name:
        return f"**{label}:** {name}  "
    return None


def main():
    lib, _ = require_slug(sys.argv[1:], "Usage: python3 scripts/build_catalog.py <slug>")
    fields = lib.facets
    facet_labels = lib.config.get("facet_labels", {})
    unit_label = lib.config.get("catalog_unit_label", "Sources")
    id_label = lib.config.get("catalog_id_label", "Source ID")

    if not lib.notes.exists() or not any(lib.notes.glob("*.md")):
        sys.exit(f"No notes found in {lib.notes} — run the extraction pass first.")

    by_id = lib.sources_by_id()

    entries = []
    problems = []
    for note in sorted(lib.notes.glob("*.md")):
        fm = parse_frontmatter(note)
        vid = fm.get("id")
        if vid not in by_id:
            problems.append(f"{note.name}: id '{vid}' is not in the manifest")
            continue
        meta = by_id[vid]
        entries.append({
            "id": vid,
            "title": meta["title"],
            "url": meta.get("url"),
            "author": meta.get("author"),
            "upload_date": meta.get("upload_date"),
            "duration": meta.get("duration"),
            "source_file": f"sources/{meta.get('clean_file', f'clean/{vid}.txt')}",
            **{f: as_list(fm.get(f)) for f in fields},
        })

    if problems:
        sys.exit("Catalog build failed:\n  " + "\n  ".join(problems))

    entries.sort(key=lambda e: e["title"].lower())

    default_description = (
        "Every source ingested into this knowledge package, with the "
        + ", ".join(facet_labels.get(f, f) for f in fields[:-1])
        + f", and {facet_labels.get(fields[-1], fields[-1])} each one covers."
    ) if fields else "Every source ingested into this knowledge package."

    lines = [
        catalog_heading(lib.catalog_file),
        "",
        lib.config.get("catalog_description", default_description),
        "",
    ]
    attr_line = attribution_line(lib)
    if attr_line:
        lines.append(attr_line)
    lines += [
        f"**{unit_label} catalogued:** {len(entries)}",
        "",
        f"Entries are alphabetical by title. Use the {id_label[0].lower() + id_label[1:]} to "
        "trace any claim in the other files back to its source.",
        "",
        "---",
        "",
    ]

    for i, e in enumerate(entries, 1):
        lines += [f"## {i}. {e['title']}", "", f"- **{id_label}:** `{e['id']}`"]
        if e.get("url"):
            lines.append(f"- **URL:** {e['url']}")
        if e.get("author"):
            lines.append(f"- **Author:** {e['author']}")
        if e.get("upload_date"):
            lines.append(f"- **Upload date:** {e['upload_date']}")
        if e.get("duration"):
            lines.append(f"- **Duration:** {e['duration']}")
        lines.append(f"- **Source file:** `{e['source_file']}`")
        for f in fields:
            lines.append(f"- **{facet_labels.get(f, f.capitalize())}:** {bullets(e[f])}")
        lines.append("")

    # Reverse index: systems (or the library's second facet) -> sources.
    index_facet = "systems" if "systems" in fields else (fields[1] if len(fields) > 1 else fields[0])
    index_label = facet_labels.get(index_facet, index_facet).lower()
    lines += ["---", "", f"## Index by {index_label}", ""]
    index = {}
    for e in entries:
        for s in e[index_facet]:
            index.setdefault(s.strip().lower(), []).append(e)
    for key in sorted(index):
        titles = ", ".join(f"{v['title']} (`{v['id']}`)" for v in index[key])
        lines += [f"**{key}** — {titles}", ""]

    out = lib.knowledge / lib.catalog_file
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} — {len(entries)} entries, {len(index)} {index_label} indexed.")


if __name__ == "__main__":
    main()
