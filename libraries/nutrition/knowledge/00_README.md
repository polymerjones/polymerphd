# 00 — README

**Polymer Ph.D. — Nutrition knowledge package**

This folder contains a synthesised knowledge base built from **68 YouTube transcripts** from the
channel **[@Paulsaladinomd](https://www.youtube.com/@Paulsaladinomd)**, covering food safety,
contamination, brand-level shopping decisions, and the reasoning behind an animal-based,
seed-oil-avoidant way of eating.

It is designed to be uploaded to a private Custom GPT, mirroring the working setup already built
for this project's Restorative Physiology library.

---

# What this is

**This package synthesises the teachings of one YouTube channel.** That is its scope and its whole
content. Every claim in it traces back to a specific video, at a specific timestamp, in that
collection.

It is not a survey of the nutrition literature, and it does not compare its source against other
nutrition authorities or schools of thought. The material cites outside research, brand-specific
lab tests, and named individuals, but those citations are reported as the videos give them, not
independently re-verified by this package.

**Nothing in this package originates outside the transcripts.**

---

# What was processed

| Measure | Figure |
|---|---|
| Videos written up as structured notes | **68** |
| Source channel | **Paul Saladino MD** (`@Paulsaladinomd`) |
| Knowledge files in this package | **17** (11 numbered + 6 topic references) |

---

# How it was built

The package was built as a two-stage process, and the structure is deliberate:

**Stage 1 — extraction.** Each transcript was read once and turned into a structured note
preserving central claims, foods and brands named, contamination mechanisms, glossary terms,
analogies, the source's own confidence statements, and `[mm:ss]` anchors back to the video.

**Stage 2 — synthesis.** The knowledge files were written **from the 68 notes, never from raw
transcripts.**

That separation is the anti-fabrication mechanism. **If a claim is not in a note, it does not
appear in this package.** The notes are traceable to timestamps; the timestamps are traceable to
videos; the videos are catalogued with full metadata in `09_SOURCE_CATALOG.md`.

The original transcripts were never modified, renamed, moved or deleted.

---

# The files

## Numbered files — the general answers

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`01_CORE_PRINCIPLES.md`** | The cross-cutting principles this collection returns to again and again |
| **`02_FOOD_PURPOSE_DIRECTORY.md`** | Foods and food categories, organized by what the source says each one is for or against |
| **`03_CONTAMINANTS_AND_MECHANISMS.md`** | The contaminants named across the corpus and how each is said to get into food or water |
| **`04_SHOPPING_AND_SOURCING_PRACTICES.md`** | Label-reading heuristics, store-by-store walkthroughs, and sourcing criteria |
| **`05_CONCERNS_MAP.md`** | Concern-by-concern index of which foods and products each health worry attaches to |
| **`06_MEAL_CONSTRUCTION_NOTES.md`** | What the corpus does and does not say about assembling meals |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | Every technical term the notes introduce, defined in plain language |
| **`08_QUESTIONS_AND_ANSWERS.md`** | Worked answers in the package's house style |
| **`09_SOURCE_CATALOG.md`** | All 68 videos — ID, title, URL, upload date, duration, subjects, foods, concerns, concepts. **Generated mechanically from the notes, so it is complete by construction** |
| **`10_CUSTOM_GPT_INSTRUCTIONS.md`** | The system instructions, boundaries and scope guidance |

## Topic references — the depth

| File | Covers |
|---|---|
| **`topic_reference_01_EGGS_AND_DAIRY.md`** | Eggs, milk, butter and cheese — labels, feed effects, A1/A2 casein, raw versus pasteurized |
| **`topic_reference_02_OILS_AND_FATS.md`** | Seed oils, olive and avocado oil, tallow, butter and other cooking fats |
| **`topic_reference_03_WATER_AND_HYDRATION.md`** | Bottled and tap water, filtration, fluoride, and hydration guidance |
| **`topic_reference_04_SUGAR_SWEETENERS_AND_ADDITIVES.md`** | Sugar sources, artificial sweeteners, food dyes and processed-food additives |
| **`topic_reference_05_MEAT_AND_REGENERATIVE_SOURCING.md`** | Grass-fed and grass-finished beef, pastured pork and chicken, regenerative grazing |
| **`topic_reference_06_PESTICIDES_AND_ENVIRONMENTAL_CONTAMINANTS.md`** | Glyphosate, PFAS, heavy metals, microplastics and other environmental exposures |

*(These carry the corpus's video-ID citations; the numbered files above do not.)*

---

# What the package covers well

**This is a shopping and product-safety library, not a general nutrition library.** Its genuine
strength, repeated across dozens of videos, is:

- **Which brand or product to avoid, and the specific reason** — named olive oils, bottled waters,
  salts, egg cartons, fast-food menu items, and packaged snacks, broken down ingredient by
  ingredient or contaminant by contaminant.
- **Contamination mechanisms** — how phthalates migrate from plastic into oil, how glyphosate
  carries from feed into meat and milk, how PFAS gets from packaging into food, how heavy metals
  move from soil into leafy greens and salt.
- **Label literacy** — what "grass-fed," "pasture-raised," "cage-free," "natural flavors," and
  similar terms actually certify (often much less than they imply), and what a careful shopper
  checks instead.
- **The case for an animal-based, seed-oil-avoidant way of eating**, and the mechanisms the source
  offers for it (linoleic acid accumulation, oxidized LDL, peroxidation index versus smoke point,
  and related arguments).

---

# What the package does not cover

Be clear-eyed about this collection's shape before relying on it for something it was never built
to answer:

- **Comprehensive meal planning.** The corpus is almost entirely about *what to avoid and what to
  buy instead* — it does not walk through building balanced meals or a weekly menu.
  `06_MEAL_CONSTRUCTION_NOTES.md` states this limitation directly rather than papering over it.
- **Calorie or macronutrient tracking.** No video in this collection is organized around counting
  calories, grams of protein/fat/carbohydrate, or portion sizing as its main subject.
- **Medical or diagnostic advice.** Several videos discuss conditions (alpha-gal syndrome,
  hypothyroidism, oxalate-related pain) but none of this package's material substitutes for
  clinical evaluation, testing, or treatment.
- **A survey of nutrition science generally.** This is one physician-influencer's channel, with a
  consistent point of view. Where the source disagrees with mainstream dietary guidance (seed
  oils, dietary cholesterol, fluoride), that disagreement is reported as the source's position, not
  validated against the wider literature.
- **Anything outside the channel.** No outside health theories were introduced, by design.

---

# How claims are graded

Many claims in this corpus — brand names, contamination figures, specific ppb/ppm numbers — are
stated in their source video **without an in-video citation** to a named study, lab, or agency.
Where a note's `## Source-stated confidence` section preserves that gap, this package preserves it
too, rather than upgrading an unsupported brand claim into a settled fact. `01_CORE_PRINCIPLES.md`
addresses this pattern directly.

Where two videos genuinely conflict — including two videos from the same channel reaching
different conclusions about the same brand — **both are preserved**, and the fact that a
disagreement exists is stated rather than resolved by picking a side.

---

# Upload guidance

**These files are made for pasting into a ChatGPT Custom GPT's knowledge base.** Upload the full
set of numbered files and topic references together — they cross-link to each other by filename,
and the topic references carry the depth and citations that the numbered files intentionally omit.

**Suggested setting:** turn web browsing **off**. The canonical-knowledge rule depends on the GPT
answering from this collection rather than from the open internet, and this collection represents
one channel's point of view, not a consensus.

**Recommend the GPT flag its scope up front** — this is a brand/product-safety and shopping
reference from one source, not a general dietitian, and it should say so rather than implying
broader coverage of meal planning or medical nutrition than it actually has.

---

*Built from 68 transcripts from one YouTube channel (@Paulsaladinomd).*
