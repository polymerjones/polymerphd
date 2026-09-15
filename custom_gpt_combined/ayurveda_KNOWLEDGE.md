# Ayurveda

## From 00_README.md

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

---

## From 01_CORE_PRINCIPLES.md

# 01 — Core Principles

This library holds five sources spanning very different registers — a psychiatrist's YouTube video,
a general-audience textbook, two government clinical guidelines, and one unrelated psychology book.
The seven patterns below are the ones that recur or are independently extended across the four
Ayurveda-focused sources, despite their very different authority levels and intended audiences.

---

## 1. The tridosha framework (Vata, Pitta, Kapha) is the organizing lens for everything else

All four Ayurveda-focused sources treat the three-dosha system as the starting classification for
mind, body, disease, and treatment — but apply it to different domains. The video applies it to
personality and psychiatric presentation; the Ketabi book applies it to personality, body type,
digestion, and daily practice; both CCRAS guidelines apply it strictly clinically, as the causative
framework behind specific named diseases (skin disease, hypertension, diabetes, obesity). The
underlying trait descriptions are consistent across all four — Vata as changeable/quick/thin/prone
to anxiety, Pitta as driven/sharp/prone to anger and inflammation, Kapha as slow/steady/heavyset/
prone to depression and weight gain — even though no two sources cite each other.

## 2. The doshas' elemental composition is stated identically by a pop-audience book and a government guideline

The Ketabi book states **Vata = air + ether, Pitta = fire + water, Kapha = earth + water**. The
CCRAS cardiac guideline, independently and in an entirely different register (Panchamahabhoota
composition), states the same pairing: **Vata = Vayu + Akasha, Pitta = Agni + Jala, Kapha = Jala +
Prithvi** — the same two elements per dosha, just named in Sanskrit rather than English. This is the
closest thing in this small library to a fully corroborated, source-independent fact.

## 3. Digestive fire (agni) is treated as the root mechanism behind most disease, not just digestion

The Ketabi book frames agni as governing physical digestion *and* emotional processing (confidence,
patience, and logic on one side; fear, impatience, and confusion on the other, depending on which of
the four agni types is out of balance). The CCRAS cardiac guideline proposes an explicit causal
chain — impaired **Koshtagni** → poor-quality **Ahararasa** → vitiated **Rasa Dhatu** → metabolic
disorders → heart disease — extending the same "digestion as root cause" logic from a textbook claim
into a specific, named clinical pathway for cardiovascular disease.

## 4. Diet is the primary lever, applied through one consistent rule: eat the opposite of your dosha's qualities

The video states this directly (Vata eats warm/moist, Pitta eats cold/dry, Kapha eats warm/dry) as a
simple rule of thumb. The Ketabi book states the identical counterbalancing rule with far more detail
(full food-category lists per dosha, the six-taste system layered on top). Both CCRAS guidelines
operationalize the same underlying logic into disease-specific pathya/apathya (do/don't) lists and,
in the cardiac guideline, three full dosha-specific full-day diet charts.

## 5. Daily and seasonal routine (dinacharya and ritucharya) is treated as preventive medicine, not lifestyle advice

The Ketabi book's dinacharya (wake near sunrise, tongue scrape, oil pull, dry brush, self-massage,
light breakfast, biggest meal at midday, light dinner, asleep by 10pm) and both CCRAS guidelines'
dinacharya (waking during Brahma Muhurta 4:00–5:30am, oil massage, daily exercise, bathing,
grooming) describe the same practice, differing mainly in specificity and register. The two CCRAS
documents in particular share dinacharya, ritucharya, and sadvritta sections that are worded
near-identically to each other, down to matching phrasing — evidence these sections come from a
shared classical source rather than being independently derived by each guideline's authors.

## 6. Individualization, not a universal rule, is the stated point of the whole system

The Ketabi book states this as a first principle: "no single guideline can work for all people
because we are all different beings with unique needs." The video's psychiatrist frames the same
idea as Ayurveda's advantage over Western medicine specifically: Western medicine "sub-specializes"
and "treats diseases," while Ayurveda "presumes that all human beings are different." Both sources
independently arrive at the same contrast between a universal-protocol model and an individualized
one, applied to different fields (nutrition versus psychiatry).

## 7. A person's baseline constitution and their current, deviated state are treated as two different things — and treatment targets the gap between them

The Ketabi book names this distinction explicitly and centrally: **Prakriti** (birth-fixed dosha
mix, unchangeable) versus **Vikruti** (today's dosha state, shaped by diet/environment/stress/age),
illustrated with three worked case studies of people whose current state has drifted from their
baseline. The video's psychiatrist describes the identical two-part structure — a genetic baseline
("prakruti... the stats you are created with") and a second, correctable state that diet and
lifestyle changes are meant to shift back toward baseline — but the video's own auto-generated
captions never correctly spell the second term, so this library's note on that video does not assert
it said "vikriti," even though the concept matches. See `06_OPEN_QUESTIONS.md`.

---

Every other file in this package applies one or more of these seven patterns to a specific topic —
diet and routine, or remedies and practices.

---

## From 02_DIET_AND_DAILY_ROUTINE.md

# 02 — Diet and Daily Routine

Diet and daily/seasonal routine are the most heavily corroborated topic in this library — all four
Ayurveda-focused sources address them, from an informal rule of thumb (the video) to full clinical
diet charts (the CCRAS guidelines).

## Dosha-specific diet: the counterbalancing rule

The consistent rule across sources: **eat foods with qualities opposite to your dosha's own.**

| Dosha | Qualities | Eat foods that are |
|---|---|---|
| Vata | Cold, dry, light | Warm and moist (soup over salad; cooked over raw) |
| Pitta | Hot, oily, sharp | Cold and dry (salads, sandwiches); avoid excess garlic/onion/spice |
| Kapha | Cold, oily, heavy | Warm and dry (toast); light, bitter/pungent/astringent, minimal dairy |

The Ketabi book gives full food-category lists (fruit, vegetable, grain, legume, dairy, nut, animal
product, oil, sweetener, spice) per dosha. Both CCRAS guidelines translate the same logic into
disease-specific pathya (wholesome/do) and apathya (unwholesome/don't) lists rather than general
dosha lists — e.g., for Uchcharaktachapa (hypertension): pathya includes barley, moringa, bitter
gourd, carrot, radish, amla, pomegranate, cold milk; apathya includes excess salt, butter, ghee,
chilies, pickles, curd, tea/coffee, alcohol, and day-sleeping.

## The six tastes (rasa)

Six tastes should all appear daily, in proportions matched to dosha imbalance: **madhura** (sweet),
**amla** (sour), **lavana** (salty), **katu** (pungent), **tikta** (bitter), **kashaya** (astringent).
The Ketabi book gives the per-dosha balance: Vatas favor sweet/sour/salty and reduce the other
three; Pittas favor sweet/bitter/astringent and reduce sour/salty/pungent; Kaphas favor bitter/
pungent/astringent and reduce sweet/sour/salty. The CCRAS cardiac guideline states a parallel
taste-to-dosha alleviation mapping: sweet/sour/salty tastes alleviate Vata; astringent/sweet/bitter
alleviate Pitta; astringent/pungent/bitter alleviate Kapha.

The Ketabi book additionally maps digestion itself to a six-stage, roughly six-hour sequence, one
stage per taste, each tied to an element pair and a dosha (sweet → sour → salty → pungent → bitter →
astringent, moving from stomach to colon). Its strongest procedural claim: do not eat again until the
prior meal has fully passed through all six stages, since snacking is said to trap the body in the
early, "heavy" stages and block the later detoxifying ones.

## The eight-factor framework for evaluating any food

Both CCRAS guidelines state the same eight-factor framework (**Ashta ahara vidhi visesha ayatana**)
for judging whether a food is beneficial:

| Factor | Meaning |
|---|---|
| Prakriti | Nature of the food itself (heavy/light, hot/cold potency) |
| Karana | How processing changes the food's properties |
| Samyoga | Combinations that augment or nullify each other |
| Raashi | Quantity required per person |
| Desha | Habitat/origin of the food relative to the person |
| Kaala | Time — climate, digestive phase, time of day, disease stage |
| Upayoga Samstha | Following proper rules of how food is taken |
| Upayokta | The consumer's own preference and habituation |

A separate quantity rule, attributed to Susruta and Vagbhata in the CCRAS skin-disease guideline:
divide stomach capacity into four parts — two solid food, one liquid, one left empty "for easy
movement of Vata."

## Virudha ahara (dietetic incompatibility)

A recurring concept across three sources, though applied slightly differently. Both CCRAS guidelines
define it via Acharya Charaka as diet combinations that "interrupt the metabolism" or have properties
opposite to the tissue being nourished, citing roughly 18 named types with complications ranging from
skin disease to insanity to death — e.g., sprouted vegetables or grains with meat, milk with meat,
honey with meat, curd with chicken, or fish with jaggery. The Ketabi book states related but more
general food-combining rules ("never eat starches with animal proteins," "always eat fruit on an
empty stomach") as general Ayurvedic law rather than citing the CCRAS documents' more granular,
disease-specific, classically-sourced list. See `05_CROSS_SOURCE_COMPARISON.md` for why this is
flagged as a difference in evidentiary register rather than a resolved contradiction.

## Dinacharya, ritucharya, and disease-specific diet charts

**Dinacharya (daily regimen):** waking near sunrise or during Brahma Muhurta (4:00–5:30am
per the CCRAS guidelines), tongue/eye cleaning, oil massage (abhyanga), daily exercise, bathing, and
grooming — described in near-identical wording across the Ketabi book and both CCRAS documents.

**Ritucharya (seasonal regimen):** dosha-specific dietary shifts across six named seasons — e.g., "in
summer season due to hot climate aggravation of pitta occurs. Hence pitta pacifying cold, liquid,
sweet and oily diet is advised," per the CCRAS cardiac guideline.

**Disease-specific diet charts:** the CCRAS cardiac guideline gives three full-day menus (Vata,
Pitta, Kapha Prakriti Purush) across six meal slots, with specific differences at the same slot —
e.g., bedtime is plain milk for Vata Prakriti, milk with sugar for Pitta Prakriti, and unsweetened
milk (with tea/coffee added in the evening slot) for Kapha Prakriti. The CCRAS skin-disease guideline
gives a parallel Aharaja (food-related causative factor) table for Kushta specifically — e.g., excess
salt (pickles, chips, namkeen), excess sour (fermented foods, vinegar, alcohol), or "guru annapana"
hard-to-digest foods (pizza, cheese, fried bread, red meat).

---

## From 03_REMEDIES_AND_PRACTICES.md

# 03 — Remedies and Practices

Beyond diet, this library's sources describe three tiers of practice: everyday self-care rituals, a
formal detoxification therapy (panchakarma), and a catalog of specific home remedies for named
complaints.

## Daily self-care rituals

From the Ketabi book: oil pulling, tongue scraping, self-oil massage (**abhyanga**), dry brushing,
and **nasya** (nasal therapy) as components of dinacharya, alongside the wake/meal/sleep timing
covered in `02_DIET_AND_DAILY_ROUTINE.md`. Both CCRAS guidelines describe the same core rituals
(oil massage, daily exercise, bathing, tooth/tongue cleaning) in a more clinical register, adding
**udvartana** (dry-powder massage with yava/kola/kulath) in the cardiac guideline specifically.

## The ethical regimen (sadvritta) and urge suppression

Both CCRAS guidelines state a roughly 20-item **sadvritta** (ethical conduct) list: truthfulness,
temper control, moderation, cleanliness, meditation, self-control, patience, kindness, regularity,
and avoiding sensory addiction.

Both CCRAS guidelines also name **13 natural urges that should never be suppressed** (urination,
defecation, flatus, ejaculation, vomiting, sneezing, eructation, yawning, hunger/thirst, tears,
exertion-induced respiration, sleep), each paired with a specific named consequence — e.g.,
suppressing vomiting is said to produce "urticaria, giddiness, anaemia, hyperacidity, skin diseases
and fever." A separate, shorter list of urges (greed, grief, fear, fury, pride, envy) is described as
the opposite case — these should be actively suppressed rather than acted on.

## Panchakarma (detoxification therapy)

The Ketabi book describes classical panchakarma ("five therapies" — basti/enema, nasya/nasal
irrigation, vamana/emesis, virechana/purgation, raktamokshana/bloodletting) as a 3–21-day (typically
5-day) program requiring a strict kitchari (rice + lentil) diet, oil-based therapies, and a
technology/stimulation detox — noting that most modern centers now perform gentler versions (massage,
steam) rather than the full historical five therapies. It also gives a simplified at-home version
with a tridoshic kitchari recipe for readers without facility access.

The CCRAS skin-disease guideline describes a disease-specific panchakarma sequence for Kushta:
**Snehapanam** (internal medicated ghee) prior to **Samshodhana**, then **Swedana** (sudation), then
**Vamana** or **Virechana** depending on the dominant dosha (Vataja kusta: internal medicated ghee;
Pittaja kusta: raktamokshana/blood-letting and virechana/purgation; Kaphaja kusta: vamana/therapeutic
emesis), followed by **Samsarjana krama** (regulated post-therapy diet) and, for excess Vata,
enemas (Asthapana/Anuvasana Vasti) and nasya.

## Home remedies

**From the video** (a psychiatrist's clinical-experience remedies, not classically sourced in the
clip): plain (not Greek, not low-fat) yogurt mixed with water roughly 1:2 to 2.5:5.5, with a pinch of
toasted cumin and pink/Himalayan salt, taken daily for digestive complaints if not lactose
intolerant — offered explicitly as something to try **alongside** seeing a doctor, not instead of.
Also: eating papaya and pomegranate on alternate days for weak or difficult digestion, attributed to
the digestive enzyme papain in papaya. Choosing dosha-appropriate milk (of several possible animal
sources) is described as a targeted remedy rather than treating "milk" as one substance, citing the
classical text Charaka Samhita as comparing different milks and their dosha-specific uses.

**From the Ketabi book**, a larger catalog tied to dosha-based causal stories:
- Constipation (Vata-dominant, dry colon): flaxseed-cumin tea or daily triphala.
- Heartburn (Pitta): aloe vera juice, eliminating garlic/onion/citrus/coffee.
- Three dosha-typed headache patterns (Vata: back/side of head; Pitta: temples; Kapha:
  frontal/sinus), each with a different forehead paste remedy.
- Three dosha-typed PMS patterns with different herbs (Vata: ashwagandha; Pitta: shatavari; Kapha:
  trikatu).

## Scope note

None of these remedies carry peer-reviewed efficacy data within this library's corpus — they are
reported as each source states them (one psychiatrist's clinical experience, or one textbook's
traditional-knowledge catalog), not as trial-tested interventions. Neither CCRAS guideline's home
remedy or panchakarma content addresses conditions outside its own named scope (skin disease;
diabetes, hypertension, and obesity specifically) — this package does not extend either guideline's
recommendations to conditions they don't state.

---

## From 05_CROSS_SOURCE_COMPARISON.md

# 05 — Cross-Source Comparison

This library's five sources span four very different registers (a YouTube video, a general-audience
textbook, two government clinical guidelines, and one unrelated psychology book). Each individual
note's own "Conflicts with other sources" section is the primary, anchor-cited record of these
comparisons; this file summarizes the patterns across all five.

## Strong convergence between the two CCRAS guidelines

Published by the same body (Central Council for Research in Ayurvedic Sciences, Ministry of AYUSH)
in the same guideline series, the skin-diseases and cardiac-disorders documents share near-identical
Ahara/Vihara framing, an identical eight-factor (Ashta ahara vidhi visesha ayatana) food-evaluation
list, and word-for-word overlapping Dinacharya, Ritucharya, Sadvritta, and urge-suppression sections
— down to matching phrasing ("It is advisable to wake up during Brahma Muhurta (preferably between
4.00 a.m. to 5.30 a.m.)"). They diverge only in their disease-specific content: Kushta
etiology/classification and pathya/apathya lists in one, cardiac risk-factor framing and diet charts
in the other. Both also independently name Viruddhahara (dietetic incompatibility) as a contributing
cause — the cardiac guideline alongside Gulma and allergies, the skin guideline as a direct Kushta
cause — a point of genuine overlap, not disagreement.

## Convergence between the video and the Ketabi book on dosha/personality framing

Both describe the same basic Vata/Pitta/Kapha elemental and personality framework — Vata as
quick-learning/quick-forgetting and prone to boredom, Kapha as easy-weight-gain and highly resilient
— though the Ketabi book is far more granular (explicit food lists, taste tables, a formal
self-assessment quiz) where the video relies on informal RPG-stat analogy. Both also independently
state the same elemental composition (Vata = air+ether, Pitta = fire+water, Kapha = earth+water; see
`01_CORE_PRINCIPLES.md`).

## Convergence between the Ketabi book and both CCRAS guidelines on routine and food-combining concepts

The Ketabi book's dinacharya, ritucharya's six-season scheme, and its virudha ahara (dietetic
incompatibility) concept describe the same mechanism the CCRAS guidelines call Viruddhahara — the
Ketabi book's Chapter 3 elemental/dosha framework and its "foods unstable for one's Doshic
constitution" section overlap substantially with the CCRAS documents' equivalent sections.

## A genuine difference in evidentiary register, not a resolved contradiction

The Ketabi book states specific food-combining rules ("never eat starches with animal proteins,"
"always eat fruit on an empty stomach") as general Ayurvedic law. The CCRAS cardiac guideline's food
lists are more narrowly disease-specific and cite named classical texts (Charaka Samhita, Sushruta
Samhita) directly, rather than presenting one general food-combining framework. Neither source cites
the other, and the Ketabi book does not cite classical texts as granularly as the CCRAS documents do
— worth keeping in mind rather than treating claims from the two sources as equally authoritative.

## Same three doshas, non-overlapping domains

The video's dosha-personality framework (cognitive fingerprint, RPG-stat analogies, three depression
subtypes) and the CCRAS skin-disease guideline's strictly clinical/dermatological dosha framework
(Kushta subtype classification, Tridosha-based treatment) describe the same three doshas but apply
them to different domains without directly overlapping, comparable claims. Similarly, the video's
"ayurgenomics" and gut-brain-axis claims run parallel to, but are not sourced from or reconciled
with, the CCRAS cardiac guideline's clinical Madhumeha (diabetes) guidance — both make claims linking
dosha and diabetes susceptibility, independently derived, that neither source engages with directly.

## The one point of contact with the deliberate non-Ayurveda outlier

*Flow* shares no subject matter with the other four sources and was not written with any awareness
of Ayurveda. Its one substantive point of contact is Patanjali's eight-limbed classical Yoga system
(yama, niyama, asana, pranayama, pratyahara, dharana, dhyana, samadhi), which the Ketabi book also
describes as a route to spiritual liberation and dissolution of the self toward union with the
universal (moksha) — while *Flow* explicitly frames the identical eight stages as "a very thoroughly
planned flow activity" whose purpose is to **fortify** the self rather than dissolve it. This is
flagged as the one place in this library where two sources describe the same named practice with
opposite stated goals, rather than merely using different vocabulary for the same claim. Neither
source is aware of or responds to the other — this is an observation about the corpus, not a
resolution of the divergence.

---

## From 06_OPEN_QUESTIONS.md

# 06 — Open Questions

What this small, young corpus doesn't yet resolve, or leaves genuinely unsettled — either because
the sources themselves flag uncertainty, or because they point in different directions.

## Flagged as uncertain by the sources themselves

- **The genomic/"ayurgenomics" and MGUS-meditation research the video cites** is presented with
  varying confidence by the source itself — the ayurgenomics claim with the most specificity, the
  meditation/gene-expression study explicitly hedged ("this may be the first evidence, or there may
  be other evidence — I'm not really sure, because this isn't my area"). Neither has been
  independently checked against anything else in this corpus.
- **The Ketabi book's self-assessment dosha quiz** is explicitly caveated by its own source as
  approximate: "it is not entirely accurate... the best way to truly determine your Doshic
  constitution is by consulting with an Ayurvedic practitioner."
- **The CCRAS skin-disease guideline's past-life/karmic causation claim** (Kulaja Nidana — Kushta
  as transmissible "from past lives") is presented as classical doctrine (citing Sushruta) rather
  than the guideline's own clinical observation, unlike the diet/lifestyle claims that make up the
  bulk of the same document. This library does not have another source addressing this kind of
  causal claim to weigh it against.

## A term the corpus never fully captures

The video's own auto-generated captions never correctly spell the term for a person's current,
deviated dosha state (only "Vic rupee"/"Vic Ruthie") — even though the Ketabi book independently
names and explains the identical concept as **Vikruti**. This library's note on the video does not
assert the two are the same word, since the caption never spells it correctly; a reader should treat
the video's second concept as *probably* Vikruti, not confirmed as such by that source alone.

## How literally should "dosha" be taken?

The four Ayurveda-focused sources use dosha language at different levels of literalness, and this
package does not resolve the difference: the video treats dosha-personality correlation as close to
diagnostic fact; the Ketabi book treats its own quiz as approximate and recommends practitioner
consultation for a real answer; both CCRAS guidelines treat dosha classification as established
clinical doctrine without hedging, for the specific diseases each addresses. A question spanning
more than one source's register should note this range rather than picking one reading.

## Gaps in current coverage

- No peer-reviewed clinical-outcomes research exists in this corpus for any Ayurvedic treatment,
  panchakarma protocol, or home remedy — all such claims trace to clinical experience, classical
  text citation, or traditional-knowledge catalogs, not trials.
- This library covers only two specific disease areas in clinical depth (skin disease; cardiac-risk
  conditions — diabetes, hypertension, obesity) via the CCRAS guidelines. It has no comparable
  clinical guideline for any other disease category.
- *Flow*'s inclusion is a single, deliberate outlier; this library does not yet have a second
  Western-psychology source to know whether the Patanjali-goal divergence noted in
  `05_CROSS_SOURCE_COMPARISON.md` is a one-off mismatch or part of a larger pattern.
- No source in this library addresses Ayurvedic pharmacology, herb-drug interactions, or safety data
  for the specific herbs and remedies named in `03_REMEDIES_AND_PRACTICES.md`.

This file will grow as more sources are added and as genuine disagreements or unresolved questions
surface across new notes.

---

## From 08_QUESTIONS_AND_ANSWERS.md

# 08 — Questions and Answers

Worked answers in this package's house style. Per this project's provenance rule, this file carries
no video-ID or page-number citations — see the individual notes in `notes/` for the anchored source
of every claim summarized here.

**What are the three doshas, and what do they govern?**
Vata (air + ether) governs movement — circulation, elimination, respiration, and the nervous system;
Pitta (fire + water) governs transformation — digestion, metabolism, and body temperature; Kapha
(earth + water) governs structure — bone density, fat, strength, and immunity. All four
Ayurveda-focused sources in this library use this same three-way split, applied to personality, body
type, digestion, and (in the two government guidelines) specific named diseases.

**What's the difference between Prakriti and Vikruti?**
Prakriti is a person's dosha mix at birth — fixed, genetic, unchangeable. Vikruti is a person's
current dosha state, shaped by diet, environment, stress, and age, and is what a symptom or a quiz
actually measures. Ayurvedic treatment, per this corpus, targets bringing Vikruti back toward
Prakriti, not the reverse.

**What does it mean to "eat opposite your dosha"?**
The consistent rule across sources: counterbalance a dosha's own qualities with food of the opposite
quality. Vata (cold, dry, light) eats warm and moist food; Pitta (hot, oily, sharp) eats cold and dry
food; Kapha (cold, oily, heavy) eats warm and dry food.

**What is agni, and why does this corpus treat it as so central?**
Agni is digestive fire. One source in this library extends it beyond physical digestion to emotional
processing (healthy agni is linked to confidence and patience; imbalanced agni to fear or
withdrawal, depending on which of four agni types is affected). A government clinical guideline in
this corpus proposes a specific causal chain from impaired digestive fire through to cardiovascular
disease.

**What is dinacharya, and what does a basic version look like?**
Dinacharya is Ayurveda's daily routine. Across this corpus it typically means: waking near sunrise
(or during "Brahma Muhurta," roughly 4:00–5:30am), tongue scraping, oil pulling, self-oil massage
(abhyanga), daily exercise, bathing, and grooming — described in near-identical terms by three of
this library's four Ayurveda-focused sources.

**Is anything in this library a substitute for seeing a doctor or an Ayurvedic practitioner?**
No. Both government guidelines in this corpus state explicitly that their content should only be
followed under supervision of a qualified, registered Ayurveda practitioner. Even the video's own
home-remedy suggestion is offered as something to try alongside seeing a doctor, not instead of.

**What is panchakarma?**
A detoxification therapy, classically five specific procedures (enema, nasal irrigation, therapeutic
emesis, purgation, and bloodletting), traditionally run over 3–21 days with a strict diet and
oil-based therapies. One source in this corpus notes most modern centers now use gentler versions
(massage, steam) rather than the full historical five, and one government guideline in this corpus
describes a disease-specific panchakarma sequence for skin disease.

**What are the six tastes, and why do they matter?**
Sweet, sour, salty, pungent, bitter, and astringent. This corpus states that all six should appear
in the diet daily, in proportions matched to a person's dosha — each dosha is said to benefit from
some tastes and do worse with others.

**Does gut bacteria affect mood, according to this corpus?**
One source (the video) cites this as supporting evidence for an Ayurvedic gut-brain connection,
describing a study where stool from depressed rats was transplanted into healthy rats, which then
became depressed, plus research linking specific gut bacteria to anxiety levels. No other source in
this library addresses gut-brain mechanisms, so this claim has not been corroborated or challenged
elsewhere in this corpus.

**Why does this library include a book with no Ayurvedic content at all?**
*Flow: The Psychology of Optimal Experience* was added at the user's explicit direction as a
deliberate outlier, not for Ayurvedic fit. Its one real point of contact with the rest of the corpus
is its treatment of Patanjali's eight-limbed classical Yoga — a system another source in this
library also describes, but with the opposite stated goal (fortifying the self versus dissolving
it).

**Can this library answer questions about herbs, supplements, or remedies not named in its sources?**
No. This corpus names a small, specific set of home remedies (a yogurt-cumin-salt digestive remedy;
papaya and pomegranate for weak digestion; specific herbs for headache and PMS patterns by dosha;
flaxseed-cumin tea and triphala for constipation; aloe vera for heartburn). It does not cover
Ayurvedic pharmacology or herb-drug safety data more broadly, and a question about an unnamed remedy
should be answered by saying this corpus doesn't cover it, not by reasoning from general Ayurvedic
knowledge.

**What disease areas do the two government guidelines actually cover?**
Only two: skin disease (grouped under the umbrella term Kushta) and three cardiac-risk-related
conditions — Madhumeha (diabetes), Uchcharaktachapa (hypertension), and Sthaulya (obesity). This
corpus does not contain comparable clinical guidance for any other disease.

