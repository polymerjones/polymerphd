# Polymer Ph.D. — offline reference app

`index.html` is the whole app: 190 notes, 20 knowledge files, 146 glossary terms and
16,272 source timestamps, in one 2.4 MB file. Double-click it. It works offline, makes
no network requests, and contains no model — every word was written during the synthesis
pass and is only being looked up here.

## Rebuilding

After adding videos and notes, regenerate everything:

```
python3 scripts/build_app_data.py
```

It reads `notes/`, `restorative_vitality_knowledge/` and `source_transcripts/manifest.json`,
and writes `data.json` (the dataset alone, for any later consumer) and `index.html` (the
same data gzipped and inlined into `app.template.html`). Nothing outside `app/` is written.

The build refuses to write if a note's id is missing from the manifest, a universal section
is missing, or a timestamp runs past the end of its video. Re-running without changing an
input produces a byte-identical file.

## Editing the app

Edit `app.template.html`, not `index.html` — the latter is generated. The template carries a
`/*__DATA__*/` placeholder where the payload is injected.

## The derived practice filters

Duration, position and equipment are pattern-matched out of the source's own wording, so
they are partial: of 703 practices, 144 state a readable duration, 19 a seated cue, 6 "no
equipment." Everything the matcher could not classify is listed in
`unclassified_practices.txt`. To correct one by hand, add it to `practice_overrides.json`:

```json
{
  "12kGPUoN0BA::heel bounce, 60 in 60 seconds, no equipment": {
    "duration_seconds": 60,
    "position": ["standing"],
    "equipment": "none"
  }
}
```

Overrides win over the matcher. The raw source string always appears on the card regardless,
so a filter can never hide what the material actually said.
