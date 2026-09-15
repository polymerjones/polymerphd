# 00 — README

**Polymer Ph.D. — Ayurveda knowledge package**

This folder contains a synthesised knowledge base built from five sources on Ayurveda — doshas,
digestion, daily and seasonal routine, remedies, and clinical guidance — spanning very different
registers, from a YouTube psychiatrist to two Indian government clinical guidelines. It is the
youngest and smallest library in this project so far.

---

# What this is

**This package synthesises five sources on Ayurveda and one deliberate outlier.** Every claim in it
traces back to a specific point in a specific source — a video timestamp, or a page number.

- **`-BEdhS9-cno`** — a YouTube video by a psychiatrist (HealthyGamerGG), framing doshas as
  personality/constitution typing with a clinical-practice angle.
- **`ayurveda-idiots-guides-sahara-rose-ketabi`** — a 332-page general-audience introductory
  textbook (DK/Penguin Random House, 2017), by far the most comprehensive single source here. Most
  of the Sanskrit vocabulary and framework used elsewhere in this library either originates from or
  overlaps with this book.
- **`ccras-diet-lifestyle-guidelines-skin-diseases`** and
  **`ccras-diet-lifestyle-guidelines-cardiac-disorders`** — two government clinical guidelines
  (Central Council for Research in Ayurvedic Sciences, Ministry of AYUSH, Government of India),
  citation-backed and written in a clinical-protocol register, not a consumer one.
- **`flow-the-psychology-of-optimal-experience`** — Csikszentmihalyi's *Flow* (1990), a Western
  academic-psychology book with **no Ayurvedic content at all**, included at the user's explicit
  direction as a deliberate outlier. Its only genuine point of contact with the rest of this
  library is Patanjali's eight-limbed Yoga, which the Ketabi book also describes — with an opposite
  stated goal. See `05_CROSS_SOURCE_COMPARISON.md`.

**Nothing in this package originates outside these five sources.** In particular, this package does
not add outside Ayurvedic knowledge the author may know — if a claim, term, or remedy isn't in one
of the five notes, it isn't in this package.

---

# What was processed

| Measure | Figure |
|---|---|
| Sources written up as structured notes | **5** |
| Registers spanned | One YouTube video, one general-audience textbook, two government clinical guidelines, one unrelated Western psychology book |
| Knowledge files in this package | **9** (numbered files 00–08; `09_SOURCE_CATALOG.md` self-regenerates) |

This library is still very young — see `09_SOURCE_CATALOG.md` (generated mechanically from the
notes, so it is always complete and current) for the exact, up-to-the-minute source count.

# A note on evidentiary weight

These five sources do not carry equal authority, and this package does not flatten that difference:

- The two **CCRAS government guidelines** are citation-backed (35–42 numbered references each,
  mixing classical Ayurvedic texts with some modern peer-reviewed citations) and explicitly labeled
  clinical guidance — but each also carries its own printed caveat that it should only be followed
  "under supervision of qualified registered Ayurveda practitioner."
- The **Ketabi book** is a popular introductory textbook; it states most of its material as settled
  doctrine but explicitly flags its self-assessment quiz, some food lists, and its modern-sweetener
  additions as approximate or personal synthesis rather than fixed tradition.
- The **HealthyGamerGG video** is one psychiatrist's own clinical framework and synthesis, stated
  with high confidence throughout, citing named research only for a handful of specific claims
  (ayurgenomics, a gut-brain stool-transplant study).
- ***Flow*** carries the evidentiary standards of an academic psychology text (decades of interviews
  plus a purpose-built Experience Sampling Method) but contributes nothing to this library's
  Ayurvedic content specifically.

---

# How it was built

The package follows the same two-stage process as this project's other libraries:

**Stage 1 — extraction.** Each source is read once and turned into a structured note preserving
central claims, glossary terms, analogies, the source's own confidence statements, and `[mm:ss]` or
`[p.N]` anchors back to the source.

**Stage 2 — synthesis.** The knowledge files are written **from the notes, never from raw
transcripts or the original books/PDFs.**

That separation is the anti-fabrication mechanism. **If a claim is not in a note, it does not
appear in this package.**

---

# The files

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`01_CORE_PRINCIPLES.md`** | The fundamentals that recur or are extended across multiple sources |
| **`02_DIET_AND_DAILY_ROUTINE.md`** | Dosha-specific diet, the six tastes, dinacharya/ritucharya, and disease-specific diet charts |
| **`03_REMEDIES_AND_PRACTICES.md`** | Panchakarma, home remedies, self-care rituals, and the ethical/urge-suppression regimen |
| **`05_CROSS_SOURCE_COMPARISON.md`** | Where these five sources converge, extend, or genuinely conflict |
| **`06_OPEN_QUESTIONS.md`** | What this small corpus does not yet resolve |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | Every technical term the notes introduce, defined in plain language |
| **`08_QUESTIONS_AND_ANSWERS.md`** | Worked answers in the package's house style |
| **`09_SOURCE_CATALOG.md`** | All five sources — ID, title, author/creator, and details. **Generated mechanically from the notes, so it is complete by construction** |

*(Only files carrying page/timestamp citations by design are `topic_reference_*.md` files, added
once there is enough depth on a given topic to warrant one — none exist yet for this library.)*

---

# What the package does not cover

- **A substitute for a qualified Ayurvedic practitioner (Vaidya).** Both CCRAS guidelines state this
  explicitly, and this package repeats rather than overrides that caveat.
- **Clinical treatment of disease beyond what the two CCRAS documents state.** This is not a general
  Ayurvedic-medicine reference; disease-specific guidance here is limited to what `Kushta` (skin
  disease) and cardiac-risk-related conditions (`Madhumeha`/diabetes, `Uchcharaktachapa`/
  hypertension, `Sthaulya`/obesity) the two guidelines actually cover.
- **Peer-reviewed efficacy data for any specific remedy.** Home remedies, panchakarma, and dosha-
  based diet recommendations are reported as each source states them — traditional or clinical-
  experience claims — not as trial-tested interventions.
- **A resolved answer to how literally "dosha" should be taken.** The four Ayurveda-focused sources
  range from personality typing to strict clinical classification; this package reports that range
  rather than picking one reading. See `06_OPEN_QUESTIONS.md`.
- **Anything outside these five source transcripts/texts**, including general Ayurvedic knowledge
  the author may know that isn't stated in one of them.

---

# Upload guidance

**These files are made for pasting into a ChatGPT Custom GPT's knowledge base.** Upload the
numbered files together; add a topic reference once one exists.

**Suggested setting:** turn web browsing **off** — the value of this collection depends on the GPT
answering from these five specific sources rather than blending in outside Ayurvedic claims it
can't attribute.
