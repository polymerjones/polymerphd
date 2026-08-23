# 00 — README

**Polymer Ph.D. — knowledge package**

This folder contains a synthesised knowledge base built from **190 YouTube transcripts** from the channel **[@The_Feynman_Way](https://www.youtube.com/@The_Feynman_Way)**, covering restorative physiology, the biology of ageing, and the mechanisms behind everyday health practices.

It is designed to be uploaded to a private Custom GPT. **All 20 files in this folder are the upload set** — that is exactly the Custom GPT knowledge file limit, and the package was scoped to fit it.

---

# What this is

**This package synthesises the teachings of one YouTube channel.** That is its scope and its whole content. Every claim in it traces back to a specific video, at a specific timestamp, in that collection.

It is not a survey of the medical literature, and it does not compare its source against other sources. The material *does* cite external research heavily — roughly 970 named attributions across 55+ journals — but those citations are reported as the videos give them, not independently verified.

**Nothing in this package originates outside the transcripts.**

---

# What was processed

| Measure | Figure |
|---|---|
| Videos identified on the channel | 280 |
| Health / human-body videos fetched | **224** |
| Videos written up as structured notes | **190** |
| Videos deferred | **34** |
| Total source runtime | **~89 hours** |
| Upload date range | **2026-02-10 → 2026-08-16** |
| Knowledge files produced | **20** (~102,000 words) |

## The 34 deferred videos

These were fetched and normalised but deliberately not written up. They are the channel's physics-framed material — thin on actionable physiology and outside the scope of a restorative-health guide.

**They remain on disk in the working folders and can be added later without re-downloading anything.** The full ID list is in `scripts/deferred_videos.txt`.

## Two caption dropouts

The auto-caption tracks for two videos have genuine gaps. These are recorded here because the material at those timestamps is not recoverable from the transcript, and **no claim anywhere in this package is drawn from the missing intervals.**

| Video | Gap | Missing |
|---|---|---|
| `5qdc4-rR9uQ` — *The Sleep Position That Protects the Most Organs After 50* | **15:24 → 18:06** | ~2.7 minutes |
| `co54vFnEHWU` — *The Molecule You Were Taught Is Waste* | **25:17 → 27:59** | ~2.5 minutes (part of the clinical / pulse-oximeter section) |

These are the only two gaps across all 190 transcripts.

---

# How it was built

The package was built as a two-stage process, and the structure is deliberate:

**Stage 1 — extraction.** Each transcript was read once and turned into a structured note (~1,200 words) preserving mechanisms, practices, doses, glossary terms, symptoms, analogies, the source's own confidence statements, and `[mm:ss]` anchors back to the video.

**Stage 2 — synthesis.** The 20 knowledge files were written **from the 190 notes, never from raw transcripts.**

That separation is the anti-fabrication mechanism. **If a claim is not in a note, it does not appear in the package.** The notes are traceable to timestamps; the timestamps are traceable to videos; the videos are catalogued with full metadata in `09_SOURCE_CATALOG.md`.

The original transcripts were never modified, renamed, moved or deleted.

---

# The files

## Numbered files — the general answers

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`01_CORE_PRINCIPLES.md`** | The 14 principles the whole collection rests on |
| **`02_BODY_SYSTEMS.md`** | System by system, across 10 systems |
| **`03_BIOLOGICAL_MECHANISMS.md`** | The consolidated mechanisms — nitric oxide, the vagus, the baroreflex, mitochondrial membrane potential, coupled oscillation, the olfactory-limbic bypass — and the worked resolutions of every apparent conflict |
| **`04_RESTORATIVE_PRACTICES.md`** | Every practice with its dose, timing, duration and mechanism |
| **`05_SYMPTOMS_AND_BODY_SIGNALS.md`** | Symptom → mechanism map, drawn from 1,152 catalogued entries across the notes |
| **`06_DAILY_VITALITY_FRAMEWORK.md`** | The day, the week and the year in sequence, plus the sequencing conflicts |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | 146 terms, curated from the 1,420 distinct terms the videos introduce |
| **`08_QUESTIONS_AND_ANSWERS.md`** | 18 worked answers in the package's house style |
| **`09_SOURCE_CATALOG.md`** | All 190 videos — ID, title, URL, upload date, duration, subjects, systems. **Generated mechanically from the notes, so it is complete by construction** |
| **`10_CUSTOM_GPT_INSTRUCTIONS.md`** | The system instructions, boundaries and emergency guidance |

## Topic references — the depth

| File | Videos behind it |
|---|---|
| **`topic_reference_01_EVIDENCE_AND_ATTRIBUTIONS.md`** | Corpus-wide — confidence levels, anchor studies, known conflicts |
| **`topic_reference_02_SLEEP_AND_CIRCADIAN.md`** | 64 |
| **`topic_reference_03_GLUCOSE_METABOLISM_AND_MEAL_TIMING.md`** | 64 |
| **`topic_reference_04_SPINE_POSTURE_AND_CONNECTIVE_TISSUE.md`** | 96 |
| **`topic_reference_05_LIGHT_AND_OUTDOOR_EXPOSURE.md`** | 19 |
| **`topic_reference_06_FALLS_BALANCE_AND_MOBILITY.md`** | 28 |
| **`topic_reference_07_VAGUS_AND_AUTONOMIC_REGULATION.md`** | 29 |
| **`topic_reference_08_GRIEF_LOSS_AND_CONNECTION.md`** | 20 |
| **`topic_reference_09_MEDICATION_INTERACTIONS.md`** | 26 |

*(Video counts overlap — a video about post-meal walking feeds both the glucose and the movement material.)*

---

# What the package covers

**Nervous system and autonomic regulation** — the vagus and every route into it, HRV, the dive reflex, the baroreflex, trauma, forgiveness, crying.

**Sleep and circadian rhythm** — architecture, the four systems behind the 3 a.m. waking, sleep position, snoring and the airway, napping, the full evening protocol, bedroom CO₂.

**Movement, balance and falls** — the directional argument, the four untrained planes, gait, foot clearance, terrain, and the protocols for each.

**Spine, posture and connective tissue** — disc pressures by posture, the sit-up, morning stiffness, the chair, decompression and loading.

**Metabolism and digestion** — glucose curves, insulin resistance as adaptation, meal timing and the circadian multiplier, chewing, the migrating motor complex, fasting and its honest trade-offs.

**Light and the outdoors** — the light dose, the sun argument, forest exposure and its decay curve, wind, soil, birdsong.

**Connection** — grief as whole-body physiology, touch thresholds, laughter, shared meals, singing together.

**Cardiovascular, respiratory, immune, lymphatic, endocrine, urinary and renal**, throughout.

**Medications** — a consolidated reference for how ~12 common drug classes interact with the practices in this package.

---

# What the package does not cover

- **The 34 deferred physics videos.** Available to add later.
- **Anything outside the channel.** No outside health theories were introduced, by design.
- **Diagnosis.** The symptom material maps signals to mechanisms as explanation, never as identification.
- **Medication decisions.** The source routes every one of these to the prescribing physician, and so does the package.
- **Content in the two caption gaps above.**

---

# How claims are graded

The source collection grades its own claims — **all 190 videos end with an explicit confidence statement** — and that grading is preserved rather than flattened.

Where this package states something plainly, the source stated it plainly. Where it says *"presented as,"* *"the video's inference,"* *"stated as a range,"* or *"flagged as the weakest evidence"* — **that language came from the source material.**

`topic_reference_01_EVIDENCE_AND_ATTRIBUTIONS.md` documents this in full, including the 64 passages the corpus explicitly hedges and the ten apparent conflicts with their resolutions.

Where two videos genuinely conflict, **both are preserved**, with the newer, more detailed or more context-specific source favoured — and the fact that a choice was made is stated rather than hidden.

---

# Emergency signals

`10_CUSTOM_GPT_INSTRUCTIONS.md` carries these in full. In brief, the source material identifies these as requiring emergency medical attention immediately:

- **Stroke** — face drooping, arm weakness, speech difficulty. Act immediately; a transient episode that resolves is a warning, not an all-clear.
- **Cauda equina syndrome** — loss of bladder or bowel control, saddle numbness, bilateral leg weakness. A surgical emergency requiring decompression within hours.
- **First episode of chest pain, breathlessness, racing heart or numbness** — regardless of confidence that the cause is anxiety.
- **Any sudden change** rather than a gradual one.

And two instructions that outrank everything else in the package:

- **Blood pressure medication must never be stopped without physician supervision.**
- **Anyone on insulin or a sulfonylurea must not undertake sudden strict carbohydrate reduction without medical supervision.**

---

# Recommended upload set

**All 20 files.** They are designed as a set — the numbered files carry the general answers, the topic references carry the depth, and they cross-link to each other by filename.

`09_SOURCE_CATALOG.md` is the largest file at ~37,000 words. It is a lookup table rather than prose, and it is what makes every citation in the package resolvable to a real video with a real URL.

**Suggested setting:** turn web browsing **off**. The canonical-knowledge rule depends on the GPT answering from this collection rather than from the open internet.

---

# Branding

| Item | Value |
|---|---|
| **GPT name** | Polymer Ph.D. |
| **Icon** | `images/app_icon.png` — 1254×1254 PNG |
| **Web browsing** | Off |

The icon lives outside this folder deliberately — it is set in the Custom GPT builder as the profile picture, not uploaded as a knowledge file. **Uploading it as a knowledge file would waste one of the 20 slots**, and all 20 are in use.

---

*Built from 190 transcripts, ~89 hours of source material, published 2026-02-10 to 2026-08-16.*
