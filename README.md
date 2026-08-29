# Polymer Ph.D.

A knowledge base built from YouTube transcripts, one library per source channel — restorative
physiology, nutrition, Dupuytren's contracture, and others as they're added — and three ways to
use each one.

**Nothing in this repository originates outside the source transcripts.** Every claim traces to
a specific video at a specific second. That constraint is the point of the whole project, and
each delivery path below preserves it.

---

## What's here

| Path | What it is |
|---|---|
| `libraries/<slug>/` | One directory per library. Everything below is per-library unless noted |
| `libraries/<slug>/library.json` | That library's config: facets, controlled vocab, section headings, attribution, Custom GPT settings |
| `libraries/<slug>/sources/` | Raw and cleaned transcripts, plus `manifest.json` — the authoritative video metadata |
| `libraries/<slug>/notes/` | Structured notes, one per video. Identical schema within a library: frontmatter facets and six universal sections |
| `libraries/<slug>/knowledge/` | The synthesised knowledge files. This is the Custom GPT upload set for that library |
| `libraries/<slug>/deferred_sources.txt` | Video ids intentionally excluded from notes (out of scope for that library), one per line |
| `libraries/<slug>/PASTE_INTO_GPT_INSTRUCTIONS.txt` | That library's Custom GPT system prompt |
| `app/` | The offline reference app — one self-contained HTML file bundling every library |
| `ios/` | An Xcode project wrapping that file as a native iOS app |
| `scripts/` | The build pipeline, shared across all libraries |

## The libraries

| Slug | Title | Source |
|---|---|---|
| `restorative-physiology` | Restorative Physiology ("The Feynman Way") | [The Feynman Way](https://www.youtube.com/@The_Feynman_Way) |
| `nutrition` | Nutrition | [Paul Saladino MD](https://www.youtube.com/@Paulsaladinomd) |
| `dupuytren` | Dupuytren | [Dupuytren Foundation](https://www.youtube.com/@DupuytrenFoundation) + clinical guidelines/studies |

Exact video/note counts drift as libraries grow — each library's own
`knowledge/09_SOURCE_CATALOG.md` is the current, authoritative count; `libraries/<slug>/library.json`
carries its `title`/`subtitle`/`attribution`.

## How it was built

Two stages, deliberately separated, run independently per library:

1. **Extraction.** Each transcript read once and turned into a structured note preserving
   mechanisms, doses, glossary terms, symptoms, the source's own confidence statements, and
   `[mm:ss]` anchors back to the video.
2. **Synthesis.** That library's knowledge files written **from its own notes, never from raw
   transcripts.**

That separation is the anti-fabrication mechanism: if a claim is not in a note, it does not
appear anywhere downstream.

---

## The three delivery paths

All three are built from the same corpus. The web app is also published, so it can be opened
without installing anything:

**<https://polymerjones.github.io/polymerphd/>** — GitHub Pages, served from `main` at the
repository root, where a small `index.html` redirects to `app/index.html`. It redeploys about a
minute after any push. The app needs iOS 16.4+ or macOS 13.3+, because it unpacks its data with
`DecompressionStream`; on anything older the page opens blank.

### 1. Custom GPT (one per library)

Upload the files in `libraries/<slug>/knowledge/` and paste
`libraries/<slug>/PASTE_INTO_GPT_INSTRUCTIONS.txt` as the system prompt. Each library is scoped
to fit inside the Custom GPT 20-file knowledge limit.

### 2. Offline web app — `app/index.html`

One self-contained file, ~2.5 MB. Double-click it. Works offline permanently, makes zero
network requests, and contains no model — it surfaces the existing synthesis and never
generates. Five surfaces: Search, Practices, Symptoms, Sources, Reference.

```
python3 scripts/build_app_data.py
```

Emits `app/data.json` (the dataset alone, for any future consumer) and `app/index.html` (the
same data gzipped and inlined into `app/app.template.html`). See `app/README.md`.

To read it on a phone without building the iOS app, serve it over the local network:

```
python3 -m http.server 8000 --directory app
ipconfig getifaddr en0        # the address to open on the phone
```

### 3. Native iOS app — `ios/`

A WKWebView wrapper around the same file, bundled inside the app so it works in airplane mode.

```
python3 scripts/build_app_data.py     # rebuild the web app
python3 scripts/make_xcodeproj.py     # regenerate the project, sync the bundled copy
```

Then open `ios/PolymerPhD.xcodeproj`, set a signing team, and ⌘R. A free Apple ID works, with
a 7-day expiry. See `ios/README.md`.

---

## Adding a new video

Four stages, run against one library's slug (a directory name under `libraries/`). Only the
second is judgement; the rest is plumbing.

```
bash scripts/add.sh <slug> https://youtu.be/XXXXXXXXXXX   # 1. fetch + normalize, then list what needs a note
                                                            # 2. write libraries/<slug>/notes/<id>.md by hand
python3 scripts/check_notes.py <slug> <id>                 # 3. validate before building
bash scripts/publish.sh --push                              # 4. rebuild ALL libraries and ship
```

**Stage 1** is safe to re-run and safe to paste duplicates into — `add_videos.py` sorts every id
into *already fetched*, *already listed*, *previously excluded* or *new*, so nothing is silently
dropped or re-downloaded. Captions only; no video or audio.

**Stage 2** is the extraction pass. Read `libraries/<slug>/sources/clean/<id>.txt` once and write
the note: that library's frontmatter facets, its six universal sections (headings declared in
`library.json`), whatever video-specific sections the argument calls for in between, and an
`[mm:ss]` anchor on every substantive claim. If a video is out of scope for the library, add its
id to `libraries/<slug>/deferred_sources.txt` instead — a deferred id remains a legitimate
cross-reference.

**Stage 4** regenerates every library's `09_SOURCE_CATALOG.md` automatically, across all of
`libraries/*/`. **The other knowledge files do not update themselves** — they were synthesised by
hand from the notes, and whether a new video changes them is a judgement call each time. Skipping
it is not wrong; it means the synthesis lags the notes by one video.

Starting a brand-new library (a channel that's never been ingested before) is a manual, one-time
setup — see "Adding a library" in `CLAUDE.md`.

---

## Scripts

Every script below except `publish.sh`, `build_app_data.py`, and `make_xcodeproj.py` takes a
`<slug>` as its first argument (a directory name under `libraries/`) — those three operate over
every library at once.

| Script | Purpose |
|---|---|
| `add.sh <slug>` | **Adding a video — one command.** Wraps the ingestion scripts and reports what still needs a note |
| `publish.sh` | **Shipping — one command.** Rebuilds every library's catalog, the app, and the Xcode project, then pushes with `--push` |
| `check_notes.py <slug>` | Validates that library's notes against its schema and the provenance rules |
| `lib_common.py` | Shared `Library` class — resolves per-slug paths/config; not run directly |
| `fetch_transcripts.sh <slug>`, `add_videos.py <slug>`, `normalize.py <slug>` | YouTube ingestion |
| `add_pdf.py <slug>`, `add_website.py <slug>` | Non-video source ingestion (PDF, web page) |
| `list_channel.py`, `classify_channel.py`, `check_gaps.py` | Channel listing, triage, and caption-gap detection |
| `slice_sections.py`, `slice_matching.py` | Read one dimension across a library's notes (staging for the synthesis pass) |
| `build_catalog.py <slug>` | Generates that library's `09_SOURCE_CATALOG.md` from note frontmatter |
| `build_app_data.py` | Generates the offline app for all libraries |
| `make_xcodeproj.py` | Generates the Xcode project |

`build_catalog.py` and `build_app_data.py` both refuse to write if a note's id is missing from
the manifest, a universal section is missing, or a timestamp runs past the end of its video.
Both are deterministic: re-running without changing an input produces byte-identical output.

`check_notes.py` runs the same class of checks earlier, plus the one that matters most here:
**every `[mm:ss]` anchor must appear verbatim in the transcript it cites.** A timestamp that is
well-formed, inside the video's runtime, and absent from the transcript is a fabricated citation —
the one failure this package cannot absorb, and the one the other guards do not catch.

```
python3 scripts/check_notes.py <slug>              # all notes in that library
python3 scripts/check_notes.py <slug> <video_id>   # one
```

> `slice_sections.py` and `slice_matching.py` read `sys.argv` at module level and cannot be
> imported. `build_catalog.py` guards its entry point and is safely importable —
> `build_app_data.py` reuses its `parse_frontmatter()` and `as_list()`.

---

## Two things the app is deliberately honest about

(The specifics below describe `restorative-physiology`; the same pattern — numbered files with no
citations, `topic_reference_*` files that carry them, notes that carry all the anchors — repeats
in every library, with different file counts and numbers per library.)

**Citation density is uneven.** Files `01`–`08` carry **no** video-ID citations. The nine
`topic_reference` files carry 228 between them. The notes carry all 16,631 timestamps. So the
app renders live citations on notes and topic references, and never fabricates one on a
synthesis page. Related sources shown there are labelled *by tag*, not as claim-level citations.

**The practice filters are derived and partial.** Duration, position and equipment are
pattern-matched out of the source's own wording: of 713 practices, 144 state a readable
duration, 19 a seated cue, 6 "no equipment." Misses are listed in
`app/unclassified_practices.txt` and can be corrected by hand in `app/practice_overrides.json`.
The raw source string always appears on the card, so a filter can never hide what the material
actually said.

## Boundaries

These come from the source material itself and are reproduced in both the GPT prompt and the
app: do not diagnose; do not advise starting, stopping or re-timing any medication; reproduce
stated contraindications with the practice rather than after it. Emergency signals — stroke,
cauda equina, first episode of chest pain — are stated without softening. See
`PASTE_INTO_GPT_INSTRUCTIONS.txt` and `topic_reference_09_MEDICATION_INTERACTIONS.md`.

## Source and attribution

Every transcript, note and synthesised file in this repository derives from its named source.
The `restorative-physiology` library derives from
**[The Feynman Way](https://www.youtube.com/@The_Feynman_Way)**. The `nutrition` library derives
from **[Paul Saladino MD](https://www.youtube.com/@Paulsaladinomd)**. The `dupuytren` library's
video notes derive from **[Dupuytren Foundation](https://www.youtube.com/@DupuytrenFoundation)**;
its other sources (clinical guidelines, systematic reviews, patient material) are cited
individually in `libraries/dupuytren/sources/manifest.json` and its own source catalog. Each
library's exact source count and runtime is in its own `library.json` and
`knowledge/09_SOURCE_CATALOG.md`. All rights in the underlying material remain with the
respective channel or publisher.

This is a personal, non-commercial study aid. It is not affiliated with or endorsed by either
channel, and nothing here is presented as original writing. The `[mm:ss]`/`[p.N]`/`[¶N]`
anchors exist so that any claim can be checked against the source that made it — the material
is meant to be watched or read, not replaced. If you find this useful, watch and subscribe to
the source channels.
