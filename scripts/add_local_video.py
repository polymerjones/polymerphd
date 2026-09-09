#!/usr/bin/env python3
"""Ingest a local video file (no YouTube URL, no captions): local Whisper
transcription straight from the file on disk.

Sibling to add_video_whisper.py, minus the yt-dlp fetch steps — for a video
that was never on YouTube at all (e.g. a DVD rip). Duration comes from
ffprobe instead of yt-dlp's info.json; Whisper transcribes the video file
directly (its ffmpeg backend decodes audio from .mp4/.avi/etc without a
separate extraction step). Writes the same [mm:ss]-anchored clean text file
and manifest entry shape as add_video_whisper.py, so the note-writing and
check_notes.py flow afterward is identical.

Anchor format: MM:SS for anchors under an hour, H:MM:SS from the one-hour
mark on — lib_common.ANCHOR_KINDS["timestamp"] accepts both, and several of
these DVDs run past 99 minutes, where a plain-MM:SS anchor would render a
3-digit minute field the anchor regex can't parse (e.g. "[101:19]").

Usage:
  python3 scripts/add_local_video.py <slug> <path/to/video> [--id ID] [--title T]
                                      [--source-note TEXT] [--release-year YYYY]
                                      [--model small] [--device cpu|mps] [--language en]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402

ANCHOR_EVERY_SEC = 60


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "source"


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def timestamp(seconds):
    """MM:SS under an hour, H:MM:SS from the one-hour mark on (both accepted
    by lib_common.ANCHOR_KINDS["timestamp"]; plain MM:SS with 3-digit minutes
    is not)."""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def transcribe(video_path, model_name, device, language):
    import whisper

    print(f"Loading whisper model '{model_name}' (device={device})...", file=sys.stderr)
    model = whisper.load_model(model_name, device=device)
    print(f"Transcribing {video_path.name} — this can take a while for a long file...",
          file=sys.stderr)
    result = model.transcribe(str(video_path), language=language, verbose=False)
    return result["segments"]


def build_body(segments):
    """Group whisper segments into ~60s paragraphs with a leading anchor,
    the same windowing add_video_whisper.py uses for YouTube fallback audio."""
    paragraphs = []
    current = []
    next_anchor = 0.0
    anchor = None

    for seg in segments:
        start, text = seg["start"], seg["text"].strip()
        if not text:
            continue
        if start >= next_anchor or anchor is None:
            if current:
                paragraphs.append(f"{anchor} {' '.join(current)}")
                current = []
            anchor = f"[{timestamp(start)}]"
            next_anchor = start + ANCHOR_EVERY_SEC
        current.append(text)

    if current:
        paragraphs.append(f"{anchor} {' '.join(current)}")

    return "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in paragraphs)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("path", type=Path)
    ap.add_argument("--id")
    ap.add_argument("--title")
    ap.add_argument("--source-note", default=None,
                     help="free-text description of provenance, e.g. a program name "
                          "(stored as SOURCE: in the clean file header)")
    ap.add_argument("--release-year", type=int)
    ap.add_argument("--model", default="small",
                     help="whisper model: tiny/base/small/medium/large-v3/turbo (default: small)")
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps"],
                     help="mps is faster on Apple Silicon but less reliable; cpu is the safe default")
    ap.add_argument("--language", default="en")
    args = ap.parse_args()

    lib = load_library(args.slug)
    if not args.path.exists():
        sys.exit(f"No such file: {args.path}")

    source_id = args.id or slugify(args.path.stem)
    title = args.title or args.path.stem

    duration = ffprobe_duration(args.path)
    dur_str = timestamp(duration)

    segments = transcribe(args.path, args.model, args.device, args.language)
    body = build_body(segments)
    if not body.strip():
        sys.exit("Whisper produced an empty transcript — nothing to write.")

    header = (
        f"TITLE: {title}\n"
        + (f"SOURCE: {args.source_note}\n" if args.source_note else "")
        + f"SOURCE FILE: {args.path.name}\n"
        + (f"RELEASE YEAR: {args.release_year}\n" if args.release_year else "")
        + f"DURATION: {dur_str}\n"
        + f"CAPTION TRACK: whisper-local ({args.model})\n"
        + f"{'=' * 70}\n\n"
    )

    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{source_id}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    manifest = lib.load_manifest()
    sources = [s for s in manifest.get("sources", []) if s["id"] != source_id]
    sources.append({
        "id": source_id,
        "kind": "video_local",
        "title": title,
        "url": None,
        "source_file": args.path.name,
        "release_year": args.release_year,
        "duration_seconds": duration,
        "duration": dur_str,
        "word_count": len(body.split()),
        "clean_file": f"clean/{source_id}.txt",
        "transcript_source": f"whisper-local:{args.model}",
        "anchor": {
            "kind": "timestamp", "format": "mm:ss",
            "bound_field": "duration_seconds", "bound": duration,
        },
    })
    sources.sort(key=lambda r: r["title"].lower())
    lib.save_manifest({**manifest, "sources": sources})

    print(f"Wrote {clean_path}")
    print(f"  {len(body.split())} words, {len(segments)} whisper segments, id: {source_id}")
    print(f"  Write libraries/{args.slug}/notes/{source_id}.md, then:")
    print(f"  python3 scripts/check_notes.py {args.slug} {source_id}")


if __name__ == "__main__":
    main()
