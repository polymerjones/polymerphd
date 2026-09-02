#!/usr/bin/env python3
"""Build a combined multi-library Custom GPT knowledge bundle.

Concatenates each library's numbered knowledge files (00-08, minus the glossary)
into <slug>_KNOWLEDGE.md, its topic_reference_*.md files into <slug>_TOPIC_REFERENCE.md,
and folds every library's glossary and source catalog into one shared
COMBINED_GLOSSARY.md / COMBINED_SOURCE_CATALOG.md, each section verbatim under a
per-file or per-library heading. No content is rewritten -- this only merges file
boundaries, so it can't introduce a claim that wasn't already in a note-derived file.

A library with no numbered knowledge files or no topic_reference files yet (still
mid-synthesis) simply doesn't get that output file -- no empty files are written.

Usage: python3 scripts/build_custom_gpt_bundle.py <slug> [<slug> ...] [--out DIR]
"""
import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARIES_DIR = REPO_ROOT / "libraries"

# Numbered knowledge files 00-08 fold into <slug>_KNOWLEDGE.md (in filename order).
# 07 (glossary) is pulled out separately into the combined glossary.
# 09 (catalog) and 10 (GPT instructions) are handled separately too.
KNOWLEDGE_NUMBERS = range(0, 9)


def load_title(slug):
    data = json.loads((LIBRARIES_DIR / slug / "library.json").read_text())
    return data.get("title", slug)


def numbered_knowledge_files(knowledge_dir):
    files = []
    for path in sorted(knowledge_dir.glob("*.md")):
        m = re.match(r"^(\d{2})_", path.name)
        if m and int(m.group(1)) in KNOWLEDGE_NUMBERS and not path.name.startswith("07_"):
            files.append(path)
    return files


def topic_reference_files(knowledge_dir):
    return sorted(knowledge_dir.glob("topic_reference_*.md"))


def concat_with_headers(files, title):
    parts = [f"## From {f.name}\n\n{f.read_text().rstrip()}\n" for f in files]
    return f"# {title}\n\n" + "\n---\n\n".join(parts) + "\n"


def write_if_nonempty(path, files, title):
    if not files:
        return None
    path.write_text(concat_with_headers(files, title))
    return path


def collect_shared_section(sections, title, knowledge_dir, filename):
    f = knowledge_dir / filename
    if f.exists() and f.read_text().strip():
        sections.append(f"## {title}\n\n{f.read_text().rstrip()}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="+", help="library slugs under libraries/")
    parser.add_argument("--out", default="custom_gpt_combined", help="output directory (relative to repo root)")
    args = parser.parse_args()

    out_dir = REPO_ROOT / args.out
    out_dir.mkdir(exist_ok=True)

    glossary_sections = []
    catalog_sections = []
    built = []

    for slug in args.slugs:
        knowledge_dir = LIBRARIES_DIR / slug / "knowledge"
        title = load_title(slug)

        out_path = write_if_nonempty(
            out_dir / f"{slug}_KNOWLEDGE.md", numbered_knowledge_files(knowledge_dir), title
        )
        if out_path:
            built.append(out_path.name)

        out_path = write_if_nonempty(
            out_dir / f"{slug}_TOPIC_REFERENCE.md", topic_reference_files(knowledge_dir), title
        )
        if out_path:
            built.append(out_path.name)

        collect_shared_section(glossary_sections, title, knowledge_dir, "07_PLAIN_ENGLISH_GLOSSARY.md")
        collect_shared_section(catalog_sections, title, knowledge_dir, "09_SOURCE_CATALOG.md")

    if glossary_sections:
        (out_dir / "COMBINED_GLOSSARY.md").write_text(
            "# Combined Glossary\n\n" + "\n---\n\n".join(glossary_sections)
        )
        built.append("COMBINED_GLOSSARY.md")

    if catalog_sections:
        (out_dir / "COMBINED_SOURCE_CATALOG.md").write_text(
            "# Combined Source Catalog\n\n" + "\n---\n\n".join(catalog_sections)
        )
        built.append("COMBINED_SOURCE_CATALOG.md")

    print(f"Wrote {len(built)} files to {out_dir}/:")
    for name in built:
        print(f"  {name}")


if __name__ == "__main__":
    main()
