#!/usr/bin/env python3
"""Ingest a YouTube video that has NO captions: local Whisper transcription.

Falls back to this only when add.sh's normal caption-fetch pipeline finds
nothing (normalize.py reports "no captions"). Downloads audio with yt-dlp,
transcribes it locally with openai-whisper, and writes a [mm:ss]-anchored
clean text file and manifest entry in exactly the same shape normalize.py
produces for a captioned video — the note-writing and check_notes.py flow
afterward is identical either way.

The one difference that matters for provenance: the clean text file's
CAPTION TRACK header line says "whisper-local (<model>)" instead of an
en-orig/en YouTube caption track name, so it's always visible on disk that
this transcript came from local speech recognition, not YouTube's own
captions — a materially different (independently generated, not
uploader/YouTube-supplied) source of possible transcription error.

Usage:
  python3 scripts/add_video_whisper.py <slug> <youtube_id_or_url>
                                        [--model turbo] [--device cpu|mps]
                                        [--language en]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402

ANCHOR_EVERY_SEC = 60


def video_id(url_or_id):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})", url_or_id)
    return m.group(1) if m else url_or_id


def mmss(seconds):
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def fetch_info(raw_dir, vid, url):
    info_path = raw_dir / f"{vid}.info.json"
    if info_path.exists():
        return json.loads(info_path.read_text(encoding="utf-8"))
    raw_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["yt-dlp", "--skip-download", "--write-info-json",
         "-o", str(raw_dir / "%(id)s.%(ext)s"), url],
        check=True,
    )
    return json.loads(info_path.read_text(encoding="utf-8"))


def fetch_audio(raw_dir, vid, url):
    audio_path = raw_dir / f"{vid}.audio.mp3"
    if audio_path.exists():
        return audio_path
    subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "5",
         "-o", str(raw_dir / f"{vid}.audio.%(ext)s"), url],
        check=True,
    )
    if not audio_path.exists():
        sys.exit(f"Expected {audio_path} after yt-dlp audio extraction, not found.")
    return audio_path


def transcribe(audio_path, model_name, device, language):
    import whisper

    print(f"Loading whisper model '{model_name}' (device={device})...", file=sys.stderr)
    model = whisper.load_model(model_name, device=device)
    print(f"Transcribing {audio_path.name} — this can take a while for a long file...",
          file=sys.stderr)
    result = model.transcribe(str(audio_path), language=language, verbose=False)
    return result["segments"]


def build_body(segments):
    """Group whisper segments into ~60s paragraphs with a leading [mm:ss] anchor,
    the same windowing normalize.py uses for YouTube captions."""
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
            anchor = f"[{mmss(start)}]"
            next_anchor = start + ANCHOR_EVERY_SEC
        current.append(text)

    if current:
        paragraphs.append(f"{anchor} {' '.join(current)}")

    return "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in paragraphs)


def fmt_date(raw):
    if raw and len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return "not available"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("url", help="YouTube URL or 11-char video id")
    ap.add_argument("--model", default="turbo",
                     help="whisper model: tiny/base/small/medium/large-v3/turbo (default: turbo)")
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps"],
                     help="mps is faster on Apple Silicon but less reliable; cpu is the safe default")
    ap.add_argument("--language", default="en")
    args = ap.parse_args()

    lib = load_library(args.slug)
    vid = video_id(args.url)
    url = args.url if args.url.startswith("http") else f"https://www.youtube.com/watch?v={vid}"

    info = fetch_info(lib.raw_dir, vid, url)
    title = info.get("title") or "not available"
    duration = info.get("duration")
    dur_str = mmss(duration) if duration else "not available"
    date = fmt_date(info.get("upload_date"))

    audio_path = fetch_audio(lib.raw_dir, vid, url)
    segments = transcribe(audio_path, args.model, args.device, args.language)
    body = build_body(segments)
    if not body.strip():
        sys.exit("Whisper produced an empty transcript — nothing to write.")

    header = (
        f"TITLE: {title}\n"
        f"VIDEO ID: {vid}\n"
        f"URL: {url}\n"
        f"UPLOAD DATE: {date}\n"
        f"DURATION: {dur_str}\n"
        f"CAPTION TRACK: whisper-local ({args.model})\n"
        f"{'=' * 70}\n\n"
    )

    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{vid}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    manifest = lib.load_manifest()
    sources = [s for s in manifest.get("sources", []) if s["id"] != vid]
    sources.append({
        "id": vid,
        "kind": "youtube",
        "title": title,
        "url": url,
        "upload_date": date,
        "duration_seconds": duration,
        "duration": dur_str,
        "word_count": len(body.split()),
        "clean_file": f"clean/{vid}.txt",
        "transcript_source": f"whisper-local:{args.model}",
        "anchor": {
            "kind": "timestamp", "format": "mm:ss",
            "bound_field": "duration_seconds", "bound": duration,
        },
    })
    sources.sort(key=lambda r: r["title"].lower())
    # This id may still be listed in skipped (from normalize.py's earlier
    # "no captions" run) — that's harmless, the source catalog build only
    # reads `sources`, but strip it for a clean manifest.
    skipped = [s for s in manifest.get("skipped", []) if s.get("id") != vid]
    lib.save_manifest({**manifest, "sources": sources, "skipped": skipped})

    print(f"Wrote {clean_path}")
    print(f"  {len(body.split())} words, {len(segments)} whisper segments, id: {vid}")
    print(f"  Write libraries/{args.slug}/notes/{vid}.md, then:")
    print(f"  python3 scripts/check_notes.py {args.slug} {vid}")


if __name__ == "__main__":
    main()
