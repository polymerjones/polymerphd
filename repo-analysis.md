# Polymer Ph.D. — repo analysis and product advice

## Executive summary

This repo is a transcript-derived knowledge system, not a typical web app. It turns source videos and transcripts into structured notes, synthesised knowledge files, and then packages that material into an offline reference app.

The most important design choice is that the content is constrained by provenance: every claim is meant to trace to a source video and timestamp. That is the core value proposition.

The product is strongest when it is treated as a serious evidence-first reference layer, not as a generic AI app. The next gains will come from improving editorial clarity, navigation, and synthesis rather than adding more raw data.

---

## What the repo is doing

The project has three main layers:

1. Source capture and normalization
2. Structured note authoring
3. Synthesised knowledge and app packaging

The repository structure makes this obvious:

- libraries/<slug>/notes/ contains per-video note files
- libraries/<slug>/knowledge/ contains synthesised knowledge files
- libraries/<slug>/sources/ contains raw and cleaned transcripts plus manifest metadata
- app/ contains the packaged offline app
- scripts/ contains the build and validation pipeline

This is not a “chat with PDFs” project. It is closer to a research and reference archive with a consumer interface.

---

## How the app works

### 1) One library per domain

Each library is a self-contained content domain, for example:

- restorative-physiology
- nutrition
- dupuytren
- additional channels as they are added

Every library has its own:

- config file
- notes
- knowledge files
- source transcripts
- metadata manifest
- custom GPT instructions

The configuration file is the real schema definition. For example, the file at libraries/restorative-physiology/library.json defines the facets, section headings, label mapping, attribution, and file constraints.

### 2) Notes are the evidence layer

The note files are structured markdown entries with frontmatter and universal sections. The project is designed so that the note carries the real source-backed evidence.

This matters because the note layer is the “source of truth” for the project. The synthesis files are derived from the notes, not from raw transcripts.

The note schema is intentionally strict:

- frontmatter facets
- standard sections for each note
- source-specific sections in between
- timestamp anchors everywhere substantive claims are made
- explicit conflict section with other sources

This is a strong editorial discipline and is one of the project’s biggest strengths.

### 3) The knowledge files are curated synthesis

The repo clearly distinguishes between:

- notes: direct, traceable source material
- knowledge files: higher-level synthesis and interpretation

The README makes this explicit: the catalog file updates automatically, but the other synthesis files do not automatically regenerate and must be reviewed by judgement.

That is a good design because it prevents the system from becoming over-automated or “hallucination-friendly.”

### 4) The app bundle is generated, not hand-written

The build pipeline in scripts/build_app_data.py assembles the app from the library data.

It reads:

- notes
- synthesised knowledge files
- source metadata
- derived facet corrections

Then it writes:

- app/data/<slug>.json for each library
- app/index.html as a self-contained offline app bundle

The app is deliberately built as a single HTML archive so that it works offline and makes no network requests.

### 5) The web app and native iOS app share the same underlying data

There are multiple delivery paths:

- GitHub Pages/web app
- offline local HTML app
- iOS wrapper in ios/

This is a good architecture because the same content can be consumed in multiple ways while preserving the same source-backed structure.

---

## Why the repo is strong

### Provenance-first thinking

This is the foundation. The project does not pretend to be an unconstrained model. It is intentionally designed to stay tied to source material.

That gives it:

- trustworthiness
- editorial integrity
- defensibility
- a clear product identity

### Good separation of concerns

The project separates:

- raw source ingestion
- structured note writing
- synthesis
- packaging
- delivery

That separation is important. It reduces the chance that a sloppy model or a rushed script pollutes the final product.

### Offline-first product design

The app is designed to run without network access. That is a meaningful product feature, especially for reference and study tools.

This is a more durable product idea than “web app plus API.”

### Source-backed educational value

The project is not just a database. It is a training and learning system built from source material. That creates a strong niche.

It feels especially suited for:

- self-directed learning
- deep study of specialist topics
- careful review of claims and evidence
- searchable reference workflows

---

## Biggest product opportunity

The biggest opportunity is not adding more content; it is improving the experience of understanding the content.

Right now the system is strong at evidence capture and retrieval. The next move is to make the app more editorial and navigable.

### I would prioritize these improvements:

#### 1) Better concept navigation

Add stronger paths between:

- topic → related videos
- symptom → relevant practices
- practice → safety context
- concept → source evidence

This can turn the app from a library into a learning system.

#### 2) Stronger “confidence / disagreement / consensus” surfaces

Your material is already rich in source-stated confidence and conflicts. That could be more visible in the UI.

Examples:

- “high confidence” vs “inference” labels
- “consensus across sources” summaries
- “disagreement across sources” sections
- “what remains uncertain” badges

This would make the app feel more intellectually honest and more useful.

#### 3) Better summaries for non-expert users

The repo is highly structured, but it could still use more “plain-language synthesis” at the front of each topic.

For example:

- “What this is about in one paragraph”
- “What to watch for first”
- “What is strongly supported vs tentative”
- “What the source itself said about safety”

This would help users without requiring them to read every note.

#### 4) Better compare mode

The project already tracks conflicts between sources. That is a natural fit for a compare view:

- compare two videos on the same concept
- compare two practices
- compare safety framing
- show convergence or disagreement over time

This is a really strong product feature.

#### 5) Study workflows

The app could evolve from “browsing knowledge” to “guided learning.”

Possible flows:

- build a study plan around a symptom
- read a summary and then source evidence
- follow a practice with contraindication warnings
- move from general concept to specific note to source timestamp

---

## Risks and watch-outs

### 1) The app can become too archival

A great risk is that the system becomes a dense archive with excellent evidence but poor usability.

That would still be valuable, but it would limit adoption.

### 2) Synthesis could drift from source material

The README explicitly warns that synthesis files are not automatically updated and require judgement. That is correct and wise. The project should preserve this discipline.

### 3) The app may need clearer product intent

This repo is not obviously “AI” from the outside. It is more like a serious evidence-backed reference tool.

That is a strength, but it needs a crisp product story so users understand what makes it different.

---

## The real differentiator

The real differentiator is not the app UI alone.

It is the combination of:

- transcript-origin discipline
- structured evidence logging
- source-backed note creation
- library-based organisation
- offline app distribution
- synthesis without fabricated claims

This is a remarkably thoughtful foundation for a research or educational product.

---

## My recommendation

If you want to make this even more amazing, I would focus on the following order:

1. Add clearer editorial summaries and “what matters” layers
2. Improve cross-linking between concepts, symptoms, practices, and sources
3. Expose confidence and disagreement more clearly in the UI
4. Build comparison and study flows
5. Keep the source-first discipline as a premium feature

That will preserve the strengths of the repo while making it more accessible and product-ready.

---

## Bottom line

This repo already has a strong foundation and a distinctive identity. It is not a generic website or chatbot project; it is a careful, evidence-bound knowledge product.

The most promising next step is to turn that evidence archive into a more guided, editorial, and educational experience without losing the rigor that makes it valuable in the first place.
