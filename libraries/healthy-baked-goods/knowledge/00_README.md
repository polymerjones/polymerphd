# 00 — README

**Polymer Ph.D. — Healthy Baked Goods knowledge package**

This folder contains a synthesised knowledge base built from **Instagram recipe reels**,
one at a time, from many different creators — there is no single channel or author behind
this library.

---

# What this is

**This package synthesises individual Instagram recipe posts, each treated as its own,
independent source.** Every claim in it traces back to a specific post's caption, comments,
or on-screen/spoken content, at a specific paragraph or timestamp.

**Nothing in this package originates outside the source posts.** A recipe's ingredient
list, method, and any substitution notes are exactly what the creator stated — including
their own hedges ("I haven't tried this, but...").

---

# What was processed

| Measure | Figure |
|---|---|
| Recipes written up as structured notes | **1** |
| Source platform | **Instagram (reels)** |
| Knowledge files in this package | **2** (this README and the glossary) |

---

# The files

| File | Contents |
|---|---|
| **`00_README.md`** | This file |
| **`07_PLAIN_ENGLISH_GLOSSARY.md`** | Any technical baking terms the notes introduce, defined in plain language, no citations |
| **`09_SOURCE_CATALOG.md`** | Every recipe — ID, title, creator, URL, upload date, facets. **Generated mechanically from the notes**, so it stays complete as more videos are added |

A fuller synthesis — cross-cutting substitution guidance, an ingredient-by-ingredient
reference, patterns across creators — is deliberately not written yet. With only one note
from one creator, that kind of synthesis would mostly restate one note's own words; per
this project's standing practice, whether to add it is a judgement call revisited as more
recipes are added, not a gap to paper over now.

---

# What the package covers

- **Individual recipes exactly as one creator presented them** — ingredients, method, and
  any stated substitutions or variations.

# What the package does not cover

- **Nutrition analysis.** No note states macro or calorie figures unless the creator
  themselves stated one; nothing here is calculated or estimated.
- **A single creator's point of view, presented as consensus.** Each note is one creator's
  own recipe and claims — conflicting or overlapping recipes from other creators are noted
  in each note's own `## Conflicts with other sources` section as they're added.

---

# Upload guidance

Upload the files in this folder to a Custom GPT's knowledge base, following the same
pattern used for this project's other libraries — see `PASTE_INTO_GPT_INSTRUCTIONS.txt`
for the system prompt.

**Suggested setting:** turn web browsing **off**, so the GPT answers from these sources
rather than the open internet.

---

*Built from 1 Instagram recipe reel so far, from 1 creator.*
