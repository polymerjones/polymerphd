# Ingestion System — Engineering Handoff

Purpose: a precise, implementation-level description of this repo's content-ingestion pipeline,
written so another coding agent (operating in a separate repo, via Codex) can reproduce the
*machinery* — not the content. No note bodies, synthesis text, or health/nutrition/clinical
claims are reproduced anywhere below; only file structure, schemas, code, and one short
transcript-header excerpt appear.

**Note on confidentiality:** this repo is not actually private (it publishes to GitHub Pages at
a public URL, per `README.md`). Earlier internal notes calling it "private" were a documentation
oversight, not a statement about actual visibility — treat nothing below as confidential.

**Note on the target use case:** the stated destination for this machinery is a *different*,
genuinely private repo, ingesting personal journals rather than YouTube/web/PDF/EPUB/Instagram
sources. Nothing about that changes the architecture described below — the pipeline is already
source-kind-agnostic at the `manifest.json`/`notes/`/`knowledge/` layer (§7, §9) — but it does
surface one real gap, called out again in the Migration Checklist: **no existing `add_*.py` script
ingests plain local text (e.g. one file or one entry per day).** The closest existing patterns to
adapt are `add_epub.py` (paragraph-anchored, walks a local file, no network fetch) and
`add_website.py`'s manifest/evidence shape (minus the URL fetch). A new `add_journal.py`-shaped
script — same manifest-upsert pattern, same `[¶N]`-or-date-anchor convention, own `kind` value
(e.g. `"journal_entry"`) — is something Codex will need to write, not something to copy from this
repo. This handoff intentionally does not design that script, per the instruction not to design
new architecture yet.

**Provenance key**, used throughout:
- **[Verified]** — read directly from the code/config in this repo during this session.
- **[Documented]** — stated in this repo's `CLAUDE.md`/`README.md`, not independently re-derived
  from code in this pass.
- **[Inferred]** — a reasonable conclusion that is not explicitly stated anywhere; flagged as a
  judgment call, not a fact.

All paths below are relative to the repo root (`/Users/paulfisher/polymerphd` in this checkout).

---

## 1. High-level architecture

**[Verified]** There is no LLM API call anywhere in `scripts/` — no `openai`, `anthropic`, or
similar SDK is imported by any script. "Extraction" and "synthesis" (the two stages that actually
turn raw material into knowledge) are **human work**. The scripts only do fetch, normalize,
validate, and build. This is the single most important architectural fact for a reproduction: the
"content-ingestion system" is a fetch/normalize/validate/publish pipeline wrapped around a
human-in-the-loop writing step, not an LLM extraction pipeline.

Pipeline shape, per library (a library = one topical corpus, e.g. `nutrition`, `dupuytren`):

```
external source (YouTube / website / PDF / EPUB / Instagram reel / local video file)
        │  fetch (yt-dlp, urllib+trafilatura, pypdf/OCR, zipfile+bs4, instaloader, whisper)
        ▼
sources/raw/<id>.*            — untouched fetch dump (gitignored, regenerable)
        │  normalize (strip boilerplate, paragraph/anchor formatting)
        ▼
sources/clean/<id>.txt        — anchored plain text (the provenance record, committed)
sources/manifest.json         — structured metadata + anchor schema for every source
        │  HUMAN: read clean/<id>.txt once, write a structured note by hand
        ▼
notes/<id>.md                 — YAML frontmatter + 6 universal sections + anchors (committed)
        │  validate (check_notes.py) — refuses to let a bad note through
        ▼
        │  HUMAN: synthesize knowledge/*.md by hand, from notes only, never from raw transcripts
        ▼
knowledge/*.md                 — hand-written synthesis (numbered files + topic_reference_*)
knowledge/09_SOURCE_CATALOG.md — the one knowledge file that IS auto-generated (build_catalog.py)
        │  build (build_app_data.py, make_xcodeproj.py)
        ▼
app/data/<slug>.json, app/index.html, ios/PolymerPhD.xcodeproj/project.pbxproj
        │  publish (git add/commit/push)
        ▼
GitHub Pages (https://polymerjones.github.io/polymerphd/), redeploys ~1 min after push [Documented]
```

What goes in: YouTube video URLs (primary), web pages/PubMed abstracts, PDFs, EPUBs, Instagram
reel URLs, local video files.
What transforms happen: caption/text extraction → boilerplate stripping → anchor-numbered plain
text → (human) claim extraction into a schema'd markdown note → (human) cross-note synthesis →
mechanical catalog/app/iOS rebuild.
What comes out: a set of per-source clean transcripts, one structured note per source, a set of
hand-maintained knowledge files plus one auto-generated source catalog, a self-contained offline
web app, an iOS Xcode project, and (per library) a Custom-GPT-ready file bundle.

---

## 2. Exact ingestion workflow

**[Documented + Verified]** The canonical loop, quoted from `CLAUDE.md` and confirmed against the
scripts:

```
bash scripts/add.sh <slug> https://youtu.be/XXXXXXXXXXX   # 1. fetch, normalize, list what needs a note
                                                            # write libraries/<slug>/notes/<id>.md   <- judgement
python3 scripts/check_notes.py <slug> <id>                 # 2. validate
bash scripts/publish.sh --push                              # 3. rebuild ALL libraries and ship
```

Stage-by-stage, **[Verified]** against the actual code:

1. **`add.sh <slug> <url...>`** (`scripts/add.sh`) — three sub-steps, printed as
   `── 1/3 registering links ──`, `── 2/3 fetching captions ──`, `── 3/3 normalizing ──`:
   - `add_videos.py <slug>` classifies every pasted id into `already fetched` / `already listed`
     / `previously excluded` / `new`, appends new ids to `ingest_state/video_ids_full.txt`, and
     writes the ones that actually need fetching to `ingest_state/video_ids_added.txt`.
   - `fetch_transcripts.sh <slug> ingest_state/video_ids_added.txt` shells out to `yt-dlp` to pull
     caption tracks + metadata into `sources/raw/`.
   - `normalize.py <slug>` turns each `sources/raw/<id>.*` pair into `sources/clean/<id>.txt` and
     (re)writes `sources/manifest.json`.
   - Finally `add.sh` prints (and writes to `ingest_state/notes_todo.txt`) every fetched source
     that has neither a note nor a deferred entry — i.e., "what still needs a note."
2. **Human writes `libraries/<slug>/notes/<id>.md`** — reads `sources/clean/<id>.txt` once, no
   scripts run here. Format is fixed per-library (see §6/§7 below).
3. **`check_notes.py <slug> [id...]`** — validates the note(s) against the library's schema and
   citation-provenance rules; exits nonzero on any failure.
4. **`publish.sh [--push]`** — for every library found under `libraries/*/library.json`: rebuilds
   that library's `09_SOURCE_CATALOG.md` (`build_catalog.py`), then rebuilds the offline app for
   *all* libraries at once (`build_app_data.py`), then regenerates the iOS Xcode project
   (`make_xcodeproj.py`). With `--push`, commits everything changed and pushes to `origin main`.

Non-YouTube source kinds enter the same `sources/clean/` + `sources/manifest.json` + `notes/` +
`publish.sh` pipeline through their own one-shot scripts instead of `add.sh`'s three-step flow —
`add_website.py`, `add_pdf.py`, `add_epub.py`, `add_instagram_reel.py`, `add_local_video.py`,
`add_video_whisper.py` / `add_videos_whisper.py` (YouTube-video-without-captions fallback). Each
does fetch+normalize itself in one process and upserts directly into `sources/manifest.json`; from
there stages 2–4 above are identical regardless of source kind.

---

## 3. Repository structure relevant to ingestion

**[Verified]**

```
scripts/                              — all pipeline code (flat directory, 25 files, no subpackages)
  lib_common.py                       — shared Library class + anchor-citation helpers (imported by nearly everything)
  add.sh, fetch_transcripts.sh,
  add_videos.py, normalize.py         — YouTube ingestion (the "add.sh" pipeline)
  check_notes.py                      — validation gate
  build_catalog.py                    — generates knowledge/09_SOURCE_CATALOG.md
  build_app_data.py                   — generates app/data/<slug>.json + app/index.html (all libraries)
  make_xcodeproj.py                   — generates ios/PolymerPhD.xcodeproj/project.pbxproj
  publish.sh                          — orchestrates the three build scripts + git commit/push
  add_website.py, add_pdf.py,
  add_epub.py, add_instagram_reel.py,
  add_local_video.py,
  add_video_whisper.py,
  add_videos_whisper.py               — non-YouTube / caption-less ingestion paths
  list_channel.py, classify_channel.py,
  check_gaps.py                       — one-off channel triage tooling (classify_channel.py and
                                         check_gaps.py are hardcoded to one library, see §4)
  slice_sections.py, slice_matching.py — synthesis staging helpers, hardcoded to restorative-physiology
  build_custom_gpt_bundle.py          — merges multiple libraries' knowledge files into one bundle

libraries/<slug>/                     — one directory per topical corpus
  library.json                        — per-library config: facets, sections, attribution, Custom GPT settings
  sources/
    raw/                              — untouched fetch dumps, GITIGNORED, regenerable
    clean/<id>.txt                    — normalized, anchor-numbered plain text — the provenance record, COMMITTED
    manifest.json                     — {"sources": [...], "skipped": [...]} — authoritative metadata, COMMITTED
    images/<id>/                      — (Instagram-sourced libraries) extracted stills, COMMITTED
  notes/<id>.md                       — one hand-written structured note per source, COMMITTED
  knowledge/                          — hand-synthesized knowledge files + auto-generated catalog, COMMITTED
    00_README.md ... NN_*.md          — numbered synthesis files (no source-id citations by design)
    topic_reference_NN_*.md           — deep-dive files that DO carry source-id citations
    09_SOURCE_CATALOG.md              — auto-generated by build_catalog.py (filename configurable per library)
  ingest_state/                       — working-state files for the ingest process itself (mostly COMMITTED,
                                         one file gitignored — see §16)
  deferred_sources.txt                — ids deliberately excluded from note-writing, one per line + reason
  icon.b64, splash.b64                — raw base64 PNG image data (no data: URI prefix), COMMITTED
  PASTE_INTO_GPT_INSTRUCTIONS.txt     — that library's literal Custom GPT system prompt, COMMITTED
  overrides.json                      — OPTIONAL, hand corrections for derived practice facets (present only
                                         if that library needs them; absent = {})

app/
  app.template.html                   — the offline-app shell template with placeholder tokens
  index.html                          — BUILD OUTPUT of build_app_data.py (do not hand-edit)
  data/<slug>.json                    — BUILD OUTPUT, one per library
  sound.b64                           — raw base64 audio data inlined into the app shell
  unclassified_practices_<slug>.txt   — BUILD OUTPUT, only written for libraries with unclassified practice cards

ios/
  PolymerPhD.xcodeproj/project.pbxproj — BUILD OUTPUT of make_xcodeproj.py (never hand-edit in Xcode)
  PolymerPhD/Resources/index.html      — BUILD OUTPUT, byte copy of app/index.html

CLAUDE.md, README.md, .gitignore       — root-level operating docs (see §5, §8, §16)
```

---

## 4. Every script — path, purpose, I/O, interactions

All scripts below were read in full this session. Every `add_*`/`check_notes`/`build_catalog`
script (except `build_app_data.py`, `build_catalog.py`, `publish.sh`, `make_xcodeproj.py`) takes a
library `<slug>` as `argv[1]`, resolved through `lib_common.Library`.

### `scripts/lib_common.py` (200 lines) — shared library, not run directly

**[Verified]** Defines `class Library(slug)`, which raises `SystemExit` (listing known slugs) if
`libraries/<slug>/library.json` doesn't exist, and otherwise exposes path properties (`.notes`,
`.knowledge`, `.sources_dir`, `.clean_dir`, `.raw_dir`, `.manifest_path`, `.deferred_path`,
`.ingest_state_dir`) and config-driven properties (`.facets`, `.primary_facet`,
`.universal_sections`, `.controlled_facets`, `.glossary_file`, `.curated_facts_file`,
`.catalog_file`) read from `library.json` with sane fallbacks. Also provides:

- `require_slug(argv, usage)` — pops the slug off `argv`, or exits with `usage` + the list of
  known libraries (`all_library_slugs()`, which scans `libraries/*/library.json`). Reused by
  nearly every other script's `main()`.
- `ANCHOR_KINDS` — a dict keyed by `"timestamp"` / `"page"` / `"paragraph"`, each with a regex, a
  value-conversion function, and a canonicalization function. This is the single definition of
  what an anchor looks like for each source kind.
- `find_anchor_citations(text, own_id)` — yields `(source_id, kind, value, literal)` for every
  bracketed anchor in a note's body. A bare `[anchor]` cites the note's own source; an anchor
  immediately preceded by a backtick id with no space — `` `other-id`[anchor] `` — cites a
  different source, using *that* source's anchor kind.
- `BACKTICK_ID_RE` — matches a bare backtick-quoted 11-char YouTube id (a cross-reference with no
  anchor, e.g. "see also `dQw4w9WgXcQ`").
- `Library.load_manifest()` / `.save_manifest(manifest)` — reads/writes `manifest.json` with
  `json.dumps(..., indent=2, ensure_ascii=False, sort_keys=False)` plus a trailing newline.
- `Library.sources_by_id()` — `{id: source_dict}` from the manifest.
- `Library.deferred_ids()` — `re.findall(r"[A-Za-z0-9_-]{6,}", deferred_sources.txt text)`, i.e. a
  crude token scan, not a line-exact parse.

Dependencies: stdlib only (`json`, `re`, `pathlib`). No env vars, no CLI.

### `scripts/add.sh` (90 lines)

**[Verified]** `bash scripts/add.sh <slug> [urls...]` (or piped via stdin, e.g. `pbpaste |
bash scripts/add.sh <slug>`). `SLUG="${1:?Usage: ...}"` (bash required-arg pattern). Runs under
`set -uo pipefail` — deliberately **not** `-e**, so it keeps reporting through a substep's
non-fatal failure. Deletes `ingest_state/video_ids_added.txt` at the start of every run ("a stale
one would silently re-fetch the previous slate," per its own comment), then runs
`add_videos.py` → `fetch_transcripts.sh` → `normalize.py` in sequence, then an inline Python
heredoc (`python3 - "$SLUG" <<'PY' ... PY`) that computes and prints/writes the "still needs a
note" list to `ingest_state/notes_todo.txt` as tab-separated `id\ttitle` lines. Exits 1 if
`libraries/$SLUG` doesn't exist.

### `scripts/fetch_transcripts.sh` (53 lines)

**[Verified]** `bash scripts/fetch_transcripts.sh <slug> [batch-file]` (default batch file:
`ingest_state/video_ids.txt`). Shells out to `yt-dlp` directly:

```bash
yt-dlp \
  --skip-download --write-auto-subs --sub-langs "en-orig,en" --sub-format json3 \
  --write-info-json --no-overwrites --ignore-errors --no-warnings \
  --sleep-requests 1.5 --sleep-interval 2 --max-sleep-interval 5 \
  --retries 5 --extractor-retries 3 \
  -o "$RAW/%(id)s.%(ext)s" --batch-file "$BATCH"
```

Writes `sources/raw/<id>.info.json`, `<id>.en-orig.json3`, `<id>.en.json3`. `--no-overwrites` +
`--ignore-errors` make this idempotent and fault-tolerant per-video. No audio/video is ever
downloaded here.

### `scripts/add_videos.py` (121 lines)

**[Verified]** `python3 scripts/add_videos.py <slug> [links.txt]` (or stdin). Extracts 11-char
YouTube ids from arbitrary pasted text via two regexes (`v=`, `/shorts/`, `/live/`, `/embed/`,
`youtu.be/`, or a bare id). Classifies every id into exactly one of four buckets — see the exact
logic quoted below (this is the core dedup mechanism for YouTube ingestion):

```python
fetched = {p.name.split(".")[0] for p in lib.raw_dir.glob("*.json3")} & \
          {p.name.split(".")[0] for p in lib.raw_dir.glob("*.info.json")}
...
buckets = {"already fetched": [], "already listed": [], "previously excluded": [], "new": []}
for vid in pasted:
    if vid in fetched: buckets["already fetched"].append(vid)
    elif vid in listed_set: buckets["already listed"].append(vid)
    elif vid in excluded_map: buckets["previously excluded"].append(vid)
    else: buckets["new"].append(vid)
to_fetch = buckets["new"] + buckets["previously excluded"]
```
`listed_set` comes from `ingest_state/video_ids_full.txt`; `excluded_map` from
`ingest_state/excluded_videos.tsv`. New ids get appended to `video_ids_full.txt`; `to_fetch`
(new + previously-excluded, since a previously-excluded id pasted again is an explicit override)
is written to `ingest_state/video_ids_added.txt`. Never deletes or rewrites existing transcripts.

### `scripts/normalize.py` (224 lines)

**[Verified]** `python3 scripts/normalize.py <slug>`. Reads every `sources/raw/<id>.info.json`
(falling back caption-wise to `.en-orig.json3` then `.en.json3` — `caption_path()`). Cleanup
pipeline: `TAG_RE` strips `[...]` sound-effect tags; `BOILERPLATE_RE` strips subscribe/like/bell/
comment boilerplate via a list of regex patterns; `dedupe_consecutive()` drops rolling-caption
duplicate lines; `build_body()` groups captions into paragraphs anchored every 60 seconds
(`ANCHOR_EVERY_SEC = 60`) in `[mm:ss]` format. Writes:

- `sources/clean/<id>.txt` — header block (`TITLE`, `VIDEO ID`, `URL`, `UPLOAD DATE`, `DURATION`,
  `CAPTION TRACK`, then 70 `=` characters) followed by the anchored body.
- `sources/manifest.json` — full rewrite. **Idempotency-critical detail:** it explicitly preserves
  any existing non-YouTube manifest entries, and any YouTube entry whose `transcript_source`
  starts with `"whisper"`, across every re-run:
  ```python
  other_sources = [s for s in existing.get("sources", []) if s.get("kind") != "youtube"
                   or s.get("transcript_source", "").startswith("whisper")]
  ```
  ("those have no caption track to rediscover here and would otherwise silently vanish from the
  manifest every time this script re-runs" — code comment.)

Videos with no caption file or an empty transcript go into `manifest["skipped"]` with
`reason: "no captions"` / `"empty transcript"` rather than aborting the run. Exits with
`sys.exit("No .info.json files found — run fetch_transcripts.sh first.")` if `raw/` is empty.

Manifest entry shape written here (`kind: "youtube"`):
```python
{
  "id": vid, "kind": "youtube", "title": title, "url": url,
  "upload_date": date, "duration_seconds": duration, "duration": dur_str,
  "word_count": len(body.split()), "clean_file": f"clean/{vid}.txt",
  "anchor": {"kind": "timestamp", "format": "mm:ss",
             "bound_field": "duration_seconds", "bound": duration},
}
```

### `scripts/check_notes.py` (207 lines) — the anti-fabrication validation gate

**[Verified]** `python3 scripts/check_notes.py <slug> [id...] [--terms]`. For every targeted note
(all notes by default, or specific ids), `check()` runs:

1. Every heading in `library.json`'s `universal_sections` is present as a `## ` heading.
2. The frontmatter block (`text.split("---")[1]`) parses as valid YAML.
3. Every declared facet (`library.json`'s `facets`) has a `"<facet>:"` line in frontmatter (a
   substring check, not structural YAML validation).
4. Every `images:` frontmatter entry points to a file that exists under `sources/`.
5. Every declared controlled-facet value (`library.json`'s `controlled_facets`, e.g.
   `restorative-physiology`'s `systems`) is in that facet's fixed vocabulary.
6. The note's own `id` is present in `sources/manifest.json`.
7. **The core check**: every anchor citation found by `find_anchor_citations()` — resolves to a
   known source id; matches that source's declared `anchor.kind` (e.g. rejects a `[mm:ss]`-shaped
   anchor against a page-anchored PDF source); does not exceed that source's `anchor.bound`; and
   the literal anchor string (e.g. `"[12:34]"`) appears **verbatim** in that source's
   `sources/clean/<id>.txt` text.
8. Every bare backtick cross-reference (`` `id` ``, via `BACKTICK_ID_RE`) either has its own note,
   is a source in the manifest, or is a deferred id.

`--terms` is a separate advisory-only mode (`review_terms()`): for each note's
`## Glossary terms introduced` section, it checks whether the term's own wording (British-to-
American folded via `anglicise()`, crudely stemmed via `term_roots()`) appears anywhere in that
note's source transcript. A flag means "auto-caption garbling or imported terminology — go read
this," not "this is wrong."

Prints `FAIL <id>` + bullet problems per failing note, and `"{passed}/{total} notes pass."` at the
end. `main()` returns `1 if failed else 0`; `sys.exit(main())`. Writes nothing to disk — pure
validator.

### `scripts/build_catalog.py` (196 lines)

**[Verified]** `python3 scripts/build_catalog.py <slug>`. Reads every `notes/<id>.md`'s
frontmatter (via `parse_frontmatter()`, which requires the file start with `---` and the
frontmatter parse as a YAML mapping) plus `sources/manifest.json`. **Refuses to write anything**
if any note's `id` isn't in the manifest (`sys.exit("Catalog build failed:\n  " + ...)`), or if
there are no notes at all. Otherwise writes `knowledge/<catalog_file>` (default
`09_SOURCE_CATALOG.md`, configurable per library): a heading, a description line (templated from
`library.json`'s `facet_labels`, or a literal `catalog_description` override), an attribution
line (from `library.json`'s `attribution`), a numbered, alphabetical-by-title entry per note (id,
url, author, upload_date, duration, `source_file`, one bullet per facet), a reverse index by the
library's second facet (or `systems` if present), and a "No transcript available — link only, not
cited" section for manifest `skipped` entries reasoned `"no captions"`/`"empty transcript"`.
`build_app_data.py` imports `parse_frontmatter` and `as_list` directly from this module — it is
deliberately safe to `import` (guarded `if __name__ == "__main__":`).

### `scripts/build_app_data.py` (577 lines) — the largest script; builds the offline app

**[Verified]** `python3 scripts/build_app_data.py` — no arguments; discovers every library via
`all_library_slugs()` and processes **all of them in one run**. Per its own docstring:

```
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
```

Key logic:
- `load_notes()` — parses each note's frontmatter + body, splits into `{heading: body}` via
  `split_sections()`, checks every `universal_sections` heading is present, re-validates every
  anchor citation against the manifest (same check as `check_notes.py`, independently
  implemented here), base64-embeds any `images:` files, and assembles a per-video dict with all
  frontmatter facets plus `sections`, `anchors` (citation count), and `images`.
- `load_knowledge_files()` — splits each `knowledge/*.md` by `# ` and `## ` headings into a
  nested structure, and extracts `cited_ids` by intersecting every backtick-quoted token in the
  file against the manifest's known ids (so a backtick-quoted filename like `` `09_SOURCE_CATALOG.md` ``
  is never mistaken for a source citation).
- `load_glossary()` — parses `**Term** — definition` lines from the library's `glossary_file`.
- `load_curated_symptoms()` — parses the library's `curated_facts_file`, if it has one.
- `build_symptoms()` — pulls bullet lines from every note's `Symptoms and body signals addressed`
  section, extracts any timestamp anchors from each bullet, and heuristically links each bullet to
  a curated entry via `match_curated()` (token-overlap score, threshold `>= 0.6` — deliberately
  strict, per its own comment, "a wrong match would attribute a mechanism to a symptom the source
  never linked").
- `build_practices()` / `derive_duration()` / `derive_position()` / `derive_equipment()` — regex
  heuristics pulling duration/position/equipment out of free-text practice strings, gated by
  `library.json`'s `derived_practice_facets` flag (only `true` for `restorative-physiology`
  today). Explicitly labeled "PARTIAL" in the code's own comments. Unclassified cards are written
  to `app/unclassified_practices_<slug>.txt` for correction via `libraries/<slug>/overrides.json`
  (a flat `{"<video_id>::<practice text>": {"duration_seconds":..., "position":..., "equipment":...}}`
  map, applied as an override before the heuristic).
- **Refuses to write anything for a library with validation problems** — collects up to 40
  `problems` strings, prints them to stderr, and `sys.exit(1)` before any file for that library is
  touched.
- Determinism, stated explicitly in the docstring and enforced in code: `json.dumps(data,
  ensure_ascii=False, sort_keys=True, separators=(",", ":"))` for `app/data/<slug>.json`, and
  `gzip.compress(payload.encode("utf-8"), compresslevel=9, mtime=0)` (mtime pinned to 0 "keeps the
  gzip header byte-identical between runs") for each library's inlined blob in `app/index.html`.

Template assembly: reads `app/app.template.html`, replaces `/*__LIBRARY_INDEX__*/` (a JSON array
of `{slug, title, subtitle, teaser, sources, anchors, icon_b64}` per library) and
`/*__LIBRARIES__*/` (a `{slug: base64(gzip(library_json))}` map), then `__ICON__`/`__SPLASH__`
(from the alphabetically-first library's `icon.b64`/`splash.b64`) and `__SOUND__` (from
`app/sound.b64`, replaced with `count=1` deliberately — the template reuses the literal string
`"__SOUND__"` as its own "no sound configured" sentinel, so a blanket replace would break that
comparison). Exits with a clear message if the template or its placeholders are missing.

### `scripts/make_xcodeproj.py` (285 lines)

**[Verified]** `python3 scripts/make_xcodeproj.py` — no args. Regenerates
`ios/PolymerPhD.xcodeproj/project.pbxproj` from an in-code template with stable, deterministic hex
object ids (`ID = {n: f"{i + 0x1000:024X}" for i, n in enumerate(NAMES)}`), and copies
`app/index.html` byte-for-byte to `ios/PolymerPhD/Resources/index.html`. Reads the
`DEVELOPMENT_TEAM` environment variable (falls back to a hardcoded team id) for iOS codesigning —
see §13. No error handling on a missing `app/index.html` (would raise on `.read_bytes()`).

### `scripts/publish.sh` (58 lines) — the orchestrator

**[Verified]** `bash scripts/publish.sh [--push]`, `set -euo pipefail` (this one DOES use `-e`,
unlike `add.sh`/`fetch_transcripts.sh`). Sequence:
1. `python3 scripts/build_catalog.py <slug>` for every `libraries/*/library.json` found.
2. `python3 scripts/build_app_data.py` (all libraries).
3. `python3 scripts/make_xcodeproj.py`.
4. Prints `git status --porcelain`.
5. With `--push`: if nothing changed, prints "Nothing to publish" and exits 0. Otherwise computes
   `NEW=$(git status --porcelain libraries/*/notes/ | grep -c '^??' || true)`, runs `git add -A`,
   `git commit -q -m "Add ${NEW} note(s) and rebuild outputs"`, `git push -q origin main`.

Because of `set -euo pipefail`, any of the three build scripts exiting nonzero (which they do on
validation failure — see §14/§15) aborts the whole publish **before any git operation runs**.

### Non-YouTube ingestion scripts (all follow the same manifest-upsert pattern; each is its own
one-shot process — no shared `add_*.sh` wrapper exists for these kinds)

**[Verified]** — `scripts/add_website.py` (222 lines): `argparse` CLI
(`slug`, `urls` (nargs="+"), `--id`, `--title`, `--author`, `--evidence-type`, `--evidence-level`,
`--year`). Fetches via raw `urllib.request` with a spoofed Chrome User-Agent (quoted: `"Mozilla/5.0
(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0
Safari/537.36"` — "some sites (e.g. PubMed) block trafilatura's default fetcher but allow this");
PubMed URLs (`pubmed.ncbi.nlm.nih.gov/<pmid>`) instead hit NCBI's efetch API directly. Extracts
text via `trafilatura.extract(...)`. Writes `sources/clean/<id>.txt` with a `[¶N]`-anchored body
and a manifest entry `kind: "website"`, `anchor: {"kind": "paragraph", "format": "¶N",
"bound_field": "paragraph_count", "bound": N}`, optional `evidence: {type, level, year}`. Multiple
URLs are treated as one continuous paginated source ("chapters").

`scripts/add_pdf.py` (133 lines): same CLI shape plus a PDF path. Extracts text per page via
`pypdf`; falls back to `pdf2image` + `pytesseract` OCR for pages with under 20 extracted
characters (page left blank with a warning if OCR deps aren't installed, not fatal). Manifest
`kind: "pdf"`, `anchor: {"kind": "page", "format": "p.N", "bound_field": "page_count", "bound": N}`.

`scripts/add_epub.py` (188 lines): parses the EPUB's own `META-INF/container.xml` → OPF
manifest/spine (via `xml.etree.ElementTree`) to walk chapters in true reading order, extracts
paragraph text per spine document via `BeautifulSoup` over a fixed `BLOCK_TAGS` set. Manifest
`kind: "epub"`, `[¶N]` paragraph anchors continuous across the whole book.

`scripts/add_instagram_reel.py` (297 lines): `argparse` CLI supporting either
`<slug> <url-or-shortcode> [--id] [--title] [--login] [--comment-limit] [--onscreen-file]
[--frame-pct]` (instaloader mode) or a fully manual fallback
(`--video-file --caption-file --url --title --author [--manual-url]`) for posts instaloader can't
reach. The caption text is the primary, paragraph-anchored source
(`kind: "instagram_caption"`); an optional `--onscreen-file` (the operator's own `[mm:ss]`-anchored
notes on visible/spoken content) becomes a second manifest entry with id `<id>-video`
(`kind: "instagram_reel"`, timestamp-anchored). Extracts cover + frame stills via `ffprobe`/
`ffmpeg` into `sources/images/<id>/`. Comment fetching is a fallback for thin captions, requires a
saved `instaloader` session (`--login <username>`, see §13), and catches
`instaloader.exceptions.LoginRequiredException` with a pointer back to the one-time
`instaloader --login` setup.

`scripts/add_local_video.py` (172 lines): `argparse` CLI (`slug`, `path`, `--id`, `--title`,
`--source-note`, `--release-year`, `--model` default `"small"`, `--device` default `"cpu"`
(choices `cpu`/`mps`), `--language` default `"en"`). For video files that were never on YouTube
(e.g. a purchased DVD rip). Transcribes locally via `whisper.load_model(model_name,
device=device); model.transcribe(...)`. Timestamp format switches from `MM:SS` to `H:MM:SS` past
one hour (documented reason: some DVDs run past 99 minutes, which a 2-digit-minute anchor regex
can't parse). Manifest `kind: "video_local"`, `transcript_source: "whisper-local:<model>"`.

`scripts/add_video_whisper.py` (190 lines) / `scripts/add_videos_whisper.py` (139 lines, batch
wrapper importing helpers from the singular script): for a YouTube video that `normalize.py`
already reported as `"no captions"` in `manifest["skipped"]`. Downloads audio only
(`yt-dlp -x --audio-format mp3`), transcribes locally with Whisper, strips the id back out of
`skipped`. The batch version loads the Whisper model once, is explicitly documented as
interruption-safe (`todo = [vid for vid in ids if not (lib.clean_dir / f"{vid}.txt").exists()]`),
wraps each video's processing in `try/except Exception` so one bad video doesn't kill the batch,
and deletes the downloaded audio file after transcription (raw/ is gitignored and disk-heavy).

### Ancillary / one-off tooling (not part of the routine per-video loop)

**[Verified]** `scripts/list_channel.py` (63 lines) — `python3 scripts/list_channel.py <slug>
<channel_url>`; shells out to `yt-dlp --flat-playlist --print "%(id)s\t%(availability)s\t%(duration)s\t%(title)s"`;
writes `ingest_state/channel_full.tsv`. Listing only — nothing fetched into `sources/`.

`scripts/classify_channel.py` (119 lines) — **hardcoded to `restorative-physiology`**
(`LIB = ROOT / "libraries" / "restorative-physiology"`), no CLI args. Filters that channel's full
listing against a large hardcoded `EXCLUDE` dict (~70 id→reason entries) to produce
`ingest_state/video_ids_full.txt` (included) and `ingest_state/excluded_videos.tsv` (excluded).

`scripts/check_gaps.py` (106 lines) — also scoped only to `restorative-physiology` ("predates the
multi-library layout," per its own docstring). No CLI args. Detects caption-track silence gaps
≥45s in raw json3 timing data; writes `sources/caption_gaps.json`.

`scripts/build_custom_gpt_bundle.py` (116 lines) — `argparse` CLI: `slugs` (nargs="+"), `--out`
(default `custom_gpt_combined`). Concatenates each named library's numbered knowledge files
(00–08, excluding the glossary) into `<slug>_KNOWLEDGE.md`, its `topic_reference_*.md` files into
`<slug>_TOPIC_REFERENCE.md`, and merges glossaries/catalogs across all named libraries into
`COMBINED_GLOSSARY.md`/`COMBINED_SOURCE_CATALOG.md`. Pure concatenation — "no content is
rewritten, this only merges file boundaries."

**[Documented, in `CLAUDE.md`'s Gotchas]** `slice_sections.py` and `slice_matching.py` read
`sys.argv` at module level and cannot be imported; `build_catalog.py` guards its entry point and
is safely importable (confirmed: `build_app_data.py` imports from it).

`scripts/slice_sections.py` (73 lines) — hardcoded to `restorative-physiology`. CLI:
`python3 scripts/slice_sections.py <heading> [out_dir]`. Extracts one named universal-section
heading verbatim across every note in that library into
`libraries/restorative-physiology/scratch_sections/<slugified-heading>.md`, for reading one
dimension across all notes during synthesis.

`scripts/slice_matching.py` (68 lines) — same library scope. CLI:
`python3 scripts/slice_matching.py <regex> <out_dir> <out_name>`. Same idea but matches headings
by regex, for "practice and protocol material" that lives under video-specific (not fixed)
headings.

---

## 5. Commands — worked examples

**[Documented + Verified]**

```bash
# Standard YouTube add-a-video loop
bash scripts/add.sh restorative-physiology https://youtu.be/XXXXXXXXXXX
# ... write libraries/restorative-physiology/notes/XXXXXXXXXXX.md by hand ...
python3 scripts/check_notes.py restorative-physiology XXXXXXXXXXX
bash scripts/publish.sh --push

# Validate everything in a library, or just run the advisory terminology check
python3 scripts/check_notes.py nutrition
python3 scripts/check_notes.py nutrition --terms

# Rebuild without shipping (see what changed first)
bash scripts/publish.sh

# Website / PubMed source
python3 scripts/add_website.py dupuytren https://pubmed.ncbi.nlm.nih.gov/36566101/ \
  --evidence-type systematic_review --evidence-level high --year 2023

# PDF source
python3 scripts/add_pdf.py dupuytren path/to/guideline.pdf \
  --title "..." --author "..." --evidence-type guideline --evidence-level high --year 2020

# EPUB source
python3 scripts/add_epub.py <slug> path/to/book.epub --title "..." --author "..." \
  --evidence-type textbook

# Instagram reel (one-time setup, then per-post)
pip3 install instaloader
instaloader --login <your-instagram-username>
python3 scripts/add_instagram_reel.py healthy-baked-goods https://www.instagram.com/reel/XXXX/ \
  --onscreen-file my_notes.txt

# Local video file / YouTube video with no captions, via local Whisper
python3 scripts/add_local_video.py <slug> path/to/video.mp4 --title "..." --model small
python3 scripts/add_video_whisper.py <slug> https://youtu.be/XXXXXXXXXXX --model turbo
cat ids.txt | python3 scripts/add_videos_whisper.py <slug> --model turbo

# Channel triage (pre-ingestion)
python3 scripts/list_channel.py <slug> https://www.youtube.com/@SomeChannel

# Rebuild just the app / just the iOS project (normally publish.sh does both, in order)
python3 scripts/build_app_data.py
python3 scripts/make_xcodeproj.py

# Custom GPT bundle across multiple libraries
python3 scripts/build_custom_gpt_bundle.py nutrition dupuytren --out custom_gpt_combined
```

---

## 6. File formats and naming conventions

**[Verified]**

| Artifact | Path pattern | Format |
|---|---|---|
| Raw YouTube fetch | `sources/raw/<id>.info.json`, `<id>.en-orig.json3`, `<id>.en.json3` | yt-dlp's own JSON formats |
| Raw Whisper audio | `sources/raw/<id>.audio.mp3` | deleted after batch transcription |
| Clean transcript | `sources/clean/<id>.txt` | header block + `[mm:ss]`/`[h:mm:ss]`-anchored paragraphs (YouTube/video) |
| Clean web/PubMed text | `sources/clean/<id>.txt` | header block + `[¶N]`-anchored paragraphs |
| Clean PDF text | `sources/clean/<id>.txt` | header block + `[p.N]`-anchored pages |
| Clean EPUB text | `sources/clean/<id>.txt` | header block + `[¶N]`-anchored paragraphs, continuous across the book |
| Note | `notes/<id>.md` | YAML frontmatter + `# Title` + `## ` sections (see §7) |
| Manifest | `sources/manifest.json` | `{"sources": [...], "skipped": [...]}` (see §7) |
| Deferred list | `deferred_sources.txt` | one id per line, `<id>  # <reason>` |
| Numbered knowledge file | `knowledge/NN_TOPIC_NAME.md` | hand-written, no source-id citations by design |
| Deep-dive knowledge file | `knowledge/topic_reference_NN_NAME.md` | hand-written, DOES carry source-id citations |
| Source catalog | `knowledge/09_SOURCE_CATALOG.md` (name configurable) | auto-generated, numbered entries, alphabetical by title |
| Ingest backlog | `ingest_state/notes_todo.txt` | `<id>\t<title>` per line |
| Full id list | `ingest_state/video_ids_full.txt` | one full `https://www.youtube.com/watch?v=<id>` URL per line |
| Fetch batch (transient) | `ingest_state/video_ids_added.txt` | one URL per line, rewritten every `add.sh` run, GITIGNORED |
| Channel snapshot | `ingest_state/channel_full.tsv` | `<id>\t<availability>\t<duration>\t<title>`, no header |
| Excluded list | `ingest_state/excluded_videos.tsv` | header `id\treason\ttitle` |
| App data | `app/data/<slug>.json` | build output, see §7 |
| App shell | `app/index.html` | build output, self-contained, gzip+base64-inlined per-library data |

`<id>` for YouTube sources is the 11-character YouTube video id. For non-YouTube sources, `<id>`
is an operator-chosen slug (`--id`) or a default derived from the source (e.g. PubMed uses the
pmid-derived id seen in `dupuytren`'s manifest, `layton-2023-fibrotic-disorder-review`).

The clean-file header format, **[Verified]** from `normalize.py`, for a YouTube source:
```
TITLE: <title>
VIDEO ID: <id>
URL: <url>
UPLOAD DATE: <YYYY-MM-DD or "not available">
DURATION: <mm:ss or "not available">
CAPTION TRACK: <en-orig | en>
======================================================================

[00:00] <transcript text>

[01:00] <transcript text>
...
```

---

## 7. Schemas / internal data structures

### `library.json` — **[Verified]**, keys observed across `nutrition`/`dupuytren`/`restorative-physiology`

| Key | Type | Notes |
|---|---|---|
| `slug` | string | matches the directory name |
| `title`, `subtitle` | string | display name/tagline |
| `lede` | string | uses `{videos}` template placeholder, filled by `build_app_data.py` |
| `about_paragraphs` | array of strings | uses `{videos}`/`{library_files}`/`{glossary_terms}` placeholders |
| `icon_file`, `splash_file` | string | filename within the library dir, e.g. `"icon.b64"` |
| `facets` | array of strings | frontmatter facet names for this library, e.g. `["subjects","foods","concerns","concepts"]` |
| `primary_facet` | string | default browse dimension; `lib_common.py` defaults to the 2nd facet if unset |
| `controlled_facets` | object, facet name → array of allowed values | `{}` unless the library needs a fixed vocabulary (only `restorative-physiology`'s `systems` today) |
| `universal_sections` | array of 6 strings, in order | the mandatory `## ` headings every note must contain |
| `role_sections` | object (restorative-physiology only) | maps a role name to alternate heading text that also satisfies it |
| `glossary_file`, `curated_facts_file`, `catalog_file` | string or null | knowledge filenames for the glossary / curated-facts index / source catalog |
| `facet_labels` | object, facet key → display label | UI labels |
| `catalog_description` | string, optional | overrides `build_catalog.py`'s auto-generated description line |
| `catalog_unit_label`, `catalog_id_label` | string | e.g. `"Videos"`/`"Video ID"` vs `"Sources"`/`"Source ID"` |
| `attribution` | object `{style, name, url}` | `style` values seen: `youtube_channel`, `youtube_channel_partial` |
| `custom_gpt` | object `{enabled, instructions_file, file_limit}` | `file_limit` is the Custom GPT 20-file cap |
| `derived_practice_facets` | boolean | gates `build_app_data.py`'s regex duration/position/equipment extraction |
| `evidence_types`, `evidence_levels` | array of strings | only in mixed-source-kind libraries (nutrition, dupuytren); `evidence_levels` is `["high","moderate","low","anecdotal"]` in both |

### `sources/manifest.json` — **[Verified]**

Top level: `{"sources": [...], "skipped": [...]}`.

Common fields across every source kind: `id`, `kind` (`"youtube"` | `"website"` | `"pdf"` |
`"epub"` | `"instagram_caption"` | `"instagram_reel"` | `"video_local"`), `title`, `url`,
`clean_file`, `word_count`, `anchor` (sub-object below). Kind-specific fields:
- `youtube`/`video_local`: `upload_date`, `duration_seconds`, `duration`; `video_local`/whisper-
  transcribed youtube also carry `transcript_source` (e.g. `"whisper-local:turbo"`).
- `website`/`pdf`: `author`, `retrieved_date`, optional `evidence: {type, level, year}`.

`anchor` sub-schema, one of:
```json
{"kind": "timestamp", "format": "mm:ss",   "bound_field": "duration_seconds", "bound": 527}
{"kind": "page",      "format": "p.N",     "bound_field": "page_count",       "bound": 3}
{"kind": "paragraph",  "format": "¶N",      "bound_field": "paragraph_count",  "bound": 41}
```
`skipped[]` entries: `{id, title, url, duration_seconds, duration, reason}` (reason e.g.
`"no captions"`, `"empty transcript"`).

Full real example (`dupuytren`, structural only — **[Verified]**):
```json
{
  "id": "assh-dupuytrens-contracture",
  "kind": "pdf",
  "title": "Dupuytren's Contracture",
  "author": "American Society for Surgery of the Hand",
  "url": "https://www.assh.org/handcare/condition/dupuytrens-contracture",
  "retrieved_date": "2026-08-23",
  "clean_file": "clean/assh-dupuytrens-contracture.txt",
  "word_count": 1828,
  "anchor": {"kind": "page", "format": "p.N", "bound_field": "page_count", "bound": 3},
  "evidence": {"type": "expert_commentary", "level": "moderate", "year": 2020}
}
```

### Note frontmatter — **[Verified]**

```yaml
---
id: <matches manifest id>
title: "<string>"
url: <source URL>                 # video/website sources
upload_date: <YYYY-MM-DD>          # video sources
duration: "<mm:ss>"                # video sources
author: <string>                   # PDF/website/EPUB sources instead of upload_date/duration
<facet_1>: [ ... ]                 # one key per library.json's `facets`, values are free text —
<facet_2>: [ ... ]                 #   often full descriptive clauses, not single tags (confirmed
...                                 #   in a real nutrition note: a `subjects:` entry is a full sentence)
images: [ "images/<id>/00.jpg" ]   # optional; checked to exist by check_notes.py
---
```

Body: `# <Title>` (H1), then `## ` (H2) sections. The six **universal sections**, fixed order,
**[Documented + Verified]** identical text across every library checked:
1. `## Central claim`
2. `## <symptoms/signals heading>` — e.g. `Symptoms and body signals addressed`; the heading text
   is declared per-library in `library.json`'s `universal_sections` and can be adapted in wording
   for a non-physiology library (`CLAUDE.md`'s own example: a mindset library might use "Signals
   and internal states addressed").
3. `## Glossary terms introduced`
4. `## Analogies worth reusing`
5. `## Source-stated confidence`
6. `## Conflicts with other sources`

Arbitrary additional `## ` sections may appear between #1 and #2 — the video's own argument
dictates what's needed there; nothing downstream requires or forbids specific extra headings.

Citation/anchor syntax inline in note prose — **[Verified]**, from `lib_common.py`:
- Bare `` `[mm:ss]` `` (or `[p.N]`, `[¶N]`) cites the note's own primary source.
- `` `other-source-id`[mm:ss] `` (backtick immediately followed by the bracket, no space) cites a
  *different* source, using that source's own declared anchor kind.
- A bare backtick-quoted 11-char id with no following anchor (`` `dQw4w9WgXcQ` ``) is a
  non-anchor-checked cross-reference — "related source," resolved by `check_notes.py` against
  notes/manifest/deferred but not validated against transcript text.

### `app/data/<slug>.json` — **[Verified]**, top-level keys produced by `build_app_data.py`

`videos` (per-note records: id, kind, evidence, title, url, dates, duration, every frontmatter
facet, parsed `sections`, `anchors` count, `images`), `library` (knowledge files split by
heading/subheading with `cited_ids`), `glossary`, `curated_symptoms`, `symptoms` (per-bullet,
with extracted timestamps and a `curated` match index or `null`), `practices` (per-card, with
derived `duration_seconds`/`duration_bucket`/`position`/`equipment` when
`derived_practice_facets` is on), `vocab` (per-facet term → list of video ids), `stats` (counts:
videos, library_files, glossary_terms, symptoms, practices, anchors), `meta` (slug, title,
subtitle, lede, about_paragraphs, splash_b64, primary_facet(+label), facets(+labels)).

---

## 8. Prompt templates / synthesis instructions

**[Verified]** There is no embedded LLM prompt anywhere in `scripts/` — confirmed by grepping
every import across all 25 files; no `openai`, `anthropic`, or similar SDK appears. Extraction and
synthesis are entirely human-authored. The two artifacts that function as "instructions" are:

1. **`CLAUDE.md`** (repo root) — the de facto extraction/synthesis spec a human (or an agent
   standing in for one) follows when writing a note or editing a knowledge file. Key excerpts
   (also reproduced structurally above): "The rule everything else serves" (anti-fabrication
   doctrine), "Writing the note" (schema + six universal sections + conventions: heavy direct
   quotation, an anchor on every substantive claim, tables where the source compares things, bold
   for the load-bearing sentence), and "After a note changes" (which knowledge files to consider
   updating and when). This file is the closest thing to a system prompt for the human-extraction
   step, but it is not fed to any model by the pipeline itself — it's operator documentation.

2. **`libraries/<slug>/PASTE_INTO_GPT_INSTRUCTIONS.txt`** — the literal system prompt pasted into
   each library's Custom GPT (per `README.md`: "Upload the files in `libraries/<slug>/knowledge/`
   and paste `libraries/<slug>/PASTE_INTO_GPT_INSTRUCTIONS.txt` as the system prompt"). This is
   the one place an LLM is actually instructed by this system, and it's a downstream consumption
   surface, not part of ingestion. Confirmed structure (nutrition's instance), by section, in
   order — content not reproduced beyond section names since it addresses that library's private
   subject matter:
   - Opening persona/scope paragraph
   - `## What this corpus actually is`
   - `## Core interaction model` (three named modes)
   - `## Purpose-first framing`
   - `## No fake scores`
   - `## Honesty constraint — an operating rule, not a caveat`
   - `## Citations` (explicitly states which files carry no video-ID citations "by design," and
     instructs resolving citations against `09_SOURCE_CATALOG.md` + notes)
   - `## Preserve confidence and hedges exactly`
   - `## Boundaries`
   - `## Routing` (maps question types to which knowledge file to consult)

   Referenced by `library.json`'s `custom_gpt.instructions_file` key; `custom_gpt.file_limit`
   (20) caps how many files from `knowledge/` get uploaded alongside it.

If a Codex-operated clone needs the equivalent of a "prompt template" for its own extraction step
(e.g. if that repo *does* want to automate extraction with an LLM, which this repo does not do),
`CLAUDE.md`'s "Writing the note" section is the correct seed text to adapt — see the Migration
Checklist.

---

## 9. Citation / provenance mechanism

**[Verified]**

- Every source in `sources/manifest.json` declares an `anchor` sub-schema (`kind`, `format`,
  `bound_field`, `bound`) — see §7. This is the single source of truth for what a valid citation
  into that source looks like and how far it can run.
- `lib_common.ANCHOR_KINDS` defines the regex/parsing for each anchor kind
  (`timestamp`/`page`/`paragraph`), used identically by `check_notes.py` and `build_app_data.py`.
- `find_anchor_citations(text, own_id)` walks a note's body for every bracketed anchor and
  resolves which source it cites (bare = own source; backtick-scoped = another source).
- **Validation** (`check_notes.py`, independently re-implemented inside `build_app_data.py`'s
  `load_notes()`): every citation must (a) resolve to a real source id, (b) match that source's
  declared anchor kind, (c) not exceed that source's declared bound, and (d) appear **verbatim**
  as a literal string inside that source's own `sources/clean/<id>.txt` text. This last check is
  the one `README.md` calls out explicitly as the failure mode that matters most: "A timestamp
  that is well-formed, inside the video's runtime, and absent from the transcript is a fabricated
  citation."
- **Resolution surface**: `knowledge/09_SOURCE_CATALOG.md` is the id → title/URL/date/duration
  lookup table for every source, auto-generated so it can never omit or misrepresent an ingested
  source (`build_catalog.py` refuses to build if any note references an id missing from the
  manifest).
- **Citation density is uneven by design** (`README.md`): numbered synthesis files (`01`–`08`,
  etc.) carry no source-id citations at all; `topic_reference_*.md` files do; notes carry every
  anchor. This is a deliberate anti-fabrication boundary, not an oversight — a synthesis page
  cannot silently attribute a claim to a source it doesn't actually cite.
- Non-11-char-id sources (PDF/website/EPUB) are cited via the same bracket-anchor mechanism, not
  the bare-backtick-11-char shortcut, since `BACKTICK_ID_RE` is deliberately narrow to the YouTube
  id shape; any id shape is accepted for a citation as long as it's paired with an anchor
  (`SCOPED_PREFIX_RE`).

---

## 10. Deduplication, incremental ingestion, updating, rebuilding

**[Verified]**

- **YouTube link registration** (`add_videos.py`): four-bucket classification — already
  fetched (raw files on disk) / already listed (in `video_ids_full.txt` but not yet downloaded) /
  previously excluded (in `excluded_videos.tsv`) / new. A previously-excluded id pasted again is
  treated as an explicit operator override and gets re-queued.
- **Fetch idempotency**: `yt-dlp --no-overwrites --ignore-errors` — never re-downloads an existing
  file, and one bad id in a batch doesn't abort the rest.
- **Manifest upsert pattern**, used identically by every `add_website.py`/`add_pdf.py`/
  `add_epub.py`/`add_instagram_reel.py`/`add_local_video.py`/`add_video_whisper.py`: filter out any
  existing entry with the same id, append the fresh one, re-sort, save — safe to re-run for the
  same id, always overwrites rather than duplicates.
- **`normalize.py`'s manifest rebuild** explicitly preserves non-YouTube and whisper-transcribed
  entries across every re-run (see §4) so re-running it never silently drops manually-ingested
  sources.
- **Backlog derivation**: "what needs a note" is never stored as an independent authoritative
  list — it's recomputed every `add.sh` run as `fetched minus (has a note OR is deferred)`, then
  cached to `ingest_state/notes_todo.txt` only "so the list survives the shell session" (comment
  in `add.sh`).
- **Batch Whisper resumability**: `add_videos_whisper.py` explicitly checks
  `not (lib.clean_dir / f"{vid}.txt").exists()` before transcribing, and documents itself as
  "Safe to Ctrl-C and re-run — each video's clean file + manifest entry is written before moving
  to the next, so nothing is half-done on disk."
- **Rebuild determinism**: `build_catalog.py` and `build_app_data.py` are both fully deterministic
  — re-running with no input change produces byte-identical output (sorted JSON keys, `mtime=0` on
  gzip, alphabetical catalog ordering). This makes `git status --porcelain` after a rebuild a
  reliable signal of "did anything actually change."
- **`publish.sh`'s no-op path**: if `git status --porcelain` is empty after all three build steps,
  it prints "Nothing to publish — no files changed." and exits 0 without committing.
- **Knowledge-file staleness is an explicit, accepted, tracked condition** — `09_SOURCE_CATALOG.md`
  is the only knowledge file that auto-regenerates; every other knowledge file "lags the notes by
  one video" until a human judges an update is warranted (`README.md`/`CLAUDE.md`, "After a note
  changes"). There is no automated staleness detector for this — it's a manual judgment call by
  design.

---

## 11. How the system determines what has already been processed

**[Verified]**

| Question | Source of truth |
|---|---|
| Has this source been fetched? | `sources/raw/<id>.*` files exist (YouTube) — checked by `add_videos.py`'s `fetched` set |
| Is this source known to the corpus at all (fetched or not)? | `sources/manifest.json`'s `sources[]`/`skipped[]`, and `ingest_state/video_ids_full.txt` for YouTube specifically |
| Has this source been written up? | a `notes/<id>.md` file exists — `{p.stem for p in lib.notes.glob("*.md")}` |
| Was this source deliberately excluded from note-writing? | its id/token appears in `deferred_sources.txt` (substring/token scan, not exact line match) |
| Was this YouTube id deliberately excluded from ingestion entirely (never fetched)? | `ingest_state/excluded_videos.tsv` |
| What still needs a note? | derived, not stored: `manifest.sources - (notes ∪ deferred)`, recomputed every `add.sh` run, cached in `ingest_state/notes_todo.txt` |

---

## 12. Environment / dependencies / configuration

**[Verified]** There is **no dependency manifest anywhere in this repo** — no
`requirements.txt`, `Pipfile`, `pyproject.toml`, `package.json`, `environment.yml`, or lockfile of
any kind. No Python version is pinned. This is a real gap for reproduction (see §17's sufficiency
verdict): a Codex clone will need a hand-assembled dependency list, not a manifest to copy.

Third-party Python packages actually imported (all as lazy/inline imports except `yaml` in
`build_catalog.py`, which is a top-level import):
- `yaml` (PyYAML) — frontmatter parsing (`build_catalog.py`, `check_notes.py`)
- `instaloader` (+ `instaloader.exceptions.LoginRequiredException`) — Instagram ingestion
- `trafilatura` — web-page text extraction
- `pypdf` — PDF text extraction
- `pdf2image`, `pytesseract` — PDF OCR fallback (also requires the `tesseract` and `poppler` system
  binaries, which those Python packages wrap — not verified directly in this pass, standard
  requirement for those libraries **[Inferred]**)
- `bs4` (BeautifulSoup4) — EPUB HTML parsing
- `whisper` (`openai-whisper` — note: this is the local, open-weights transcription package, **not**
  the OpenAI hosted API; no network call, no API key)

External CLI tools invoked via `subprocess`/shell:
- `yt-dlp` — YouTube caption/audio fetch, channel listing
- `ffprobe` / `ffmpeg` — duration probing and frame/cover extraction (Instagram, local video)
- `git` — status/add/commit/push (`publish.sh`)

**[Documented]**, `CLAUDE.md`'s only explicit install instruction:
```
pip3 install instaloader                                   # once per machine
instaloader --login <your-instagram-username>               # once per machine, saves a session file
```

No CI config exists (`[Verified]`: no `.github/workflows` directory anywhere in the repo).
GitHub Pages deploys automatically from `main` at the repo root on every push — no build step runs
server-side; `publish.sh` does the entire build locally before pushing.

---

## 13. Secrets, API keys, environment variables

**[Verified]** Repo-wide search of every `scripts/*.py` and `scripts/*.sh` for `os.environ`,
`os.getenv`, and shell `$VARNAME` config patterns found exactly **one** environment variable read
anywhere:

| Variable | File / line | Purpose |
|---|---|---|
| `DEVELOPMENT_TEAM` | `scripts/make_xcodeproj.py:19` — `os.environ.get("DEVELOPMENT_TEAM", "976XKW42U9")` | Apple Developer Team ID for iOS codesigning in the generated Xcode project. Has a hardcoded personal-account fallback baked in; not treated as a secret in this repo, but a Codex clone should still parameterize it via env var rather than hardcoding a new default. |

No other environment variables, `.env` file (none exists, none expected — `.gitignore` has no
`.env` entry), or API keys of any kind are used anywhere in the ingestion pipeline:
- YouTube fetch (`yt-dlp`) is unauthenticated public scraping — no key.
- Whisper transcription is fully local (`openai-whisper` package) — no key, no network call.
- Instagram auth is a **saved session file on disk** at `~/.config/instaloader/`, created once via
  `instaloader --login <username>` (interactive password prompt) and reused thereafter via
  `--login <username>` — this is a local credential file, not an environment variable, and it is
  not part of the repo (never committed, lives outside the repo in the user's home directory).
- `git push` relies on the operator's local git/SSH credentials — nothing repo-specific.

**For a Codex clone**: no secrets need to be provisioned to reproduce this exact pipeline. If the
new repo adds an LLM-driven extraction step (which this repo does not have), that would introduce
the first real API-key requirement (e.g. `ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) — out of scope for
this handoff since it doesn't exist in the source system.

---

## 14. Failure modes and recovery behavior

**[Verified]**

| Script | Failure-tolerance strategy |
|---|---|
| `add.sh` | `set -uo pipefail` (no `-e`) — deliberately keeps running through a substep's failure so the operator sees a full report; only a missing library directory is a hard `exit 1` |
| `fetch_transcripts.sh` | `yt-dlp --ignore-errors --no-overwrites` — one bad video in a batch doesn't abort the fetch, and re-running never re-downloads |
| `normalize.py` | per-video: a missing/empty transcript goes to `manifest["skipped"]` with a `reason`, not a crash; hard-exits only if `raw/` has zero `.info.json` files at all |
| `add_videos_whisper.py` | per-video `try/except Exception` (batch continues; failures collected and reported at the end); explicitly documented as Ctrl-C-safe and resumable |
| `check_notes.py` | never crashes on a bad note — collects `problems` per note, prints `FAIL <id>`, and exits 1 overall if any note failed; this is the intended way to discover a bad note before it reaches `publish.sh` |
| `build_catalog.py` | refuses to write the catalog at all if any note's id is missing from the manifest — `sys.exit(1)` with the full problem list, no partial file |
| `build_app_data.py` | refuses to write anything for a library with validation problems (missing sections, unresolvable anchors, out-of-bound anchors) — `sys.exit(1)`, up to 40 problems printed |
| `publish.sh` | `set -euo pipefail` — any of the three build scripts exiting nonzero aborts the whole publish immediately, before `git add`/`commit`/`push` ever runs. This is the load-bearing safety property of the whole pipeline: **a malformed note cannot reach the published app or the git history via the normal workflow**, because the build step it would need to pass through refuses to run |

**Recovering from a halfway failure**: because every fetch/normalize step is either idempotent
(`--no-overwrites`, manifest upsert-by-id) or additive-only, the safe recovery action after any
failure is simply **re-run the same command**. There is no "clean up partial state" step required
anywhere in this pipeline — this is a deliberate design property, not incidental. The one
exception to check manually: `ingest_state/video_ids_added.txt` is deleted at the start of every
`add.sh` run specifically so a stale batch can't silently re-fetch the previous slate — if a
user interrupts `add.sh` mid-run and wants to resume the *same* batch rather than re-pasting links,
they'd need to reconstruct that file by hand or just re-paste, since `add.sh` doesn't preserve it
across runs by design.

---

## 15. Tests / validation

**[Verified]** There is no separate automated test suite — no `tests/` directory, no `pytest`
config, no CI. **Validation is a first-class pipeline stage** (`check_notes.py`), not a
development-time test suite, and it is re-implemented (independently) inside `build_app_data.py`
so the app build itself cannot silently absorb a note that `check_notes.py` would have failed.

An ingest is considered "successful" when:
1. `check_notes.py <slug> <id>` exits 0 for the new note (all universal sections present, all
   frontmatter facets present, all controlled-vocabulary values valid, all image references
   exist, all anchor citations resolve/match-kind/in-bound/verbatim-in-source, all cross-references
   resolve).
2. `publish.sh` completes without any of the three build steps exiting nonzero.
3. (Optional, advisory only, does not gate success) `check_notes.py <slug> --terms` review of any
   newly-introduced glossary terms, to catch imported terminology or caption-garbling.

There is no runtime/integration test of the produced `app/index.html` beyond what's implicit in
`build_app_data.py`'s own internal consistency checks (frontmatter-vs-manifest, section presence,
anchor resolution) — **[Inferred]** manual visual verification in a browser is presumably how the
app itself gets checked, since nothing in `scripts/` renders or screenshots it.

---

## 16. Git behavior

**[Verified]** `.gitignore` at repo root, ingestion-relevant lines quoted verbatim:

```gitignore
# Raw ingest dumps (yt-dlp captions, fetched HTML, source PDFs/EPUBs) — large,
# regenerable from each library's sources/manifest.json. The cleaned text in
# each library's sources/clean/ is the provenance record.
libraries/*/sources/raw/

# Transient fetch batch, rewritten by add_videos.py on every run.
libraries/*/ingest_state/video_ids_added.txt
```

Also present (not ingestion-specific but repo hygiene): `/ebook/` and
`/Georges St-Pierre Rushfit Workout Program/` (purchased source media staged for `add_pdf.py`/
`add_epub.py`/`add_local_video.py` before ingestion — "never committed, these are often
copyrighted works the user owns a personal copy of"), `.DS_Store`, `__pycache__/`, `*.pyc`,
`.venv/`, `venv/`, `ios/build/`, `ios/**/xcuserdata/`, `*.xcuserstate`, `/repo-analysis.md`.

**Committed** (everything not listed above): `sources/clean/*.txt`, `sources/manifest.json`,
`sources/images/`, `notes/*.md`, `knowledge/*.md` (including the auto-generated catalog),
`ingest_state/*` except `video_ids_added.txt`, `deferred_sources.txt`, `icon.b64`/`splash.b64`,
`PASTE_INTO_GPT_INSTRUCTIONS.txt`, `overrides.json` (where present), `app/index.html`,
`app/data/*.json`, `app/app.template.html`, `app/sound.b64`, `ios/PolymerPhD.xcodeproj/`,
`ios/PolymerPhD/Resources/index.html`.

**Should stay local, never committed**: `sources/raw/` (gitignored, regenerable — ~300 MB across
all libraries per repo memory), `ingest_state/video_ids_added.txt` (gitignored, transient),
purchased source media staged under `/ebook/` or similar (gitignored, copyrighted personal
copies), Python `__pycache__`, Xcode build artifacts.

**Commit pattern**: `publish.sh --push` produces commit messages of the exact form
`"Add ${NEW} note(s) and rebuild outputs"` where `NEW` is the count of untracked (`??`) files
under any `libraries/*/notes/` at commit time — so this count only reflects brand-new notes, not
edits to existing ones. One `git add -A` bundles the new note(s) together with every rebuilt
output (catalog, app data, app shell, Xcode project) into a single commit; there is no separate
commit-per-artifact-type.

---

## 17. Worked example — one real source, raw → knowledge

**[Verified]** Library `dupuytren`, YouTube video id `_hoXDJ5qBFU`.

**1. Raw fetch** — `libraries/dupuytren/sources/raw/`:
`_hoXDJ5qBFU.en.json3`, `_hoXDJ5qBFU.en-orig.json3`, `_hoXDJ5qBFU.info.json` (gitignored, present
locally). No video/audio file — captions + metadata only, per `fetch_transcripts.sh`'s
`--skip-download`.

**2. Clean transcript** — `libraries/dupuytren/sources/clean/_hoXDJ5qBFU.txt`, first lines:
```
TITLE: Drs. Wolfgang Wach and Charles Eaton: "Welcome!" 2015 Dupuytren Symposium
VIDEO ID: _hoXDJ5qBFU
URL: https://www.youtube.com/watch?v=_hoXDJ5qBFU
UPLOAD DATE: 2015-10-25
DURATION: 08:47
CAPTION TRACK: en-orig
======================================================================

[00:00] ah excellent okay so welcome to all of you and on behalf of the...
```

**3. Manifest entry** — `libraries/dupuytren/sources/manifest.json`:
```json
{
  "id": "_hoXDJ5qBFU",
  "kind": "youtube",
  "title": "Drs. Wolfgang Wach and Charles Eaton: \"Welcome!\" 2015 Dupuytren Symposium",
  "url": "https://www.youtube.com/watch?v=_hoXDJ5qBFU",
  "upload_date": "2015-10-25",
  "duration_seconds": 527,
  "duration": "08:47",
  "word_count": 1191,
  "clean_file": "clean/_hoXDJ5qBFU.txt",
  "anchor": {"kind": "timestamp", "format": "mm:ss", "bound_field": "duration_seconds", "bound": 527}
}
```

**4. Note** — `libraries/dupuytren/notes/_hoXDJ5qBFU.md`, structure only:
```yaml
---
id: _hoXDJ5qBFU
title: "Drs. Wolfgang Wach and Charles Eaton: \"Welcome!\" 2015 Dupuytren Symposium"
url: https://www.youtube.com/watch?v=_hoXDJ5qBFU
upload_date: 2015-10-25
duration: "08:47"
subjects: [...]
management: []
anatomy: []
concepts: [...]
---
# Drs. Wolfgang Wach and Charles Eaton: "Welcome!" 2015 Dupuytren Symposium
## Central claim
## Two ideas offered as "food for thought"
## The society structure
## Eaton's framing: a bridge, and a team, not a hero
## Symptoms and body signals addressed
## Glossary terms introduced
## Analogies worth reusing
## Source-stated confidence
## Conflicts with other sources
```
(`management`/`anatomy` are two of `dupuytren`'s `facets`, alongside `subjects`/`concepts`; the
three video-specific sections between "Central claim" and "Symptoms..." are this note's own,
called for by this particular video's argument.)

**5. Catalog entry** — `libraries/dupuytren/knowledge/09_SOURCE_CATALOG.md`, entry #86:
```
## 86. Drs. Wolfgang Wach and Charles Eaton: "Welcome!" 2015 Dupuytren Symposium

- **Source ID:** `_hoXDJ5qBFU`
- **URL:** https://www.youtube.com/watch?v=_hoXDJ5qBFU
- **Upload date:** 2015-10-25
- **Duration:** 08:47
- **Source file:** `sources/clean/_hoXDJ5qBFU.txt`
```

**6. Knowledge-file citation** — `dupuytren` has no `topic_reference_*.md` files (its `knowledge/`
only runs `00_README.md` through `09_SOURCE_CATALOG.md`), so this id appears **only** in the
catalog — consistent with the "notes carry every citation, numbered synthesis files carry none"
rule; there's nothing further downstream to trace for this particular source.

**7. Ingest-state trace** — `libraries/dupuytren/ingest_state/video_ids_full.txt` line 82:
`https://www.youtube.com/watch?v=_hoXDJ5qBFU`. `git log -p --follow` on that file shows this URL
added as a `+` line in commit `34d18f6`.

**8. Git history** — two separate commits cover this one source's full lifecycle:
```
34d18f6  Add 68 note(s) and rebuild outputs   — fetch/normalize stage: raw+clean+manifest+id-list
d49cd77  Add 22 note(s) and rebuild outputs   — note-writing + catalog rebuild + publish stage
```
`git show --stat d49cd77` touches this note plus `09_SOURCE_CATALOG.md`, `deferred_sources.txt`,
and the rebuilt `app/data/dupuytren.json`/`app/index.html`/`ios/` files — exactly the bundle
`publish.sh --push`'s single `git add -A` + one commit produces.

---

## Codex Migration Checklist

Dependency-ordered list of files/directories to copy or recreate in a clean repo. Items later in
the list depend on items earlier in the list (imports, or being invoked by, an earlier item).

1. **`scripts/lib_common.py`** — copy verbatim. Everything else imports it; nothing else can run
   without it.
2. **`scripts/add.sh`, `scripts/fetch_transcripts.sh`, `scripts/add_videos.py`,
   `scripts/normalize.py`** — copy verbatim. This is the core YouTube ingestion loop and has no
   library-specific content baked in (all slug-parameterized).
3. **`scripts/check_notes.py`** — copy verbatim. Validation gate; depends only on `lib_common.py`.
4. **`scripts/build_catalog.py`** — copy verbatim. Depends only on `lib_common.py`; guard its
   entry point (`if __name__ == "__main__":`) is required since `build_app_data.py` imports from
   it.
5. **`scripts/build_app_data.py`, `app/app.template.html`, `app/sound.b64`** — copy verbatim
   (imports `build_catalog.py` and `lib_common.py`). The app build needs the template and sound
   asset present or it exits with a clear error; `derived_practice_facets`-gated regex heuristics
   inside are tuned to `restorative-physiology`'s prose and can be left disabled (default) for a
   new library.
6. **`scripts/publish.sh`, `scripts/make_xcodeproj.py`** — copy verbatim if the iOS delivery path
   is wanted; `publish.sh` alone (without `make_xcodeproj.py`) still works if the iOS build step is
   simply removed from its sequence. `make_xcodeproj.py` needs `DEVELOPMENT_TEAM` set (env var or
   a new hardcoded default for the new Apple account) if iOS builds are wanted.
7. **Source-kind-specific scripts, as needed** — `add_website.py`, `add_pdf.py`, `add_epub.py`,
   `add_instagram_reel.py`, `add_local_video.py`, `add_video_whisper.py`, `add_videos_whisper.py`.
   Each is independent of the others; copy only the ones the new corpus actually needs. All depend
   only on `lib_common.py` plus their own third-party package (see §12).
8. **Ancillary/optional tooling** — `list_channel.py` (generic, safe to copy as-is);
   `classify_channel.py` and `check_gaps.py` (hardcoded to one library's slug/exclusion-list —
   copy only as a *template* to rewrite for the new library, not as-is); `build_custom_gpt_bundle.py`
   (generic, safe to copy as-is); `slice_sections.py`/`slice_matching.py` (hardcoded + not
   importable — copy as a template for a synthesis-staging helper if the new repo's synthesis
   workflow wants one).
9. **A `library.json` template** — copy `libraries/nutrition/library.json` as the starting point
   (free-form facets, no controlled vocabulary) per `CLAUDE.md`'s own "Adding a library"
   instructions, or `libraries/restorative-physiology/library.json` if the new library needs a
   controlled facet vocabulary. Edit `slug`, `title`, `subtitle`, `facets`, `primary_facet`,
   `universal_sections`, `attribution`, `custom_gpt`.
10. **Per-new-library directory scaffold** — `mkdir -p libraries/<slug>/{notes,knowledge,
    sources/{clean,raw},ingest_state}` + `touch libraries/<slug>/deferred_sources.txt`, plus
    `icon.b64`/`splash.b64` (base64 PNG data, no `data:` prefix) and, if Custom GPT export is
    wanted, a `PASTE_INTO_GPT_INSTRUCTIONS.txt` written for that library's own subject matter
    (structure to mirror: persona/scope, corpus description, interaction model, citation-honesty
    rules, confidence-preservation rule, boundaries, routing — see §8).
11. **Root `.gitignore`** — copy the ingestion-relevant lines from §16 (`sources/raw/`,
    `ingest_state/video_ids_added.txt`) plus standard Python/OS ignores.
12. **`CLAUDE.md`'s "Writing the note" and "The rule everything else serves" sections** — adapt as
    the new repo's own operating instructions; this is prose guidance for whoever (human or agent)
    writes notes, not executable code, but it is the actual specification of the note schema and
    the anti-fabrication discipline that `check_notes.py` enforces mechanically. Reproducing the
    validator without this prose would leave the *rules* implicit in code with no stated rationale
    for a new operator to follow when the validator doesn't catch something (e.g. imported
    terminology, which is only advisory-checked).
13. **New: a journal-ingestion script** — if the target corpus is personal journals (as stated for
    this migration), none of `add_website.py`/`add_pdf.py`/`add_epub.py`/`add_instagram_reel.py`/
    `add_local_video.py` fit as-is; write a new `add_journal.py` following the same manifest-upsert
    pattern (§10) and paragraph/date-anchor convention (§9), modeled most closely on
    `add_epub.py` (local file, no network fetch, paragraph-anchored) or `add_website.py` (manifest/
    evidence shape). This is new code Codex must write, not a file to transfer — flagged here so
    it isn't mistaken for something already covered by items 1–12.

---

## Sufficiency verdict

**This document alone is not sufficient for Codex to reproduce the system.** It describes every
script's behavior precisely enough to reimplement each one from scratch, but reimplementation from
prose is slower and more error-prone than transferring working code, and several exact regex
patterns, template strings, and object-id-generation schemes (e.g. `make_xcodeproj.py`'s
`project.pbxproj` template, `normalize.py`'s boilerplate-stripping regex list,
`build_app_data.py`'s practice-facet heuristics) are load-bearing in ways that are fully described
above but non-trivial to retype correctly by hand.

**Transfer these files verbatim alongside this handoff document** (this list is the Migration
Checklist above, restated as a flat copy list):

```
scripts/lib_common.py
scripts/add.sh
scripts/fetch_transcripts.sh
scripts/add_videos.py
scripts/normalize.py
scripts/check_notes.py
scripts/build_catalog.py
scripts/build_app_data.py
scripts/publish.sh
scripts/make_xcodeproj.py            (if the iOS delivery path is wanted)
app/app.template.html
app/sound.b64
scripts/add_website.py               (if web/PubMed sources are wanted)
scripts/add_pdf.py                   (if PDF sources are wanted)
scripts/add_epub.py                  (if EPUB sources are wanted)
scripts/add_instagram_reel.py        (if Instagram sources are wanted)
scripts/add_local_video.py           (if local-video sources are wanted)
scripts/add_video_whisper.py         (if caption-less-YouTube/Whisper fallback is wanted)
scripts/add_videos_whisper.py        (batch wrapper for the above)
scripts/list_channel.py              (if channel pre-ingestion triage is wanted)
scripts/build_custom_gpt_bundle.py   (if multi-library GPT bundling is wanted)
libraries/nutrition/library.json     (as a schema template — do not copy its content, just its shape)
```

Also needed but not copyable — must be newly authored for the target repo, using the schemas and
examples in §6–§8 as the spec:
- A `library.json` for each new library (§7).
- A `PASTE_INTO_GPT_INSTRUCTIONS.txt` per library, if Custom GPT export is wanted (§8).
- `icon.b64`/`splash.b64` per library.
- A dependency list for the target environment (§12) — there is no manifest to copy, since none
  exists in the source repo either; this is a genuine gap in the source system, not something
  omitted from this handoff.
- `CLAUDE.md`'s "Writing the note" section, adapted into the new repo's own operating
  instructions (§8, Migration Checklist item 12).
