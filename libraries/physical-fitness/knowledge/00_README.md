# 00 — README

**Polymer Ph.D. — Physical Fitness knowledge package**

This folder contains a synthesised knowledge base built from the Georges St-Pierre RUSHFIT home
training program — nine DVD workout sessions (transcribed locally with Whisper; none were ever
captioned or posted to YouTube) and five program guides (a Workout Guide, a Nutrition Guide, and
three 8-week training calendars).

---

# What this is

**This package synthesises one complete home-fitness program**, designed by mixed martial artist
Georges St-Pierre and his trainer Erik Owings. Every claim in it traces back to a specific
source — a timestamp in a workout video, or a page in a guide.

This is the first Polymer Ph.D. library built from local media rather than YouTube: the DVDs have
no public URL, and their transcripts came from local Whisper speech recognition rather than
platform-supplied captions. The `program` facet exists specifically so this library can later
hold other home-fitness programs alongside RUSHFIT, the way `human-performance` holds multiple
YouTube creators under one roof — see each note's frontmatter.

**Nothing in this package originates outside the source transcripts and guides.**

---

# What was processed

| Measure | Figure |
|---|---|
| Sources written up as structured notes | **14** (9 videos, 5 PDF guides) |
| Program | **RUSHFIT** (Georges St-Pierre / Erik Owings) |
| Total video runtime | **~11.7 hours**, transcribed locally (Whisper, `small` model) |
| Knowledge files in this package | **11** (numbered files 00–08 and 10; `09_SOURCE_CATALOG.md` self-regenerates) |

See `09_SOURCE_CATALOG.md` (generated mechanically from the notes, so it is always complete and
current) for the exact source list.

---

# How it was built

The package follows the same two-stage process as this project's other libraries:

**Stage 1 — extraction.** Each video was transcribed locally with Whisper (`scripts/add_local_video.py`,
written for this library since no existing script handled a local, non-YouTube video file) and
each PDF guide extracted page-by-page with `scripts/add_pdf.py`. Every transcript and extraction
was then read once and turned into a structured note preserving central claims, glossary terms,
analogies, the source's own confidence statements, and `[mm:ss]`/`[p.N]` anchors back to the
source.

**Stage 2 — synthesis.** The knowledge files are written **from the notes, never from raw
transcripts.**

That separation is the anti-fabrication mechanism. **If a claim is not in a note, it does not
appear in this package.**

A structural note on this corpus specifically: several DVDs share an identical warm-up and
cool-down sequence verbatim, and three of the nine DVDs close by re-running the entire Foundation
Moves DVD in full. Rather than re-deriving that shared content in every note, later notes describe
it briefly and cross-reference the note that covers it in full — a deliberate choice to avoid
diluting the corpus with duplicate text, not a gap in coverage.

---

# The files

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`01_CORE_PRINCIPLES.md`** | Cross-cutting principles this program returns to, across DVDs and guides |
| **`02_MOVEMENTS_AND_TECHNIQUE.md`** | The foundation movements and their technique cues, as taught across the corpus |
| **`03_PRACTICES_AND_PROTOCOLS.md`** | Workout formats, the RUSHFIT Assessment, nutrition timing, and the training calendars |
| **`04_SIGNALS_AND_SELF_ASSESSMENT.md`** | Form cues, fatigue signals, and modification triggers the sources describe |
| **`05_CROSS_SOURCE_COMPARISON.md`** | Where sources converge, repeat verbatim, or extend each other |
| **`06_OPEN_QUESTIONS.md`** | What this corpus does not cover or leaves unresolved |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | Every technical/program-specific term the notes introduce, defined in plain language |
| **`08_QUESTIONS_AND_ANSWERS.md`** | Worked answers in the package's house style |
| **`09_SOURCE_CATALOG.md`** | All sources — ID, title, kind, duration/page count, workouts, exercises. **Generated mechanically from the notes, so it is complete by construction** |
| **`10_CUSTOM_GPT_INSTRUCTIONS.md`** | The system instructions, boundaries, and scope guidance |

*(Only files carrying source-ID citations by design would be `topic_reference_*.md` files —
none exist yet; this is a single-program corpus without the cross-creator depth that motivates
them in libraries like `nutrition` or `human-performance`.)*

---

# What the package does not cover

- **Exercise science evidence.** This corpus is entirely instructional/programmatic — the
  program's own coaching rationale and demonstrations, not cited studies. Nothing here should be
  read as a research citation.
- **Medical or diagnostic advice.** Nothing here substitutes for a physician's evaluation; the
  program's own guides repeatedly say the same.
- **Other home-fitness programs.** This library is architecturally ready to hold them (see the
  `program` facet), but none are ingested yet.
- **Anything outside the source transcripts and guides.** No outside fitness or nutrition theories
  are introduced.

---

# Upload guidance

**These files are made for pasting into a ChatGPT Custom GPT's knowledge base.** Upload the
numbered files together.

**Suggested setting:** turn web browsing **off** — the value of this collection depends on the GPT
answering from this specific program rather than blending in outside fitness advice it can't
attribute.
