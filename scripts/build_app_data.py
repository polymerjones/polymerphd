#!/usr/bin/env python3
"""
Build the offline reference app shell from every library's notes and knowledge files.

Reads, per library under libraries/<slug>/:
        notes/<id>.md          (YAML frontmatter + universal sections)
        knowledge/*.md          (the synthesised knowledge files)
        sources/manifest.json   (authoritative source metadata)
        overrides.json          (hand corrections for derived facets)

Writes  app/data/<slug>.json  each library's dataset on its own, for any later consumer
        app/index.html        one self-contained app: a library picker plus every
                               library's data inlined as its own gzip+base64 blob,
                               lazily inflated client-side the first time that
                               library is actually entered

Every library's data stays inlined in this one file rather than fetched at
runtime, so the app keeps making zero network requests and works fully offline
on both GitHub Pages and the iOS WKWebView wrapper — see CLAUDE.md.

Nothing outside app/ is written. The source material is read, never modified.

Determinism matters here: the output is regenerated whenever notes are added, so
every collection is sorted and json is dumped with sorted keys. Re-running without
changing an input must produce a byte-identical file.

Usage:
  python3 scripts/build_app_data.py
"""

import base64
import gzip
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# parse_frontmatter/as_list already solve the frontmatter shape (string-or-list
# facets included). build_catalog guards its entry point, so importing is safe.
# slice_sections is NOT importable -- it reads sys.argv at module level -- so its
# section splitter is reimplemented below against the same heading convention.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_catalog import parse_frontmatter, as_list  # noqa: E402
from lib_common import all_library_slugs, load_library, find_anchor_citations  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
TEMPLATE = APP / "app.template.html"
OUT_HTML = APP / "index.html"
DATA_DIR = APP / "data"
SOUND = APP / "sound.b64"


def strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def split_sections(text, level="## "):
    """Split a markdown body into {heading: body} at one heading level.

    Same contract as slice_sections.section(), but returns every section in one
    pass instead of re-scanning per heading.
    """
    out = {}
    pat = re.compile(r"^" + re.escape(level) + r"(.+?)\s*$", re.M)
    marks = list(pat.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[m.group(1).strip()] = text[m.end():end].strip()
    return out


def bullets(text):
    """Top-level bullet lines, with their wrapped continuation lines folded in."""
    out = []
    for line in (text or "").splitlines():
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            out.append(m.group(1).strip())
        elif out and line.strip() and line.startswith((" ", "\t")):
            out[-1] += " " + line.strip()
    return out


# ---------------------------------------------------------------------------
# Derived practice facets
#
# These are pattern-matched out of free text and are therefore PARTIAL. Roughly
# 15% of practice strings state a readable duration, 7% a seated/supported cue.
# Two things keep that honest: anything unclassified is reported for hand
# correction in overrides.json, and the raw source string always rides on the
# card, so a filter can never hide what the material actually said.
#
# Gated by library.json's "derived_practice_facets" (default off): this pattern
# set is tuned for restorative-physiology's practice-instruction prose and isn't
# assumed to fit every library's content.
# ---------------------------------------------------------------------------

UNIT_SECONDS = {"second": 1, "sec": 1, "minute": 60, "min": 60, "hour": 3600}

# "2 to 10 minutes", "15-20 minutes", "60 in 60 seconds", "five minutes"
DURATION_RE = re.compile(
    r"(\d+)\s*(?:(?:to|-|–|or)\s*\d+\s*)?(second|sec|minute|min|hour)s?\b", re.I
)
WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "fifteen": 15, "twenty": 20, "thirty": 30,
}
WORD_DURATION_RE = re.compile(
    r"\b(" + "|".join(WORD_NUMBERS) + r")\s+(second|minute|hour)s?\b", re.I
)

POSITION_PATTERNS = [
    ("seated", r"\b(seated|sitting|chair|desk|sit-to-stand|chair sits?)\b"),
    ("lying", r"\b(lying|lie|bed|supine|prone|flat on|body pillow)\b"),
    ("supported", r"\b(wall|counter|handrail|banister|doorway|hold(?:ing)? on)\b"),
    ("standing", r"\b(standing|stand|walk(?:ing)?|bounce|bouncing|heel drops?|stairs?)\b"),
]

# Anything naming a specific object is equipment. Deliberately narrow: the cost of
# a false "no equipment" is a user planning around gear they do not have.
EQUIPMENT_RE = re.compile(
    r"\b(trampoline|rebounder|weight|dumbbell|kettlebell|band|blanket|pillow|"
    r"tennis ball|foam roller|mat|bar\b|pull-?up|treadmill|bike|sauna|bath|"
    r"shower|light box|lamp|glasses|monitor|supplement|protein powder|"
    r"oximeter|monitor|scale|tracker)\b",
    re.I,
)
NO_EQUIPMENT_RE = re.compile(r"\b(no equipment|bodyweight|barefoot|hands? only)\b", re.I)


def derive_duration(text):
    """Shortest stated duration in seconds, or None. Ranges take the low end, so
    a '2 to 10 minutes' practice answers a 'what fits in 5 minutes' question."""
    best = None
    for value, unit in DURATION_RE.findall(text):
        secs = int(value) * UNIT_SECONDS[unit.lower()]
        best = secs if best is None else min(best, secs)
    for word, unit in WORD_DURATION_RE.findall(text):
        secs = WORD_NUMBERS[word.lower()] * UNIT_SECONDS[unit.lower()]
        best = secs if best is None else min(best, secs)
    return best


def derive_position(text):
    found = [name for name, pat in POSITION_PATTERNS if re.search(pat, text, re.I)]
    return found or None


def derive_equipment(text):
    if NO_EQUIPMENT_RE.search(text):
        return "none"
    if EQUIPMENT_RE.search(text):
        return "required"
    return None


def duration_bucket(secs):
    if secs is None:
        return None
    if secs <= 60:
        return "under-1-min"
    if secs <= 300:
        return "under-5-min"
    if secs <= 900:
        return "under-15-min"
    return "over-15-min"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def display_fields(entry):
    """Kind-agnostic display fields for a source: a short extent string
    (duration for video, page/paragraph count for text sources), a date,
    and a URL (or None if the source isn't meaningfully linkable)."""
    kind = entry.get("kind", "youtube")
    anchor_kind = entry.get("anchor", {}).get("kind")
    bound = entry.get("anchor", {}).get("bound")
    if kind == "youtube":
        extent = entry.get("duration") or "not available"
    elif anchor_kind == "page" and bound is not None:
        extent = f"{bound} page{'s' if bound != 1 else ''}"
    elif anchor_kind == "paragraph" and bound is not None:
        extent = f"{bound} paragraph{'s' if bound != 1 else ''}"
    else:
        extent = entry.get("duration") or "not available"
    date = entry.get("upload_date") or entry.get("retrieved_date") or "not available"
    return extent, date, entry.get("url")


def load_notes(lib, by_id, problems):
    videos = []
    for path in sorted(lib.notes.glob("*.md")):
        fm = parse_frontmatter(path)
        vid = fm.get("id")
        if vid not in by_id:
            problems.append(f"{path.name}: id {vid!r} is not in the manifest")
            continue
        meta = by_id[vid]
        body = strip_frontmatter(path.read_text(encoding="utf-8"))
        sections = split_sections(body)

        missing = [h for h in lib.universal_sections if h not in sections]
        if missing:
            problems.append(f"{path.name}: missing section(s) {', '.join(missing)}")

        citations = find_anchor_citations(body, vid)
        for source_id, kind, value, literal in citations:
            entry = by_id.get(source_id)
            if entry is None:
                problems.append(f"{path.name}: anchor cites unknown source `{source_id}`: {literal}")
                continue
            bound = entry.get("anchor", {}).get("bound")
            if bound is not None and value > bound:
                problems.append(
                    f"{path.name}: anchor {literal} exceeds bound {bound} for `{source_id}`"
                )

        extent, date, url = display_fields(meta)
        videos.append({
            "id": vid,
            "kind": meta.get("kind", "youtube"),
            "evidence": meta.get("evidence"),
            "title": meta["title"],
            "url": url,
            "upload_date": date,
            "duration": extent,
            **{f: sorted(as_list(fm.get(f))) for f in lib.facets},
            "sections": [{"heading": h, "body": b} for h, b in sections.items()],
            "anchors": len(citations),
        })
    return videos


def load_knowledge_files(lib, by_id, problems):
    """The knowledge files, split by heading so the app can deep-link a section."""
    files = []
    for path in sorted(lib.knowledge.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^#\s+(.+?)\s*$", text, re.M)
        title = m.group(1) if m else path.stem
        groups = split_sections(text, "# ")
        sections = []
        for gh, gbody in groups.items():
            subs = split_sections(gbody, "## ")
            intro = gbody[: min([gbody.find("## " + s) for s in subs], default=len(gbody))] \
                if subs else gbody
            sections.append({"heading": gh, "intro": intro.strip(),
                             "subsections": [{"heading": sh, "body": sb}
                                             for sh, sb in subs.items()]})
        # topic_reference-style files cite source ids; numbered synthesis files do not.
        # Filtered against the manifest so a backtick-quoted filename (`09_SOURCE_CATALOG.md`)
        # or other stray backtick text is never mistaken for a source citation.
        backticked = set(re.findall(r"`([^`]+)`", text))
        cited = sorted(backticked & by_id.keys())
        files.append({
            "slug": path.stem,
            "title": title,
            "sections": sections,
            "cited_ids": cited,
            "words": len(text.split()),
        })
    if not files:
        problems.append("no knowledge files found")
    return files


def load_glossary(lib, problems):
    """Terms from the library's glossary file, formatted '**Term** — definition'."""
    filename = lib.glossary_file
    if not filename:
        return []
    path = lib.knowledge / filename
    if not path.exists():
        problems.append(f"{filename} is missing")
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$", line.strip())
        if m:
            entries.append({"term": m.group(1).strip(), "definition": m.group(2).strip()})
    return sorted(entries, key=lambda e: e["term"].lower())


def load_curated_symptoms(lib, problems):
    """The curated entries in the library's curated-facts file, if it has one."""
    filename = lib.curated_facts_file
    if not filename:
        return []
    path = lib.knowledge / filename
    if not path.exists():
        problems.append(f"{filename} is missing")
        return []
    text = path.read_text(encoding="utf-8")
    curated = []
    for group, gbody in split_sections(text, "# ").items():
        for heading, body in split_sections(gbody, "## ").items():
            curated.append({"group": group, "heading": heading, "body": body.strip()})
    return curated


# ---------------------------------------------------------------------------
# Indexes
# ---------------------------------------------------------------------------

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "with",
    "that", "this", "it", "its", "is", "are", "was", "were", "be", "been", "after",
    "before", "from", "by", "as", "no", "not", "other", "than", "then", "more",
    "most", "own", "up", "out", "off", "over", "under", "when", "what", "which",
}


def tokens(text):
    words = re.findall(r"[a-z]+", text.lower())
    return {w.rstrip("s") if len(w) > 4 else w for w in words if w not in STOPWORDS}


def match_curated(bullet, curated_tokens):
    """Attach a bullet to a curated entry by token overlap.

    Heuristic, and labelled as such in the UI. The threshold is deliberately
    strict: a wrong match would attribute a mechanism to a symptom the source
    never linked, which is exactly the failure this package exists to avoid.
    """
    btoks = tokens(bullet)
    best, best_score = None, 0.0
    for idx, ctoks in curated_tokens:
        if not ctoks:
            continue
        overlap = btoks & ctoks
        score = len(overlap) / len(ctoks)
        if score > best_score and any(len(w) > 4 for w in overlap):
            best, best_score = idx, score
    return best if best_score >= 0.6 else None


def build_symptoms(videos, curated):
    curated_tokens = [(i, tokens(c["heading"])) for i, c in enumerate(curated)]
    entries = []
    for v in videos:
        sec = next((s["body"] for s in v["sections"]
                    if s["heading"] == "Symptoms and body signals addressed"), "")
        for b in bullets(sec):
            entries.append({
                "raw": b,
                "video_id": v["id"],
                "seconds": [val for _, kind, val, _ in find_anchor_citations(b, v["id"])
                            if kind == "timestamp"],
                "curated": match_curated(b, curated_tokens),
            })
    return entries


def build_practices(videos, overrides, derive_facets):
    """One card per frontmatter practice string, enriched from the note body."""
    cards = []
    unclassified = []
    for v in videos:
        for text in v.get("practices", []):
            if text.strip().lower() in {"none recorded", "none"}:
                continue
            key = f"{v['id']}::{text}"
            o = overrides.get(key, {})
            secs = o.get("duration_seconds", derive_duration(text) if derive_facets else None)
            position = o.get("position", derive_position(text) if derive_facets else None)
            equipment = o.get("equipment", derive_equipment(text) if derive_facets else None)
            if derive_facets and secs is None and not position and equipment is None:
                unclassified.append(key)
            cards.append({
                "key": key,
                "text": text,
                "video_id": v["id"],
                "duration_seconds": secs,
                "duration_bucket": duration_bucket(secs),
                "position": sorted(position) if position else [],
                "equipment": equipment,
                "overridden": key in overrides,
            })
    return cards, unclassified


def build_vocab(videos, facets):
    """Observed vocabularies with the video ids under each, so the UI's facet
    counts come from the data rather than being hardcoded."""
    vocab = {}
    for facet in facets:
        index = defaultdict(list)
        for v in videos:
            for term in v.get(facet, []):
                index[term].append(v["id"])
        vocab[facet] = {k: sorted(set(ids)) for k, ids in sorted(index.items())}
    return vocab


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_one(lib):
    """Build one library's full data dict. Returns (data, problems, unclassified)."""
    problems = []
    by_id = lib.sources_by_id()
    overrides_path = lib.dir / "overrides.json"
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path.exists() else {}
    derive_facets = bool(lib.config.get("derived_practice_facets", False))

    videos = load_notes(lib, by_id, problems)
    library = load_knowledge_files(lib, by_id, problems)
    glossary = load_glossary(lib, problems)
    curated = load_curated_symptoms(lib, problems)
    symptoms = build_symptoms(videos, curated)
    practices, unclassified = build_practices(videos, overrides, derive_facets)
    vocab = build_vocab(videos, lib.facets)

    stats = {
        "videos": len(videos),
        "library_files": len(library),
        "glossary_terms": len(glossary),
        "symptoms": len(symptoms),
        "practices": len(practices),
        "anchors": sum(v["anchors"] for v in videos),
    }

    splash_path = lib.dir / lib.config.get("splash_file", "splash.b64")
    facet_labels = lib.config.get("facet_labels", {})
    meta = {
        "slug": lib.slug,
        "title": lib.config.get("title", lib.slug),
        "subtitle": lib.config.get("subtitle", ""),
        "lede": lib.config.get("lede", ""),
        "about_paragraphs": lib.config.get("about_paragraphs", []),
        "splash_b64": splash_path.read_text(encoding="utf-8").strip() if splash_path.exists() else "",
        "primary_facet": lib.primary_facet,
        "primary_facet_label": facet_labels.get(lib.primary_facet, lib.primary_facet.capitalize()),
        "facets": list(lib.facets),
        "facet_labels": {f: facet_labels.get(f, f.capitalize()) for f in lib.facets},
    }

    data = {
        "videos": videos,
        "library": library,
        "glossary": glossary,
        "curated_symptoms": curated,
        "symptoms": symptoms,
        "practices": practices,
        "vocab": vocab,
        "stats": stats,
        "meta": meta,
    }
    return data, problems, unclassified


def main():
    slugs = all_library_slugs()
    if not slugs:
        sys.exit("No libraries found under libraries/*/library.json — nothing to build.")

    APP.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    library_index = []
    blobs = {}
    total_payload_bytes = 0

    for slug in slugs:
        lib = load_library(slug)
        if not lib.notes.exists() or not any(lib.notes.glob("*.md")):
            sys.exit(f"No notes found in {lib.notes} — run the extraction pass first.")

        data, problems, unclassified = build_one(lib)
        if problems:
            print(f"\n{slug}: {len(problems)} validation problem(s) — nothing written:\n", file=sys.stderr)
            for p in problems[:40]:
                print(f"  - {p}", file=sys.stderr)
            if len(problems) > 40:
                print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
            sys.exit(1)

        payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        total_payload_bytes += len(payload)
        (DATA_DIR / f"{slug}.json").write_text(payload, encoding="utf-8")

        # mtime=0 keeps the gzip header byte-identical between runs.
        blob = gzip.compress(payload.encode("utf-8"), compresslevel=9, mtime=0)
        blobs[slug] = base64.b64encode(blob).decode("ascii")

        # The icon is pre-encoded (96px PNG, ~27 KB) rather than downscaled here, so
        # the build has no dependency on macOS sips.
        icon_path = lib.dir / lib.config.get("icon_file", "icon.b64")
        s = data["stats"]
        library_index.append({
            "slug": slug,
            "title": lib.config.get("title", slug),
            "subtitle": lib.config.get("subtitle", ""),
            "teaser": f"{s['videos']} sources",
            "sources": s["videos"],
            "anchors": s["anchors"],
            "icon_b64": icon_path.read_text(encoding="utf-8").strip() if icon_path.exists() else "",
        })

        if unclassified:
            report = APP / f"unclassified_practices_{slug}.txt"
            report.write_text("\n".join(sorted(unclassified)) + "\n", encoding="utf-8")

        matched = sum(1 for e in data["symptoms"] if e["curated"] is not None)
        classified = len(data["practices"]) - len(unclassified)
        print(
            f"{slug}: {s['videos']} notes · {s['library_files']} knowledge files · "
            f"{s['glossary_terms']} glossary terms\n"
            f"  {s['anchors']:,} anchors resolved\n"
            f"  {s['symptoms']:,} symptoms indexed ({matched} matched to a curated entry)\n"
            f"  {s['practices']} practice cards ({classified} carry at least one derived facet, "
            f"{len(unclassified)} unclassified)"
        )
        if unclassified:
            print(f"  → unclassified keys listed in app/unclassified_practices_{slug}.txt "
                  f"for correction in libraries/{slug}/overrides.json")

    if not TEMPLATE.exists():
        sys.exit(f"Missing {TEMPLATE} — cannot build the app shell.")
    html = TEMPLATE.read_text(encoding="utf-8")
    for placeholder in ("/*__LIBRARY_INDEX__*/", "/*__LIBRARIES__*/"):
        if placeholder not in html:
            sys.exit(f"Template has no {placeholder} placeholder.")

    html = html.replace("/*__LIBRARY_INDEX__*/",
                         json.dumps(library_index, ensure_ascii=False, sort_keys=True))
    html = html.replace("/*__LIBRARIES__*/",
                         json.dumps(blobs, ensure_ascii=False, sort_keys=True))

    # Shell-level branding (favicon/apple-touch-icon, and the About panel's
    # fallback splash on the picker screen) comes from the first library,
    # alphabetically, since there's no separate umbrella artwork yet.
    shell_lib = load_library(slugs[0])
    shell_icon = shell_lib.dir / shell_lib.config.get("icon_file", "icon.b64")
    shell_splash = shell_lib.dir / shell_lib.config.get("splash_file", "splash.b64")
    if shell_icon.exists():
        html = html.replace("__ICON__", shell_icon.read_text(encoding="utf-8").strip())
    if shell_splash.exists():
        html = html.replace("__SPLASH__", shell_splash.read_text(encoding="utf-8").strip())
    if SOUND.exists():
        # count=1: the template's sentinel check re-uses the literal "__SOUND__"
        # token as its own "no sound configured" placeholder (app.template.html),
        # so a blanket replace would clobber that comparison too and SOUND would
        # always come out null even with real audio data in the first slot.
        html = html.replace("__SOUND__", SOUND.read_text(encoding="utf-8").strip(), 1)

    OUT_HTML.write_text(html, encoding="utf-8")

    total_mb = total_payload_bytes / 1_048_576
    print(
        f"\nWrote {OUT_HTML.relative_to(ROOT)} — {len(slugs)} librar{'y' if len(slugs) == 1 else 'ies'}, "
        f"{total_mb:.2f} MB of data → {OUT_HTML.stat().st_size / 1_048_576:.2f} MB single-file app (gzipped)"
    )


if __name__ == "__main__":
    main()
