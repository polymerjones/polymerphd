# Polymer Ph.D.

A knowledge base built from 190 YouTube transcripts on restorative physiology, the biology of
ageing, and the mechanisms behind everyday health practices — and three ways to use it.

**Nothing in this repository originates outside the source transcripts.** Every claim traces to
a specific video at a specific second. That constraint is the point of the whole project, and
each delivery path below preserves it.

---

## What's here

| Path | What it is |
|---|---|
| `source_transcripts/` | The raw and cleaned transcripts, plus `manifest.json` — the authoritative video metadata for all 224 fetched videos |
| `notes/` | 190 structured notes, one per video. Identical schema throughout: four frontmatter facets and six universal sections |
| `restorative_vitality_knowledge/` | The 20 synthesised knowledge files. This is the Custom GPT upload set |
| `app/` | The offline reference app — one self-contained HTML file |
| `ios/` | An Xcode project wrapping that file as a native iOS app |
| `scripts/` | The build pipeline |
| `PASTE_INTO_GPT_INSTRUCTIONS.txt` | The Custom GPT system prompt |

## The corpus, in numbers

| | |
|---|---|
| Videos on the channel | 280 |
| Health/body videos fetched | 224 |
| Written up as notes | **190** (34 deferred as physics-framed) |
| Total words across the notes | 573,666 |
| `[mm:ss]` source anchors | **16,272**, in all 190 notes |
| Symptom bullets catalogued | 1,152 |
| Practice strings | 703, across 179 notes |
| Body systems (controlled vocabulary) | 10 |
| Glossary terms | 146 |
| Source runtime | ~89 hours |

## How it was built

Two stages, deliberately separated:

1. **Extraction.** Each transcript read once and turned into a structured note preserving
   mechanisms, doses, glossary terms, symptoms, the source's own confidence statements, and
   `[mm:ss]` anchors back to the video.
2. **Synthesis.** The 20 knowledge files written **from the 190 notes, never from raw
   transcripts.**

That separation is the anti-fabrication mechanism: if a claim is not in a note, it does not
appear anywhere downstream.

---

## The three delivery paths

### 1. Custom GPT

Upload the 20 files in `restorative_vitality_knowledge/` and paste
`PASTE_INTO_GPT_INSTRUCTIONS.txt` as the system prompt. Twenty files is exactly the Custom GPT
knowledge limit; the package was scoped to fit it.

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

## Scripts

| Script | Purpose |
|---|---|
| `fetch_transcripts.sh`, `add_videos.py`, `normalize.py` | Ingestion |
| `classify_channel.py`, `check_gaps.py` | Triage and caption-gap detection |
| `slice_sections.py`, `slice_matching.py` | Read one dimension across all notes (staging for the synthesis pass) |
| `build_catalog.py` | Generates `09_SOURCE_CATALOG.md` from note frontmatter |
| `build_app_data.py` | Generates the offline app |
| `make_xcodeproj.py` | Generates the Xcode project |

`build_catalog.py` and `build_app_data.py` both refuse to write if a note's id is missing from
the manifest, a universal section is missing, or a timestamp runs past the end of its video.
Both are deterministic: re-running without changing an input produces byte-identical output.

> `slice_sections.py` and `slice_matching.py` read `sys.argv` at module level and cannot be
> imported. `build_catalog.py` guards its entry point and is safely importable —
> `build_app_data.py` reuses its `parse_frontmatter()` and `as_list()`.

---

## Two things the app is deliberately honest about

**Citation density is uneven.** Files `01`–`08` carry **no** video-ID citations. The nine
`topic_reference` files carry 227 between them. The notes carry all 16,272 timestamps. So the
app renders live citations on notes and topic references, and never fabricates one on a
synthesis page. Related sources shown there are labelled *by tag*, not as claim-level citations.

**The practice filters are derived and partial.** Duration, position and equipment are
pattern-matched out of the source's own wording: of 703 practices, 144 state a readable
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

Every transcript, note and synthesised file in this repository derives from
**[The Feynman Way](https://www.youtube.com/@The_Feynman_Way)** — 224 videos fetched,
190 written up, ~89 hours of runtime. All rights in the underlying material remain with
that channel.

This is a personal, non-commercial study aid. It is not affiliated with or endorsed by the
channel, and nothing here is presented as original writing. The `[mm:ss]` anchors exist so
that any claim can be checked against the video that made it — the material is meant to be
watched, not replaced. If you find this useful, watch and subscribe to the source.
