#!/usr/bin/env python3
"""Ingest a PDF into a library: page-anchored text extraction.

Extracts each page's text (pypdf first; falls back to OCR via pytesseract +
pdf2image for any page that yields near-zero text, e.g. a scanned page),
writes a [p.N]-anchored clean text file exactly like a video transcript's
[mm:ss] anchors, and appends a manifest entry with a "page" anchor kind.

Text only — no PDF viewer, no page-image rendering. The note-writing and
check_notes.py validation flow is identical to a video's afterward.

Usage:
  python3 scripts/add_pdf.py <slug> <path.pdf> [--id ID] [--title T]
                              [--author A] [--url U]
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402


def ocr_page(pdf_path, index):
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        print(f"  page {index + 1}: looks scanned but OCR dependencies "
              f"(pdf2image, pytesseract) aren't installed — left blank", file=sys.stderr)
        return None
    images = convert_from_path(str(pdf_path), first_page=index + 1, last_page=index + 1)
    if not images:
        return None
    return pytesseract.image_to_string(images[0]).strip()


def extract_pages(pdf_path):
    """Yield each page's text — pypdf first, OCR fallback for near-empty pages."""
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    for i, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if len(text) < 20:
            ocr_text = ocr_page(pdf_path, i)
            if ocr_text:
                text = ocr_text
        yield re.sub(r"[ \t]+", " ", text).strip()


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "source"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slug")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--id")
    ap.add_argument("--title")
    ap.add_argument("--author")
    ap.add_argument("--url")
    ap.add_argument("--evidence-type", help="e.g. guideline, systematic_review, rct, expert_commentary "
                                             "(must be in the library's declared evidence_types)")
    ap.add_argument("--evidence-level", help="high | moderate | low | anecdotal")
    ap.add_argument("--year", type=int)
    args = ap.parse_args()

    lib = load_library(args.slug)
    if not args.pdf.exists():
        sys.exit(f"No such file: {args.pdf}")

    source_id = args.id or slugify(args.pdf.stem)
    title = args.title or args.pdf.stem
    retrieved = datetime.date.today().isoformat()

    pages = list(extract_pages(args.pdf))
    if not any(pages):
        sys.exit("No text could be extracted from any page (even with OCR fallback).")

    body = "\n\n".join(f"[p.{i}] {text}" for i, text in enumerate(pages, start=1) if text)

    header = (
        f"TITLE: {title}\n"
        + (f"AUTHOR: {args.author}\n" if args.author else "")
        + (f"SOURCE URL: {args.url}\n" if args.url else "")
        + f"RETRIEVED: {retrieved}\n"
        + f"PAGE COUNT: {len(pages)}\n"
        + "=" * 70 + "\n\n"
    )

    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{source_id}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    entry = {
        "id": source_id,
        "kind": "pdf",
        "title": title,
        "author": args.author,
        "url": args.url,
        "retrieved_date": retrieved,
        "clean_file": f"clean/{source_id}.txt",
        "word_count": len(body.split()),
        "anchor": {"kind": "page", "format": "p.N", "bound_field": "page_count", "bound": len(pages)},
    }
    if args.evidence_type or args.evidence_level:
        evidence = {}
        if args.evidence_type:
            evidence["type"] = args.evidence_type
        if args.evidence_level:
            evidence["level"] = args.evidence_level
        if args.year:
            evidence["year"] = args.year
        entry["evidence"] = evidence

    manifest = lib.load_manifest()
    sources = [s for s in manifest.get("sources", []) if s["id"] != source_id]
    sources.append(entry)
    sources.sort(key=lambda s: s["title"].lower())
    lib.save_manifest({**manifest, "sources": sources})

    print(f"Wrote {clean_path}")
    print(f"  {len(pages)} pages, {len(body.split())} words, id: {source_id}")
    print(f"  Write libraries/{args.slug}/notes/{source_id}.md, then:")
    print(f"  python3 scripts/check_notes.py {args.slug} {source_id}")


if __name__ == "__main__":
    main()
