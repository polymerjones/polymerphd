#!/usr/bin/env python3
"""Batch version of add_video_whisper.py: transcribe many videos with one
model load instead of one process per video.

Same output shape as add_video_whisper.py — a [mm:ss]-anchored clean text
file and a manifest entry per video, with transcript_source recorded as
"whisper-local:<model>" so normalize.py never clobbers it on a later re-run.

Resumable: skips any id that already has a clean text file. Safe to Ctrl-C
and re-run — each video's clean file + manifest entry is written before
moving to the next, so nothing is half-done on disk.

Usage:
  python3 scripts/add_videos_whisper.py <slug> ids.txt [--model turbo] [--device cpu]
  cat ids.txt | python3 scripts/add_videos_whisper.py <slug>
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402
from add_video_whisper import (  # noqa: E402
    video_id, mmss, fetch_info, fetch_audio, build_body, fmt_date,
)


def read_ids(path):
    text = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    ids = []
    seen = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vid = video_id(line)
        if vid not in seen:
            seen.add(vid)
            ids.append(vid)
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("ids_file", nargs="?", default=None,
                     help="file of YouTube ids/urls, one per line (default: stdin)")
    ap.add_argument("--model", default="turbo")
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps"])
    ap.add_argument("--language", default="en")
    args = ap.parse_args()

    lib = load_library(args.slug)
    ids = read_ids(args.ids_file)

    todo = [vid for vid in ids if not (lib.clean_dir / f"{vid}.txt").exists()]
    print(f"{len(ids)} ids given, {len(ids) - len(todo)} already have a clean file, "
          f"{len(todo)} to transcribe.", file=sys.stderr)
    if not todo:
        return

    import whisper
    print(f"Loading whisper model '{args.model}' (device={args.device})...", file=sys.stderr)
    model = whisper.load_model(args.model, device=args.device)

    ok, failed = 0, []
    t0 = time.time()
    for i, vid in enumerate(todo, 1):
        url = f"https://www.youtube.com/watch?v={vid}"
        elapsed = time.time() - t0
        eta = (elapsed / i) * (len(todo) - i) if i else 0
        print(f"[{i}/{len(todo)}] {vid}  (elapsed {elapsed/60:.0f}m, eta {eta/60:.0f}m)",
              file=sys.stderr)
        try:
            info = fetch_info(lib.raw_dir, vid, url)
            title = info.get("title") or "not available"
            duration = info.get("duration")
            dur_str = mmss(duration) if duration else "not available"
            date = fmt_date(info.get("upload_date"))

            audio_path = fetch_audio(lib.raw_dir, vid, url)
            result = model.transcribe(str(audio_path), language=args.language, verbose=False)
            body = build_body(result["segments"])
            audio_path.unlink(missing_ok=True)  # raw/ is gitignored + disk-heavy; keep info.json only

            if not body.strip():
                failed.append((vid, "empty transcript"))
                continue

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
            (lib.clean_dir / f"{vid}.txt").write_text(header + body + "\n", encoding="utf-8")

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
            skipped = [s for s in manifest.get("skipped", []) if s.get("id") != vid]
            lib.save_manifest({**manifest, "sources": sources, "skipped": skipped})
            ok += 1
        except Exception as e:  # noqa: BLE001 — one bad video must not kill the batch
            failed.append((vid, str(e)))
            print(f"  FAILED: {e}", file=sys.stderr)

    print(f"\ndone: {ok} transcribed, {len(failed)} failed, {time.time()-t0:.0f}s total",
          file=sys.stderr)
    if failed:
        print("failures:", file=sys.stderr)
        for vid, reason in failed:
            print(f"  {vid}: {reason}", file=sys.stderr)


if __name__ == "__main__":
    main()
