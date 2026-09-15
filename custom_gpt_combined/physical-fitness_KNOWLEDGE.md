# Physical Fitness

## From 00_README.md

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

---

## From 01_CORE_PRINCIPLES.md

# 01 — Core Principles

This library holds 14 sources from one program — RUSHFIT — so the patterns below are not
cross-creator convergence the way they would be in a multi-source library; they are principles
the program itself states and restates, often nearly verbatim, across independent DVDs and
guides. That repetition is still worth naming: it marks what the program treats as load-bearing
rather than incidental.

---

## 1. Quality of repetition beats quantity, stated as the program's central rule

Repeated across more sources than any other single idea: `foundation-moves` ("quality over
quantity... don't try to use a bunch of weight"), the Workout Guide's equipment page ("It's not
how much weight you lift! The secret to the results comes from endurance and the strength built
up by pushing your body through maximum reps — not maximum weight"), `strength-and-endurance`'s
"no magic pill" framing, and `explosive-power-training`'s explicit rep caps (as few as 3-5 reps
per set) specifically to preserve movement quality over volume. The program applies this same
rule to two different training modes — grinding-endurance circuits and explosive plyometrics —
which is what makes it a principle rather than advice tied to one workout style.

## 2. Core activation is the prerequisite to every other movement, not one exercise among many

`foundation-moves` states this as a foundational concept before covering any dumbbell movement:
"We have to activate the core before we squat. We don't want to have a loose core because then
everything tumbles in." `abdominal-strength-and-core-conditioning` extends it into a mechanistic
claim about striking power itself — core as "the bridge" between leg drive and knuckle contact.
Nearly every workout note's "Form cues" section independently names a core-activation failure
(hip sag, rounded back, collapsing plank) as the root cause of a specific technical fault, not a
separate issue from it.

## 3. The safety line is pain, not imperfect form

Stated explicitly as the program's philosophy in `balance-and-agility`'s closing discussion
("he's not doing it to the point where he feels joint pain... he's pushing to his full potential")
and restated as a formal rule in the Workout Guide ("You should never do anything that is painful
or could cause injury"). Cheating a rep, skipping reps, or falling short of perfect form is
explicitly sanctioned throughout the corpus; a rep that produces pain is not — this distinction is
drawn consistently enough across independent sources to treat as the program's actual safety
standard, distinct from technical perfection.

## 4. Functional training exposes an individual's weak link — and the program uses GSP's own as the example

`strength-and-endurance` and `full-body-strength-and-conditioning` both build entire sessions
around GSP naming his own limitation directly: explosive, fast-twitch strength is his comparative
advantage, sustained isometric/endurance work is his admitted weakness. `explosive-power-training`
independently confirms the inverse — Erik calls explosiveness "one of my favorite workouts" for
GSP specifically because it's his strength. The two DVDs read as a matched pair describing the
same athlete's profile from opposite sides, not independent claims.

## 5. The vertical-to-horizontal transition is named as the specific mechanism behind fight fatigue

Stated independently in `the-fight-conditioning-workout` ("that vertical to horizontal. Going down
and up. It really tires out the body") and `full-body-strength-and-conditioning` ("this is what
makes mixed martial arts so difficult... going horizontal to vertical"). This is the stated design
rationale behind combining striking/standing work with groundwork/takedowns in the same round,
rather than training them in separate sessions.

## 6. Warm-up and cool-down are treated as load-bearing, not optional bookends

Every workout DVD in the corpus opens with the identical Rush Fit Warmup and closes with the
identical stretch sequence, and multiple sources state directly why: the warm-up's value is "the
form... not the repetition" (`balance-and-agility`), and the cool-down is reframed repeatedly as
more than physical — "a way to change my mind... from being the athlete... to the everyday normal
guy" (stated identically across `the-fight-conditioning-workout`, `full-body-strength-and-conditioning`,
`abdominal-strength-and-core-conditioning`, `strength-and-endurance`, and `explosive-power-training`).

## 7. Flexibility work is explicitly framed as necessary counterbalance, not lesser priority

`stretch-for-flexibility` states this directly as "the yin to the yang" of the harder conditioning
sessions, backed by GSP naming his own cost for neglecting it (a competition adductor injury, and
years of skipped post-workout stretching). This isn't presented as a nice-to-have recovery add-on
but as equally necessary maintenance, with its own dedicated DVD.

## 8. Individual variation is repeatedly named rather than smoothed into one standard

"You always have one side better than the other. That is normal" appears, in close paraphrase,
across `balance-and-agility`, `stretch-for-flexibility`, and `strength-and-endurance`. Every
workout note documents at least one explicitly sanctioned modification (kneeling, shortened range
of motion, a substituted easier variant) presented as equally legitimate, not a lesser fallback —
this is a consistent structural feature of how the program teaches every movement, not just a
courtesy aside.

---

Every other file in this package applies one or more of these patterns to a specific topic —
technique, protocol structure, or form cues.

---

## From 02_MOVEMENTS_AND_TECHNIQUE.md

# 02 — Movements and Technique

The corpus teaches its movement vocabulary in one place — `foundation-moves` — then reuses and
occasionally deepens it across the other eight DVDs. This file indexes where each movement is
taught in full and where it's extended; it does not re-derive the technique cues themselves —
see the named note for those, quoted with anchors.

## Bodyweight foundation movements

Taught in full in `foundation-moves`: squat, lunge (four directions), push-up, sit-up, back
extension, rotation, core activation, burpee/squat thrust. Each carries a named common fault and
at least one sanctioned modification (see `04_SIGNALS_AND_SELF_ASSESSMENT.md` for the fault/fix
pairs specifically).

These same movements reappear inside the shared Rush Fit Warmup (`balance-and-agility`,
`stretch-for-flexibility`, `the-fight-conditioning-workout`, `full-body-strength-and-conditioning`,
`abdominal-strength-and-core-conditioning`, `strength-and-endurance`, `explosive-power-training`,
`bonus-workouts`) at a brisker pace with less fault-and-modification detail — `foundation-moves`
is the corpus's only deep technical treatment of them.

## Dumbbell foundation movements

Also taught in full in `foundation-moves`: addressing the dumbbell, dumbbell squat, dumbbell
lunge, dumbbell standing press, dumbbell row, upright row/high pull, dumbbell power clean,
dumbbell swing, dumbbell get-up. `full-body-strength-and-conditioning`,
`abdominal-strength-and-core-conditioning`, and `strength-and-endurance` each run the entire
`foundation-moves` DVD again in full as their closing segment — the technique content is
identical in all four places.

Two DVDs extend specific dumbbell movements beyond what `foundation-moves` covers:

- **`explosive-power-training`** trains the power clean and push press as *explosive*,
  rep-capped movements rather than the controlled, deliberate versions `foundation-moves` teaches
  — same mechanics, different intent (see `01_CORE_PRINCIPLES.md` §1).
- **`strength-and-endurance`** introduces the dumbbell "around the world" (a torso-rotation swing
  not covered in `foundation-moves`) and the half get-up as a standalone core movement tied
  explicitly to the "hip heist" fight application.

## Fight technique (striking, kicks, and grappling)

Taught only in `the-fight-conditioning-workout`, in a dedicated closing section that pairs each
technique's real-fight application with its solo workout adaptation: fighting stance, footwork
(forward/back, lateral, pivot), jab, cross, hook, uppercut, rear vertical elbow, front elbow, rear
knee, front kick, roundhouse kick, defensive side kick, checking a kick, level change, sprawl, the
shot/takedown setup, slam, uchi-mata, hip escape, the "hip heist," armbar, kimura, triangle choke,
and the standing guard pass. No other DVD in the corpus covers combat technique directly — the
other eight are body-weight/dumbbell conditioning built from these same movement patterns without
naming the technique they mirror.

## A term inconsistently auto-transcribed across three sources

The "hip heist" (standing up from beneath an opponent, sourced to GSP's own BJJ vocabulary) is
transcribed three different ways by Whisper in three different notes: "hip eyes"
(`foundation-moves`), "hip-hist"/"hip-high" and "hip ice" (`the-fight-conditioning-workout`), and
correctly-adjacent phrasing in `strength-and-endurance`. Each note preserves its own source
file's literal (garbled) wording rather than silently normalizing to the likely-intended spelling
— see `05_CROSS_SOURCE_COMPARISON.md` for why.

## The training-camp technique link (from the guides)

The Workout Guide's "training philosophy" pyramid (`rushfit-workout-guide`) explicitly names
technique — "throw a proper jab, cross, left hook, elbow or knee" — as the *next* tier up from
this conditioning program's own scope, requiring the conditioning base first. The fight-technique
breakdown in `the-fight-conditioning-workout` is the corpus's only source that actually delivers
technique instruction rather than conditioning built from technique-shaped movement patterns.

---

## From 03_PRACTICES_AND_PROTOCOLS.md

# 03 — Practices and Protocols

## Two distinct interval formats, deliberately different

Most conditioning DVDs (`the-fight-conditioning-workout`, `full-body-strength-and-conditioning`,
`abdominal-strength-and-core-conditioning`, `strength-and-endurance`) use **time-boxed,
max-effort rounds**: a fixed window (30-60s, sometimes 2-5 minutes), as many quality reps as
possible, explicitly not capped. `explosive-power-training` uses the opposite format
deliberately: a **hard rep cap** (8 max in round 1, 3-5 max afterward) regardless of remaining
time, because the goal is preserving the stretch-shortening cycle's explosiveness rather than
accumulating fatigue — see `01_CORE_PRINCIPLES.md` §1. Both formats are described as intentional
choices matched to what each session trains, not a stylistic accident.

## The RUSHFIT Fitness Assessment

Four exercises — squat, push-up, sit-up, burpee — each performed for 60 seconds at maximum
effort with a 20-second break between. Introduced conceptually in `rushfit-workout-guide` (with
GSP's own reference scores: 75 squats, 57 push-ups, 55 sit-ups, 22 burpees) and walked through
step-by-step in `bonus-workouts`. Framed explicitly as a repeatable progress-tracking tool, not a
pass/fail test — first-attempt scores below GSP's are named as an expected, normal outcome in
both sources independently.

## Addressing the dumbbell

A named technique in its own right (`foundation-moves`): set weights on a chair, table, or rack
at knee-to-waist height, and pick them up with a flat, neutral spine rather than bending over a
floor-level weight. GSP names his own occasional violation of this as bad-but-survivable form due
to a strong core, explicitly warning against relying on that same margin ("just because you can
get away with it, you should try not to").

## Nutrition timing and macros

`rushfit-nutrition-guide` gives a personal-BMR-based calorie target (height/weight/age/gender
formula × an activity multiplier tied to weekly training frequency), then a near-mirror-image
macro swap around training: 65% carbs / 35% protein / 10% fat pre-workout, versus 35% carbs / 55%
protein / 10% fat post-workout. A stated floor (1,200 calories/day minimum) and a stated healthy
pace (1-2 lbs/week) bound the weight-loss guidance on both ends.

## Heart-rate training zones

`rushfit-workout-guide` sets a blanket target of 60-80% of max heart rate (220 minus age) for
general training, with a five-zone chart (Zone 1 "healthy heart" 50-60% through Zone 5
"red-line" 90-100%) reproduced identically in all three training calendars for reference.

## The three-tier calendar progression

`rushfit-beginner-training-calendar`, `rushfit-intermediate-training-calendar`, and
`rushfit-advanced-training-calendar` each sequence the same seven DVDs across the same 8 weeks,
with the identical equipment (2-25 lb dumbbells) and the identical midpoint cardio-dosage increase
(30 min → 40+ min at Zone 3). What actually varies between tiers, confirmed by direct comparison:

- **Beginner** has the most built-in rest — 10 rest days across 56, including two extra
  mid-week rest days (11, 31) neither harder tier includes.
- **Intermediate** compresses to a strictly weekly rest cadence (8 rest days) and introduces
  Full Body Strength and Conditioning and Explosive Power Training earlier and more often than
  Beginner.
- **Advanced** keeps Intermediate's weekly rest cadence but adds same-day double sessions
  (AM/PM splits, including two full workout DVDs on some days) — the one calendar in the corpus
  built around session-doubling rather than added frequency alone.

All three point to the RUSHFIT Assessment and the Foundation Moves DVD as prerequisites before
starting the grid itself.

---

## From 04_SIGNALS_AND_SELF_ASSESSMENT.md

# 04 — Signals and Self-Assessment

Named fault-and-fix pairs, collected from each note's own "Form cues and body signals addressed"
section. Grouped by what the signal indicates, not by which DVD it appears in — several of these
recur nearly verbatim across independent sources (see `05_CROSS_SOURCE_COMPARISON.md`).

## Unconditional faults (never acceptable, regardless of fatigue)

- **Knees buckling inward** during any squat variation — `foundation-moves` calls this "a
  definite no-no," distinct from every other fault in the corpus, which is graded by severity.
- **Looking at the weight during a swing** (risks spinal overextension) — `foundation-moves`,
  `full-body-strength-and-conditioning`.
- **Taking your eyes off the weight during a get-up** (risk of being struck by it) —
  `foundation-moves`, `full-body-strength-and-conditioning`, `strength-and-endurance`.

## Fatigue signals that call for a specific, named adjustment (not stopping)

- **Hip sag** (plank, row, lateral plank) → the specific symptom of core fatigue; the fix is
  lifting the hips, not resting — `abdominal-strength-and-core-conditioning`,
  `strength-and-endurance`.
- **Body tilting during a stability hold** → named directly as core fatigue, fixed by widening
  the base, not by trying harder at the same width — `abdominal-strength-and-core-conditioning`.
- **A wobbling, unstable single-leg movement** → add a support point (foot down, brace arm), not
  a sign to abandon the movement — `full-body-strength-and-conditioning`, `balance-and-agility`.
- **Losing balance and needing to step down** → explicitly normalized as "natural and normal,"
  not a failure — `balance-and-agility`, `strength-and-endurance`.
- **A decline in form under fatigue** → expected and acceptable up to the point of "complete
  decay," which is the actual stopping signal — `strength-and-endurance`,
  `bonus-workouts` (RUSHFIT Assessment).

## Breathing as a monitored signal, not background

- **Breath held or restricted during a plank/isometric hold** → "keep everything in place... try
  to breathe into the back of the lungs" — `foundation-moves`.
- **Inability to breathe normally in a stretch position** → the position itself is too
  aggressive; back off — `stretch-for-flexibility`.
- **A specific breathing-under-fatigue cue**: "the body is like a straw. If you bend the straw,
  the air doesn't go through" — stay upright rather than folding over when winded —
  `full-body-strength-and-conditioning`.

## Stretch/flexibility-specific ceiling

- **No-discomfort is the stated ceiling for every held stretch**, repeated near-verbatim across
  `stretch-for-flexibility` and `the-fight-conditioning-workout`'s cool-down: "It's not supposed
  to feel any pain... your body will naturally allow you to go a little bit further each time" —
  forcing past that point is named as counterproductive ("you tear muscle and become less
  flexible in the end"), not just risky.

## Balance-specific cue

- **Fixing your gaze on a stationary point** is the corpus's consistent balance cue, stated
  identically in `balance-and-agility` ("if I look this way, I'll fall down... stay looking right
  at your target") and `abdominal-strength-and-core-conditioning`.

## The program's one blanket rule tying all of the above together

`rushfit-workout-guide`: "You should never do anything that is painful or could cause injury" —
stated as a formal rule, not an in-workout aside, and the same line every workout DVD's own
closing philosophy discussions independently arrive at (most explicitly in `balance-and-agility`).

---

## From 05_CROSS_SOURCE_COMPARISON.md

# 05 — Cross-Source Comparison

This is a single-program corpus, so "cross-source comparison" here means something different than
in a multi-creator library: not disagreement between independent voices, but how the *same*
production deliberately reuses, extends, or occasionally repeats itself verbatim across nine DVDs
and five guides.

## Verbatim shared modules

- **The Rush Fit Warmup** opens all eight workout DVDs (every one except `foundation-moves`
  itself) with identical cueing, down to the same "body is like an elastic" line.
- **The cool-down stretch sequence** closes `the-fight-conditioning-workout`,
  `full-body-strength-and-conditioning`, `abdominal-strength-and-core-conditioning`,
  `strength-and-endurance`, and `explosive-power-training` identically, including the same
  closing "changing my mind" framing word-for-word.
- **`foundation-moves` is re-run in full** as the second half of `full-body-strength-and-conditioning`,
  `abdominal-strength-and-core-conditioning`, and `strength-and-endurance`.
- **`stretch-for-flexibility` and `balance-and-agility` are re-run in full** inside
  `bonus-workouts`, which otherwise contributes only the RUSHFIT Assessment as new content.

This confirms the shared modules are a deliberate production choice (a fixed warm-up/cool-down
module, and closing-DVD "review" pattern), not coincidental overlap between independently written
sessions.

## The same athlete, described from opposite sides

`strength-and-endurance` builds its entire session around GSP naming isometric/endurance work as
his personal weakness ("I'm a more fast-switch muscle-oriented guy... this is my weakness").
`explosive-power-training` independently confirms the inverse from Erik's side: "George has
incredible explosive power. And this is the way you get it, plyometric training. It's one of my
favorite workouts." Neither note cites the other, but read together they describe one consistent
athletic profile.

## A recurring personal catchphrase, not a one-off line

GSP's "I'm in pain right now, but I know that's what I need" appears twice in
`full-body-strength-and-conditioning` and in close paraphrase as "the worst day of my life... but
that's what I need" in `bonus-workouts`' RUSHFIT Assessment segment — the same rhetorical move
(naming the pain honestly, then reframing it as purposeful) recurs rather than being confined to
one video.

## A term the corpus can't spell consistently

The "hip heist" (see `02_MOVEMENTS_AND_TECHNIQUE.md`) is auto-transcribed three different ways —
"hip eyes," "hip-hist"/"hip ice," and a third rendering in `strength-and-endurance` — across three
independent DVDs. Each note preserves its own source file's literal wording rather than silently
normalizing to a single "correct" spelling, consistent with this project's rule against importing
terminology the source itself didn't clearly state. The consistent underlying *concept* (standing
up from beneath an opponent via a hip-driven motion) is the same across all three, which is how we
know it's one term garbled three ways rather than three different things.

## The Workout Guide and Nutrition Guide are a linked pair, not independent documents

`rushfit-workout-guide`'s Personal Information Worksheet points readers to the Nutrition Guide's
BMR calculation, and the Nutrition Guide's own BMR section points back to the Workout Guide's
worksheet to record the result. Each PDF cites the other by page number.

## Extension, not repetition: technique depth increases with each pass

`foundation-moves` teaches the base version of every bodyweight and dumbbell movement.
`the-fight-conditioning-workout`'s closing technique section is the only source that names the
*fight application* behind movements `foundation-moves` and `strength-and-endurance` teach purely
as conditioning (the get-up as "hip heist," the sprawl/level-change as takedown defense) — later
sources add fight-specific meaning to movements earlier sources already taught mechanically.

---

## From 06_OPEN_QUESTIONS.md

# 06 — Open Questions and Gaps

## No outside evidence anywhere in this corpus

Unlike `dupuytren` or `nutrition`, nothing in this library cites a study, a named researcher, or
an external data source. Every claim is the program's own coaching rationale or GSP's personal
account. This isn't a gap to fix — it accurately reflects what kind of source material this is —
but it means questions like "is this actually the most effective protocol" have no answer this
library can give; it can only report what the program itself claims and how confidently.

## Two PDF pages could not be independently text-extracted per calendar

All three training calendar PDFs have a page (the heart-rate-zone chart) and the front cover that
extracted no usable text at all — not garbled, simply empty, because those pages are pure
graphics. This library's calendar notes were written from direct visual inspection of the
rendered pages rather than the text layer, and say so explicitly. If those PDFs are ever
re-ingested with OCR tooling, it's worth re-checking whether OCR recovers anything beyond what
was already read directly.

## The Quick Start Guide and box-art covers were deliberately excluded

`Rushfit Quick Start Guide.jpg` restates the Workout Guide's own six points in condensed form with
no new content — confirmed by direct comparison, not skipped for convenience. The DVD box-art
covers are marketing images with no informational text beyond what a cover conveys visually
(reused only as source material for this library's icon/splash images, not as a note).

## Only one program is ingested so far

The library's `program` facet and `multi_channel`-style attribution are set up to hold other
home-fitness programs later, but none exist yet. Every cross-source comparison in
`05_CROSS_SOURCE_COMPARISON.md` is necessarily within-program, not across programs.

## The fight-technique depth is uneven across the corpus

Only `the-fight-conditioning-workout` names striking/kicking/grappling technique directly by its
real-fight application. The other eight sources teach the same underlying movement patterns
(squat, lunge, level change, sprawl) purely as conditioning, without stating the technique they
mirror — so a reader asking "how is X used in an actual fight" for most named movements will only
find an answer if that movement happens to be one of the ones `the-fight-conditioning-workout`
or `foundation-moves` explicitly ties to a fight application (the get-up/"hip heist" being the
clearest case).

---

## From 08_QUESTIONS_AND_ANSWERS.md

# 08 — Questions and Answers (worked examples)

These are worked examples of the house style this package's Custom GPT should follow: answer from
the corpus, cite the source note, and say plainly when the corpus doesn't cover something rather
than filling the gap with outside fitness knowledge.

---

**Q: My knees cave in when I squat. Is that a big deal?**

Yes — this is one of the only faults in the entire corpus called out as unconditional rather than
graded by severity. `foundation-moves` states directly: "This is a definite no-no. We want the
knees coming out." The fix offered is widening your stance slightly and going shallower rather
than continuing at full depth with the knees caving.

---

**Q: I can't do a full sit-up without it hurting my back. What do I do?**

Every source that teaches the sit-up offers the same named substitution: an abdominal crunch
(lifting only the shoulder blades off the ground, not the full torso). `foundation-moves` frames
this explicitly as a legitimate variation, not a lesser one: "there's nothing wrong with just
doing an abdominal crunch variation... eventually as you get stronger, work yourself into a full
range of motion."

---

**Q: Why does the program spend a whole DVD on stretching?**

`stretch-for-flexibility` states this directly as the reason: flexibility work is "the yin to the
yang" of the program's harder conditioning sessions — necessary to maintain joint health and
range of motion, not optional recovery. GSP backs this with a personal cost for skipping it: a
competition adductor injury he now manages with a weekly stretch, and an admitted years-long habit
of skipping post-workout stretching that he says he's still making up for.

---

**Q: What's the difference between the Beginner, Intermediate, and Advanced calendars?**

Same seven DVDs, same equipment, same midpoint cardio increase across all three. What actually
differs: Beginner has two extra rest days (10 total vs. 8) that the other two tiers don't
schedule; Intermediate introduces the harder DVDs (Full Body Strength and Conditioning, Explosive
Power Training) earlier and more often than Beginner; Advanced is the only tier that schedules two
full workouts on the same day (one AM, one PM), which is the real structural difference between
it and Intermediate. See `rushfit-beginner-training-calendar`, `-intermediate-`, and `-advanced-`
for the specifics.

---

**Q: How many calories should I be eating to lose weight on this program?**

The corpus gives a calculation, not a fixed number: your Basal Metabolic Rate (from
`rushfit-nutrition-guide`'s height/weight/age/gender formula) multiplied by an activity factor
tied to how many days a week you train (×1.2 for 1-2x, ×1.4 for 2-4x, ×1.6 for 4-6x), then a
deficit below that number. The guide names a floor: never go below 1,200 calories/day, and a
healthy pace of 1-2 lbs/week — eating too little is stated to backfire by triggering fat storage
rather than helping.

---

**Q: Is it okay if one side of my body is noticeably weaker or less coordinated than the other?**

Yes — this is stated as a normal, expected asymmetry across at least three independent sources
(`balance-and-agility`, `stretch-for-flexibility`, `strength-and-endurance`), not something to
correct before continuing. `strength-and-endurance` even gives a specific reason: "your brain is
not used to work equally both sides."

---

**Q: Does this corpus say anything about supplements, or specific medical conditions?**

No. This is a gap worth naming plainly rather than filling from outside knowledge: nothing in
this library discusses supplements, and the only medical guidance anywhere in the corpus is a
repeated instruction to consult a physician before starting (`rushfit-workout-guide`) and a
warning against training through pain (stated identically across several notes). Anything beyond
that is outside what this corpus covers.

