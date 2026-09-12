#!/usr/bin/env python3
"""Ingest an Instagram recipe reel: download via instaloader, register the
post's own caption (and optionally its comments) as a paragraph-anchored
source, and pull still images for the note page.

Unlike the YouTube pipeline (scripts/add.sh), there is no caption track to
fetch — for most creators the recipe itself lives in the post's caption, not
in spoken narration, so the primary "transcript" here is the caption text,
paragraph-anchored exactly like scripts/add_website.py anchors an article.
Comments require a logged-in session (confirmed live: an anonymous fetch
raises instaloader.exceptions.LoginRequiredException) and are fetched only
when --login is given, reusing a session saved once via the one-time setup
below — never a fresh login per run.

One-time setup (once per machine, not per video):
    pip3 install instaloader
    instaloader --login <your-instagram-username>
        # prompts for your password once, saves a session file under
        # ~/.config/instaloader/ that this script reuses via --login

Usage:
  python3 scripts/add_instagram_reel.py <slug> <url-or-shortcode> \
      [--id ID] [--title T] [--login USERNAME] [--comment-limit N] \
      [--onscreen-file PATH] [--frame-pct "8,95"]

  # Fallback, when instaloader can't reach a post at all (private/deleted):
  python3 scripts/add_instagram_reel.py <slug> --video-file PATH --caption-file PATH \
      --url URL --title T --author HANDLE [--id ID] [--onscreen-file PATH]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402

SHORTCODE_RE = re.compile(r"instagram\.com/(?:reel|reels|p)/([A-Za-z0-9_-]+)")


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "recipe"


def extract_shortcode(url_or_code):
    m = SHORTCODE_RE.search(url_or_code)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{5,}", url_or_code):
        return url_or_code
    sys.exit(f"Could not find an Instagram shortcode in: {url_or_code}")


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def timestamp(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def caption_paragraphs(caption):
    """Split on blank lines (same convention as add_website.py), but keep
    internal single-newlines within a block intact — most recipe captions
    format an ingredient list one-per-line with no blank line between them,
    and collapsing that to a run-on sentence would make the clean file
    needlessly hard for a human to read while writing the note."""
    if not caption:
        return []
    blocks = re.split(r"\n\s*\n", caption.strip())
    return [re.sub(r"[ \t]+", " ", b).strip() for b in blocks if b.strip()]


def fetch_comments(post, limit):
    from instaloader.exceptions import LoginRequiredException
    try:
        out = []
        for i, c in enumerate(post.get_comments()):
            if i >= limit:
                break
            text = re.sub(r"\s+", " ", c.text).strip()
            if text:
                out.append((c.owner.username, text))
        return out
    except LoginRequiredException:
        sys.exit(
            "Comments need a logged-in session. Run the one-time setup once:\n"
            "  instaloader --login <your-instagram-username>\n"
            "then pass --login <that-username> to this script."
        )


def extract_frames(video_path, out_dir, pct_points):
    duration = ffprobe_duration(video_path)
    paths = []
    for i, pct in enumerate(pct_points, start=1):
        seek = max(0.0, duration * pct / 100.0)
        out_path = out_dir / f"{i:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{seek:.2f}", "-i", str(video_path),
             "-vf", "scale=480:-1", "-frames:v", "1", "-q:v", "4", str(out_path)],
            check=True, capture_output=True,
        )
        paths.append(out_path)
    return paths, duration


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("url", nargs="?", help="Instagram reel URL or bare shortcode")
    ap.add_argument("--id")
    ap.add_argument("--title")
    ap.add_argument("--login", help="Instagram username with a saved instaloader session, "
                                     "used only to fetch comments as a fallback")
    ap.add_argument("--comment-limit", type=int, default=15)
    ap.add_argument("--onscreen-file", type=Path,
                     help="Paul's own [mm:ss]-anchored notes on spoken/on-screen content, "
                          "registered as a second, timestamp-anchored source: <id>-video")
    ap.add_argument("--frame-pct", default="8,95",
                     help="comma-separated percentages into the video to extract stills at "
                          "(default: an early frame and a late/final-shot frame)")
    # Manual fallback, for a post instaloader can't reach at all.
    ap.add_argument("--video-file", type=Path)
    ap.add_argument("--caption-file", type=Path)
    ap.add_argument("--author")
    ap.add_argument("--manual-url", dest="manual_url")
    args = ap.parse_args()

    lib = load_library(args.slug)
    frame_pcts = [float(p) for p in args.frame_pct.split(",") if p.strip()]

    manual_mode = bool(args.caption_file)
    if manual_mode:
        if not args.video_file or not args.title or not args.manual_url:
            sys.exit("Manual mode needs --video-file, --title, and --url together with --caption-file.")
        video_path = args.video_file
        caption = args.caption_file.read_text(encoding="utf-8")
        title = args.title
        author = args.author
        post_url = args.manual_url
        upload_date = None
        source_id = args.id or slugify(f"{author or 'creator'}-{title}")
        comments = []
        cover_path = None
    else:
        if not args.url:
            sys.exit("Give an Instagram URL/shortcode, or use --caption-file for manual mode.")
        import instaloader
        shortcode = extract_shortcode(args.url)
        L = instaloader.Instaloader(dirname_pattern=str(lib.raw_dir / "{target}"),
                                     save_metadata=False, download_comments=False,
                                     post_metadata_txt_pattern="")
        if args.login:
            L.load_session_from_file(args.login)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        author = post.owner_username
        title = args.title or (post.caption or "").splitlines()[0][:80] or shortcode
        source_id = args.id or slugify(f"{author}-{title}")
        upload_date = post.date_utc.date().isoformat()
        post_url = f"https://www.instagram.com/reel/{shortcode}/"

        target_dir = lib.raw_dir / source_id
        target_dir.mkdir(parents=True, exist_ok=True)
        L.download_post(post, target=source_id)

        vids = sorted(target_dir.glob("*.mp4"))
        if not post.is_video or not vids:
            print("warning: this post has no video — proceeding with caption/images only.",
                  file=sys.stderr)
            video_path = None
        else:
            video_path = vids[0]
        jpgs = sorted(target_dir.glob("*.jpg"))
        cover_path = jpgs[0] if jpgs else None

        caption = post.caption or ""
        comments = fetch_comments(post, args.comment_limit) if args.login else []

    # --- caption source (primary, paragraph-anchored) ----------------------
    paras = caption_paragraphs(caption)
    for owner, text in comments:
        paras.append(f"COMMENT by {owner}: {text}")

    if not paras:
        sys.exit("No caption or comment text to write — nothing to register.")

    body = "\n\n".join(f"[¶{i}] {p}" for i, p in enumerate(paras, start=1))
    header = (
        f"TITLE: {title}\n"
        + (f"CREATOR: @{author}\n" if author else "")
        + f"INSTAGRAM URL: {post_url}\n"
        + (f"UPLOAD DATE: {upload_date}\n" if upload_date else "")
        + f"PARAGRAPH COUNT: {len(paras)}\n"
        + "CAPTION TRACK: instagram-caption"
        + (f" + {len(comments)} comment(s)" if comments else "")
        + "\n" + "=" * 70 + "\n\n"
    )
    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{source_id}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    manifest = lib.load_manifest()
    sources = [s for s in manifest.get("sources", []) if s["id"] not in (source_id, f"{source_id}-video")]
    sources.append({
        "id": source_id,
        "kind": "instagram_caption",
        "title": title,
        "url": post_url,
        "author": author,
        "upload_date": upload_date,
        "word_count": len(body.split()),
        "clean_file": f"clean/{source_id}.txt",
        "anchor": {"kind": "paragraph", "format": "¶N", "bound_field": "paragraph_count",
                   "bound": len(paras)},
    })

    # --- images: cover thumbnail + extracted frames -------------------------
    images_dir = lib.sources_dir / "images" / source_id
    image_paths = []
    if cover_path or (video_path and frame_pcts):
        images_dir.mkdir(parents=True, exist_ok=True)
        if cover_path:
            cover_out = images_dir / "00.jpg"
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(cover_path), "-vf", "scale=480:-1",
                 "-q:v", "4", str(cover_out)],
                check=True, capture_output=True,
            )
            image_paths.append(cover_out)
        duration = None
        if video_path and frame_pcts:
            frames, duration = extract_frames(video_path, images_dir, frame_pcts)
            image_paths.extend(frames)
    else:
        duration = ffprobe_duration(video_path) if video_path else None

    # --- optional on-screen/narration source (secondary, timestamp-anchored) -
    if args.onscreen_file:
        if duration is None and video_path:
            duration = ffprobe_duration(video_path)
        onscreen_body = args.onscreen_file.read_text(encoding="utf-8").strip()
        onscreen_header = (
            f"TITLE: {title} (on-screen/narration notes)\n"
            f"INSTAGRAM URL: {post_url}\n"
            + (f"DURATION: {timestamp(duration)}\n" if duration else "")
            + "CAPTION TRACK: manual-hand-timed\n"
            + "=" * 70 + "\n\n"
        )
        video_source_id = f"{source_id}-video"
        onscreen_path = lib.clean_dir / f"{video_source_id}.txt"
        onscreen_path.write_text(onscreen_header + onscreen_body + "\n", encoding="utf-8")
        sources.append({
            "id": video_source_id,
            "kind": "instagram_reel",
            "title": f"{title} (video)",
            "url": post_url,
            "author": author,
            "duration_seconds": duration,
            "duration": timestamp(duration) if duration else None,
            "word_count": len(onscreen_body.split()),
            "clean_file": f"clean/{video_source_id}.txt",
            "anchor": {"kind": "timestamp", "format": "mm:ss",
                       "bound_field": "duration_seconds", "bound": duration},
        })

    sources.sort(key=lambda s: s["title"].lower())
    lib.save_manifest({**manifest, "sources": sources})

    print(f"Wrote {clean_path}  ({len(paras)} paragraphs, {len(body.split())} words)")
    if image_paths:
        print(f"Wrote {len(image_paths)} image(s) under {images_dir}")
        rel = [str(p.relative_to(lib.sources_dir)) for p in image_paths]
        print("Frontmatter snippet:")
        print("images:")
        for r in rel:
            print(f"  - {r}")
    if args.onscreen_file:
        print(f"Wrote {onscreen_path} — cite with `{source_id}-video`[mm:ss]")
    print(f"\nNow write libraries/{args.slug}/notes/{source_id}.md, then:")
    print(f"  python3 scripts/check_notes.py {args.slug} {source_id}")


if __name__ == "__main__":
    main()
