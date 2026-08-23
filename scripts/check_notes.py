#!/usr/bin/env python3
"""Validate a library's notes against its schema and provenance rules.

The build scripts already refuse to write on a malformed note. This runs the
same class of checks earlier and adds the one that matters most to this
project: every anchor (a video timestamp, a PDF page, a paragraph number —
whatever kind the cited source uses) must actually exist in that source's own
cleaned text. A plausible-looking anchor that no source contains is a
fabricated citation, which is the one failure the package cannot absorb.

Checks, per note:
  - the library's universal sections are present
  - the library's frontmatter facets are present
  - every declared controlled-vocabulary value (e.g. systems) is on-list
  - every anchor (bare, or `source-id`[anchor] scoped to a different source)
    resolves to a real source, matches that source's own anchor kind, does
    not run past that source's bound, and appears verbatim in its clean text
  - every cross-referenced id has a note, is a known (not-yet-written) source
    in the manifest, or was deliberately deferred

There is also an advisory pass, --terms, which reports glossary terms whose
wording does not appear in the transcript that introduced them. It is advisory
rather than a failure because auto-captions garble technical vocabulary (one
note's "otoconia" is transcribed "odonia"), so a flag means "read this", not
"this is wrong". It does catch terminology imported from outside the source,
which is the thing worth catching.

Usage:
  python3 scripts/check_notes.py <slug>              # all notes in that library
  python3 scripts/check_notes.py <slug> KTwE1rj8-Ek  # one or more ids
  python3 scripts/check_notes.py <slug> --terms       # advisory terminology review
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import require_slug, find_anchor_citations, BACKTICK_ID_RE  # noqa: E402

STOPWORDS = {"the", "and", "of", "a", "an", "as", "in", "to", "for", "its", "that",
             "own", "one", "with", "or", "at", "by", "from", "into", "on", "is", "it"}


def anglicise(text):
    """Fold the notes' British spelling onto the captions' American spelling."""
    text = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    text = re.sub(r"\b(\w+?)re\b", r"\1er", text)
    text = re.sub(r"\b(\w+?)isation\b", r"\1ization", text)
    text = re.sub(r"\b(\w+?)ise\b", r"\1ize", text)
    return " " + re.sub(r"\s+", " ", text) + " "


def term_roots(word):
    """Crude stems, enough to match thixotropy against thixotropic."""
    roots = {word}
    for suffix in ("ies", "es", "s", "y", "ic", "al"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            roots.add(word[: -len(suffix)])
    return roots


def review_terms(lib, paths):
    """Advisory: glossary terms whose wording is absent from their source text."""
    flagged = checked = 0
    for path in paths:
        transcript = lib.clean_dir / f"{path.stem}.txt"
        if not path.exists() or not transcript.exists():
            continue
        body = anglicise(transcript.read_text(encoding="utf-8"))
        text = path.read_text(encoding="utf-8")
        if "## Glossary terms introduced" not in text:
            continue
        section = text.split("## Glossary terms introduced")[1].split("\n## ")[0]
        for m in re.finditer(r"^- \*\*(.+?)\*\*", section, re.M):
            checked += 1
            words = [w for w in anglicise(m.group(1).split("(")[0]).split()
                     if w not in STOPWORDS and len(w) > 3]
            if not words:
                continue
            if not any(any(r in body for r in term_roots(w)) for w in words):
                flagged += 1
                print(f"  {path.stem}  {m.group(1)}")
    print(f"\n{checked} glossary terms reviewed, {flagged} not found in their source text.")
    print("Most are auto-caption garbling. Any that are not are terminology "
          "imported from outside the source.")
    return 0


def check(path, lib, note_ids, sources, deferred):
    vid = path.stem
    text = path.read_text(encoding="utf-8")
    problems = []

    headings = [l[3:].strip() for l in text.splitlines() if l.startswith("## ")]
    for section in lib.universal_sections:
        if section not in headings:
            problems.append(f"missing section: {section}")

    parts = text.split("---")
    fm = parts[1] if len(parts) > 2 else ""
    for facet in lib.facets:
        if f"{facet}:" not in fm:
            problems.append(f"missing frontmatter facet: {facet}")

    for facet, allowed in lib.controlled_facets.items():
        if f"{facet}:" not in fm:
            continue
        block = fm.split(f"{facet}:", 1)[1]
        next_key = re.search(r"\n[A-Za-z_]+:", block)
        if next_key:
            block = block[: next_key.start()]
        for v in re.findall(r"^  - (.+)$", block, re.M):
            if v not in allowed:
                problems.append(f"{facet} off-vocabulary: {v}")

    if vid not in sources:
        problems.append("id not present in manifest.json")

    missing_body_reported = set()
    for source_id, kind, value, literal in find_anchor_citations(text, vid):
        entry = sources.get(source_id)
        if entry is None:
            problems.append(f"anchor cites unknown source `{source_id}`: {literal}")
            continue

        anchor_cfg = entry.get("anchor", {})
        expected_kind = anchor_cfg.get("kind")
        if expected_kind and expected_kind != kind:
            problems.append(
                f"anchor kind mismatch for `{source_id}`: {literal} looks like "
                f"{kind}, but that source is anchored by {expected_kind}"
            )
            continue

        bound = anchor_cfg.get("bound")
        if bound is not None and value > bound:
            problems.append(f"anchor past end of source `{source_id}`: {literal} (bound is {bound})")

        clean_file = entry.get("clean_file")
        body = None
        if clean_file:
            clean_path = lib.sources_dir / clean_file
            if clean_path.exists():
                body = clean_path.read_text(encoding="utf-8")
        if body is None:
            if source_id not in missing_body_reported:
                problems.append(f"no cleaned source text on disk for `{source_id}`")
                missing_body_reported.add(source_id)
        elif literal not in body:
            problems.append(f"anchor not in source text for `{source_id}`: {literal}")

    for ref in sorted(set(BACKTICK_ID_RE.findall(text)) - {vid}):
        if ref not in note_ids and ref not in deferred and ref not in sources:
            problems.append(f"cross-reference has no note and is not a known source: {ref}")

    return problems


def main():
    lib, rest = require_slug(
        sys.argv[1:],
        "Usage: python3 scripts/check_notes.py <slug> [id...] [--terms]",
    )

    sources = lib.sources_by_id()
    note_ids = {p.stem for p in lib.notes.glob("*.md")}
    deferred = lib.deferred_ids()

    terms_only = "--terms" in rest
    wanted = [a for a in rest if not a.startswith("--")]
    paths = ([lib.notes / f"{v}.md" for v in wanted] if wanted
             else sorted(lib.notes.glob("*.md")))

    if terms_only:
        return review_terms(lib, paths)

    failed = 0
    for path in paths:
        if not path.exists():
            print(f"FAIL {path.stem}\n  - no such note")
            failed += 1
            continue
        problems = check(path, lib, note_ids, sources, deferred)
        if problems:
            failed += 1
            print(f"FAIL {path.stem}")
            for p in problems:
                print(f"  - {p}")

    print(f"\n{len(paths) - failed}/{len(paths)} notes pass.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
