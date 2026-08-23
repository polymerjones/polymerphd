"""Shared helpers for library-scoped pipeline scripts.

Every content-pipeline script takes a library slug and resolves its paths
through here, instead of hardcoding `ROOT / "notes"` etc. — this is what lets
one set of scripts serve every library under libraries/*/ rather than
assuming a single fixed corpus. Safe to import: nothing here reads sys.argv.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARIES_DIR = ROOT / "libraries"


class Library:
    def __init__(self, slug):
        self.slug = slug
        self.dir = LIBRARIES_DIR / slug
        config_path = self.dir / "library.json"
        if not config_path.exists():
            raise SystemExit(
                f"No such library: {slug!r} (expected {config_path})\n"
                f"Known libraries: {', '.join(all_library_slugs()) or '(none found)'}"
            )
        self.config = json.loads(config_path.read_text(encoding="utf-8"))

    # -- directories --------------------------------------------------
    @property
    def notes(self):
        return self.dir / "notes"

    @property
    def knowledge(self):
        return self.dir / "knowledge"

    @property
    def sources_dir(self):
        return self.dir / "sources"

    @property
    def clean_dir(self):
        return self.sources_dir / "clean"

    @property
    def raw_dir(self):
        return self.sources_dir / "raw"

    @property
    def manifest_path(self):
        return self.sources_dir / "manifest.json"

    @property
    def deferred_path(self):
        return self.dir / "deferred_sources.txt"

    @property
    def ingest_state_dir(self):
        return self.dir / "ingest_state"

    # -- config-driven facts (with sane fallbacks) ---------------------
    @property
    def facets(self):
        return tuple(self.config.get("facets", ["subjects", "systems", "practices", "concepts"]))

    @property
    def universal_sections(self):
        return self.config.get("universal_sections", [])

    @property
    def controlled_facets(self):
        return self.config.get("controlled_facets", {})

    @property
    def glossary_file(self):
        return self.config.get("glossary_file")

    @property
    def curated_facts_file(self):
        return self.config.get("curated_facts_file")

    @property
    def catalog_file(self):
        return self.config.get("catalog_file", "09_SOURCE_CATALOG.md")

    # -- manifest -------------------------------------------------------
    def load_manifest(self):
        if not self.manifest_path.exists():
            return {"sources": []}
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def save_manifest(self, manifest):
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=False)
        self.manifest_path.write_text(payload + "\n", encoding="utf-8")

    def sources_by_id(self):
        return {s["id"]: s for s in self.load_manifest().get("sources", [])}

    def deferred_ids(self):
        if not self.deferred_path.exists():
            return set()
        return set(re.findall(r"[A-Za-z0-9_-]{6,}",
                               self.deferred_path.read_text(encoding="utf-8")))


def all_library_slugs():
    if not LIBRARIES_DIR.exists():
        return []
    return sorted(p.name for p in LIBRARIES_DIR.iterdir()
                  if p.is_dir() and (p / "library.json").exists())


def load_library(slug):
    return Library(slug)


def require_slug(argv, usage):
    """Pop and validate a library slug from the front of argv, or exit with usage."""
    if not argv or argv[0].startswith("-"):
        known = ", ".join(all_library_slugs()) or "(none found)"
        raise SystemExit(f"{usage}\nKnown libraries: {known}")
    slug, rest = argv[0], argv[1:]
    return load_library(slug), rest


# -- anchor kinds -------------------------------------------------------
# Per-source, not per-library: a single library (e.g. Dupuytren) can mix a
# timestamp-anchored video with a page-anchored PDF and a paragraph-anchored
# article side by side, so this table is keyed by anchor kind, not by slug.
ANCHOR_KINDS = {
    "timestamp": {
        "regex": re.compile(r"\[(\d{1,2}):(\d{2})(?::(\d{2}))?\]"),
        "to_seconds": lambda m: (int(m[0]) * 3600 + int(m[1]) * 60 + int(m[2]))
                                 if m[2] else (int(m[0]) * 60 + int(m[1])),
        "to_literal": lambda m: f"[{m[0]}:{m[1]}" + (f":{m[2]}]" if m[2] else "]"),
    },
    "page": {
        "regex": re.compile(r"\[p\.(\d+)\]"),
        "to_value": lambda m: int(m[0]),
        "to_literal": lambda m: f"[p.{m[0]}]",
    },
    "paragraph": {
        "regex": re.compile(r"\[¶(\d+)\]"),
        "to_value": lambda m: int(m[0]),
        "to_literal": lambda m: f"[¶{m[0]}]",
    },
}

# A bare backtick id NOT followed by an anchor keeps its original, narrow meaning
# ("related source, no anchor-level check") and its original shape: exactly an
# 11-char YouTube id. This deliberately does NOT match arbitrary prose like
# `09_SOURCE_CATALOG.md` or `topic_reference` that also happens to be backticked
# in a note's own commentary. A citation to a non-11-char source (PDF, website,
# ...) that DOES need validating uses the scoped anchor form below instead,
# which is checked by find_anchor_citations() regardless of id shape.
BACKTICK_ID_RE = re.compile(r"`([A-Za-z0-9_-]{11})`")
# Backtick cross-reference immediately followed by a bracket anchor:
# `other-source-id`[anchor] — cites a source other than the note's own. Any id
# shape is allowed here since the anchor makes the citation intent unambiguous.
SCOPED_PREFIX_RE = re.compile(r"`([A-Za-z0-9_.-]{2,64})`$")
ANY_ANCHOR_RE = re.compile(r"\[(?:\d{1,2}:\d{2}(?::\d{2})?|p\.\d+|¶\d+)\]")


def classify_anchor(literal):
    """Return (kind, value-in-source-units) for a bracketed anchor string, e.g.
    '[12:34]' -> ('timestamp', 754), '[p.9]' -> ('page', 9), or (None, None)."""
    for kind, spec in ANCHOR_KINDS.items():
        m = spec["regex"].fullmatch(literal)
        if m:
            to_value = spec.get("to_value") or spec.get("to_seconds")
            return kind, to_value(m.groups())
    return None, None


def find_anchor_citations(text, own_id):
    """Yield (source_id, kind, value, literal) for every bracketed anchor in a note.

    A bare [anchor] cites the note's own primary source (own_id). An anchor
    immediately preceded by a backtick id — `other-id`[anchor], no space —
    cites that other source instead, using *that* source's own anchor kind.
    """
    out = []
    for m in ANY_ANCHOR_RE.finditer(text):
        literal = m.group(0)
        kind, value = classify_anchor(literal)
        if kind is None:
            continue
        scoped = SCOPED_PREFIX_RE.search(text[:m.start()])
        source_id = scoped.group(1) if scoped else own_id
        out.append((source_id, kind, value, literal))
    return out
