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
