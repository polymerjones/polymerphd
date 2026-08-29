# Working on Polymer Ph.D.

`README.md` describes what this project *is*. This file describes how to work on it without
breaking the one thing that gives it value.

Paul is the domain author, not a developer. Lead with the shape of the deliverable, not the
parsing internals.

---

## The rule everything else serves

**Nothing in this repository originates outside the source transcripts.** Every claim traces to a
specific video at a specific second. A plausible-looking invention destroys the package more
cheaply than any missing feature ever could.

Three ways that rule gets broken, in order of how easy they are to break by accident:

1. **A fabricated timestamp.** An anchor that is well-formed and inside the video's runtime but
   absent from the transcript. Writing a closing quote against the video's *duration* rather than
   its last real anchor is the classic slip. `check_notes.py` catches this — run it.
2. **Imported terminology.** Supplying the correct technical name for something a video described
   without naming. "Zinc finger", "capillary rarefaction" and "ribonucleotide reduction" all got
   in this way and had to be removed. If the source described a mechanism in its own words, use
   its words. `check_notes.py --terms` is an advisory pass for this.
3. **A citation on a synthesis page.** Files `01`–`08` carry **no** video-ID citations. Only the
   nine `topic_reference` files do. Keep it that way.

Alongside those: **preserve each source's own hedges verbatim.** Several videos grade their own
evidence explicitly — the closed stress–gut loop and the ridge-to-capillary pairing are both
stated by their sources as inference rather than fact. That grading travels with the claim
wherever it is used. Keep the derived-versus-stated distinction visible rather than smoothing it
away.

---

## Adding a video

This repo is multi-library: every script below takes a `<slug>` as its first argument (one of the
directory names under `libraries/`, e.g. `restorative-physiology`, `nutrition`, `dupuytren`, or a
new one — see "Adding a library" below). `publish.sh` is the one exception; it rebuilds every
library in one pass, no slug needed.

```
bash scripts/add.sh <slug> https://youtu.be/XXXXXXXXXXX   # fetch, normalize, list what needs a note
                                                            # write libraries/<slug>/notes/<id>.md   <- judgement
python3 scripts/check_notes.py <slug> <id>                 # validate
bash scripts/publish.sh --push                              # rebuild ALL libraries' outputs and ship
```

Stage 1 and stage 4 are plumbing and safe to re-run. Stage 2 is the whole job.

### Writing the note

Read `libraries/<slug>/sources/clean/<id>.txt` once. Match the schema every existing note in that
library follows — read two or three neighbours in `libraries/<slug>/notes/` first, and match
their density, not just their headings. Different libraries have different densities (dense and
clinical for `dupuytren`, conversational for `restorative-physiology`) — match the library you're
writing into, not another one.

**Frontmatter facets** are declared per library in `libraries/<slug>/library.json`'s `facets`
list (e.g. `restorative-physiology` uses `subjects`, `systems`, `practices`, `concepts`). A facet
listed under that file's `controlled_facets` must come from its fixed vocabulary — only
`restorative-physiology`'s `systems` facet is controlled today (the ten-item body-system list; see
any existing note there, or `library.json`'s `controlled_facets.systems`). Other libraries'
facets are free-form.

**Six universal sections, in this order at the edges** (the exact headings are declared per
library in `library.json`'s `universal_sections` — physiology/body libraries use "Symptoms and
body signals addressed"; a library with a different subject can adapt that one heading's wording,
e.g. a mindset/self-help library might use "Signals and internal states addressed" instead):

- `## Central claim` — first
- `## <the library's symptoms/signals heading>`
- `## Glossary terms introduced`
- `## Analogies worth reusing`
- `## Source-stated confidence`
- `## Conflicts with other sources` — last

Between "Central claim" and the symptoms/signals section, write whatever sections the video's own
argument calls for. No two notes match there, and they should not.

**Conventions that make the notes what they are:** heavy direct quotation, an `[mm:ss]` anchor on
every substantive claim, tables where the source is comparing things, bold for the load-bearing
sentence rather than scattered emphasis. `## Conflicts with other sources` does real work — find
the notes that overlap, name them by video id in backticks, and say whether this one converges,
extends, or genuinely disagrees. Deferred videos are legitimate cross-references.

If a video is out of scope for the library (e.g. physics-framed rather than body-focused, in
`restorative-physiology`), add its id to `libraries/<slug>/deferred_sources.txt` instead of
writing a note — one id per line. `add.sh` and `check_notes.py` both treat ids there as
legitimately excluded, not missing.

---

## Adding a library

There's no scaffold script for this — it's a manual, one-time setup per library, after which the
normal "Adding a video" workflow above takes over:

1. `mkdir -p libraries/<slug>/{notes,knowledge,sources/{clean,raw},ingest_state}` and
   `touch libraries/<slug>/deferred_sources.txt`.
2. Write `libraries/<slug>/library.json` — copy an existing one as a template.
   `libraries/nutrition/library.json` is the better starting point for a non-physiology library
   (free-form `facets`, empty `controlled_facets`); `libraries/restorative-physiology/library.json`
   is the one with a controlled vocabulary if the new library needs one. Set `slug`, `title`,
   `subtitle`, `facets`, `primary_facet`, `controlled_facets`, `universal_sections`, `attribution`
   (channel name/url), and `custom_gpt` (20-file upload cap).
3. Add `libraries/<slug>/icon.b64` and `splash.b64` — base64-encoded image data, referenced by
   `library.json`'s `icon_file`/`splash_file`.
4. `bash scripts/add.sh <slug> <urls...>` to start ingesting, same as any other library.
5. `bash scripts/publish.sh --push` is what actually makes the new library appear in the app's
   picker — `build_app_data.py` discovers libraries purely by scanning `libraries/*/library.json`,
   so nothing needs registering by hand beyond that file existing with at least one note.

---

## After a note changes

`09_SOURCE_CATALOG.md` regenerates itself. **The other 19 knowledge files do not.** They were
synthesised by hand, and whether a new video changes them is a judgement call every time —
skipping it is not wrong, it means the synthesis lags the notes by one video.

When it does warrant an edit, the usual homes are:

| File | Update when |
|---|---|
| `01_CORE_PRINCIPLES.md` | The video sharpens or contradicts a stated principle |
| `04_RESTORATIVE_PRACTICES.md` | It changes a dose, a technique, or a contraindication |
| `07_PLAIN_ENGLISH_GLOSSARY.md` | New terms — alphabetical, `**Term** — definition`, no citations |
| `topic_reference_*.md` | Deeper treatment of that topic; these *do* carry citations |

Prefer extending an existing entry over adding a near-duplicate.

**Contraindications go *with* the practice, not after it.** That is a standing rule from the
source material, restated in the README's Boundaries section.

---

## Gotchas

- **`project.pbxproj` is generated.** Edit `scripts/make_xcodeproj.py`, never Xcode — Xcode-side
  changes are overwritten on the next build. The development team is set in the generator for
  this reason.
- **Both build scripts must run after any web-app change**, because the second syncs
  `index.html` into the iOS bundle. `publish.sh` does both in order.
- **`slice_sections.py` and `slice_matching.py` read `sys.argv` at module level** and cannot be
  imported. `build_catalog.py` is safely importable.
- **GitHub Pages caches for about ten minutes.** After a push, verify with a cache-busting query
  string or you will see the previous build and think the deploy failed.
- **`libraries/<slug>/sources/raw/` is gitignored** (yt-dlp dumps, regenerable, ~300 MB across all
  libraries). `sources/clean/` is the provenance record and is committed.
- **The iOS build expires after 7 days** on a free Apple ID. Rebuild to renew.
- **`app/index.html` bundles every library, not just one you're working on.** `build_app_data.py`
  and `publish.sh` always process all of `libraries/*/library.json` — there's no way to rebuild
  just one library's slice of the app.

---

## Delivery paths, and what goes stale

| Path | Updates when |
|---|---|
| <https://polymerjones.github.io/polymerphd/> | ~1 min after any push. This is the link Paul sends his father |
| `app/index.html` | `build_app_data.py` (all libraries at once) |
| `ios/` | `make_xcodeproj.py`, then build to device |
| **Custom GPT** (one per library) | **Never automatically.** Re-upload the files in `libraries/<slug>/knowledge/` (per that library's `custom_gpt.file_limit`, 20 today) by hand after any synthesis change, with `libraries/<slug>/PASTE_INTO_GPT_INSTRUCTIONS.txt` as the system prompt |
