# Working on Polymer Ph.D. — read `CLAUDE.md` first

This repo's actual working instructions live in `CLAUDE.md` at the repo root. Read it in full
before making any change — it covers the video-ingestion pipeline (`scripts/add.sh <slug>` →
write `libraries/<slug>/notes/<id>.md` → `scripts/check_notes.py <slug> <id>` →
`scripts/publish.sh --push`), how to add a brand-new library, and the gotchas around generated
files (`ios/PolymerPhD.xcodeproj/project.pbxproj`, `app/index.html`).

This file exists only because some tools look for `AGENTS.md` specifically and won't otherwise
find `CLAUDE.md`. It is not a separate set of rules — if the two ever disagree, `CLAUDE.md` is
authoritative.

The one rule that matters most, restated here so it survives even a shallow read:

**Nothing in this repository originates outside the source transcripts.** Every claim traces to a
specific video (or other cited source) at a specific timestamp/page/paragraph. Never invent a
timestamp, never supply terminology a source didn't itself use, never add a video-id citation to
a synthesis page (only the `topic_reference_*.md` files carry those). `scripts/check_notes.py
<slug>` catches fabricated anchors — run it before publishing.

`README.md` describes what the project *is*, for a human reader. `CLAUDE.md` describes how to
work on it without breaking the thing that gives it value. Read both.
