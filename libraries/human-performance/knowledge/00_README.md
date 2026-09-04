# 00 — README

**Polymer Ph.D. — Human Performance and Health Optimization knowledge package**

This folder contains a synthesised knowledge base built from YouTube transcripts on human
performance, stress physiology, energy, recovery, and health optimization — drawn from **multiple
different creators' channels**, unlike this project's other libraries, which each cover one
channel.

---

# What this is

**This package synthesises the teachings of several YouTube channels on a shared subject:** human
performance and health optimization. Every claim in it traces back to a specific video, from a
specific creator, at a specific timestamp.

Because sources come from more than one creator, this package does not treat them as one unified
voice. Where two sources agree or disagree, that is noted explicitly rather than blended into a
single house position. Each note names its own source creator directly in its prose and citations.

**Nothing in this package originates outside the source transcripts.**

---

# What was processed

| Measure | Figure |
|---|---|
| Videos written up as structured notes | **42** |
| Source channels | **Seth Capehart MD** (`@SethCapehartMD`) and **Dr. Mike/Matt Jones** (`@Dr.MattJones`) |
| Knowledge files in this package | **11** (numbered files 00–08 and 10; `09_SOURCE_CATALOG.md` self-regenerates) |

This library is still growing — new creators and videos are added over time. See
`09_SOURCE_CATALOG.md` (generated mechanically from the notes, so it is always complete and
current) for the exact, up-to-the-minute video count, creators, and topics covered.

---

# How it was built

The package follows the same two-stage process as this project's other libraries:

**Stage 1 — extraction.** Each transcript is read once and turned into a structured note
preserving central claims, glossary terms, analogies, the source's own confidence statements, and
`[mm:ss]` anchors back to the video.

**Stage 2 — synthesis.** The knowledge files are written **from the notes, never from raw
transcripts.**

That separation is the anti-fabrication mechanism. **If a claim is not in a note, it does not
appear in this package.**

---

# The files

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`01_CORE_PRINCIPLES.md`** | Cross-cutting principles this collection returns to, as they emerge |
| **`02_MECHANISMS_AND_SYSTEMS.md`** | Physiological mechanisms and body systems discussed across sources |
| **`03_PRACTICES_AND_PROTOCOLS.md`** | Practices, protocols, and interventions the sources describe |
| **`04_SIGNALS_AND_SELF_ASSESSMENT.md`** | Symptoms, body signals, and self-assessment cues the sources describe |
| **`05_CROSS_SOURCE_COMPARISON.md`** | Where sources from different creators converge, extend, or conflict |
| **`06_OPEN_QUESTIONS.md`** | What this corpus does not yet cover or leaves unresolved |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | Every technical term the notes introduce, defined in plain language |
| **`08_QUESTIONS_AND_ANSWERS.md`** | Worked answers in the package's house style |
| **`09_SOURCE_CATALOG.md`** | All videos — ID, title, URL, creator, upload date, duration, subjects, practices, concepts. **Generated mechanically from the notes, so it is complete by construction** |
| **`10_CUSTOM_GPT_INSTRUCTIONS.md`** | The system instructions, boundaries and scope guidance |

*(Only files carrying video-ID citations by design are `topic_reference_*.md` files, added once
there is enough depth on a given topic to warrant one — none exist yet.)*

---

# What the package does not cover

- **A single, unified point of view.** This library intentionally spans multiple creators. It does
  not resolve disagreements between them into one answer — it reports each source's position and
  names genuine conflicts.
- **Medical or diagnostic advice.** Nothing here substitutes for clinical evaluation, testing, or
  treatment.
- **Anything outside the source transcripts.** No outside health theories are introduced.

---

# Upload guidance

**These files are made for pasting into a ChatGPT Custom GPT's knowledge base.** Upload the
numbered files together; add topic references once they exist.

**Suggested setting:** turn web browsing **off** — the value of this collection depends on the GPT
answering from these specific sources rather than blending in outside claims it can't attribute.
