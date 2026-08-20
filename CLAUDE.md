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

```
bash scripts/add.sh https://youtu.be/XXXXXXXXXXX     # fetch, normalize, list what needs a note
                                                      # write notes/<id>.md          <- judgement
python3 scripts/check_notes.py <id>                   # validate
bash scripts/publish.sh --push                        # rebuild all outputs and ship
```

Stage 1 and stage 4 are plumbing and safe to re-run. Stage 2 is the whole job.

### Writing the note

Read `source_transcripts/clean/<id>.txt` once. Match the schema every existing note follows —
read two or three neighbours in `notes/` first, and match their density, not just their headings.

**Four frontmatter facets:** `subjects`, `systems`, `practices`, `concepts`. `systems` must come
from the ten-item controlled vocabulary (see any existing note, or `data.json`'s `vocab.systems`).

**Six universal sections, in this order at the edges:**

- `## Central claim` — first
- `## Symptoms and body signals addressed`
- `## Glossary terms introduced`
- `## Analogies worth reusing`
- `## Source-stated confidence`
- `## Conflicts with other sources` — last

Between "Central claim" and "Symptoms", write whatever sections the video's own argument calls
for. No two notes match there, and they should not.

**Conventions that make the notes what they are:** heavy direct quotation, an `[mm:ss]` anchor on
every substantive claim, tables where the source is comparing things, bold for the load-bearing
sentence rather than scattered emphasis. `## Conflicts with other sources` does real work — find
the notes that overlap, name them by video id in backticks, and say whether this one converges,
extends, or genuinely disagrees. Deferred videos are legitimate cross-references.

If the video is physics-framed rather than body-focused, add the id to
`scripts/deferred_videos.txt` instead of writing a note. Thirty-four have gone that way.

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
- **`source_transcripts/raw/` is gitignored** (~300 MB of yt-dlp dumps, regenerable). `clean/` is
  the provenance record.
- **The iOS build expires after 7 days** on a free Apple ID. Rebuild to renew.

---

## Delivery paths, and what goes stale

| Path | Updates when |
|---|---|
| <https://polymerjones.github.io/polymerphd/> | ~1 min after any push. This is the link Paul sends his father |
| `app/index.html` | `build_app_data.py` |
| `ios/` | `make_xcodeproj.py`, then build to device |
| **Custom GPT** | **Never automatically.** Re-upload the 20 files in `restorative_vitality_knowledge/` by hand after any synthesis change |
