#!/usr/bin/env python3
"""Ingest an EPUB into a library: paragraph-anchored text extraction.

An EPUB has no fixed pagination (reflowable by design), so unlike add_pdf.py's
[p.N] page anchors, this uses the same continuous [¶N] paragraph anchor
add_website.py already uses for an article — same anchor kind, so
check_notes.py needs no changes to validate either one.

Reads the EPUB's own manifest/spine (META-INF/container.xml -> the OPF file)
to walk every content document in the book's actual reading order, extracts
block-level text (headings, paragraphs, list items), and numbers paragraphs
continuously across the whole book into one clean text file — exactly like a
video transcript's [mm:ss] anchors or a PDF's [p.N] anchors, just paragraph
numbered instead of page/time numbered.

Usage:
  python3 scripts/add_epub.py <slug> <path.epub> [--id ID] [--title T]
                               [--author A] [--evidence-type ...] [--evidence-level ...]
"""
import argparse
import datetime
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402

NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
}
BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote"}


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "source"


def opf_path(zf):
    container = ET.fromstring(zf.read("META-INF/container.xml"))
    rootfile = container.find(".//container:rootfile", NS)
    if rootfile is None:
        sys.exit("Malformed EPUB: META-INF/container.xml has no <rootfile>.")
    return rootfile.get("full-path")


def spine_documents(zf, opf_file):
    opf_dir = "/".join(opf_file.split("/")[:-1])
    root = ET.fromstring(zf.read(opf_file))

    manifest = {}
    for item in root.findall(".//opf:manifest/opf:item", NS):
        manifest[item.get("id")] = item.get("href")

    metadata = root.find(".//opf:metadata", NS)
    title = author = None
    if metadata is not None:
        t = metadata.find("dc:title", NS)
        a = metadata.find("dc:creator", NS)
        title = t.text.strip() if t is not None and t.text else None
        author = a.text.strip() if a is not None and a.text else None

    def resolve(href):
        return f"{opf_dir}/{href}" if opf_dir else href

    docs = []
    for itemref in root.findall(".//opf:spine/opf:itemref", NS):
        idref = itemref.get("idref")
        href = manifest.get(idref)
        if href:
            docs.append(resolve(href))
    return docs, title, author


def extract_paragraphs(xhtml_bytes):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(xhtml_bytes, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    paras = []
    for el in soup.find_all(BLOCK_TAGS):
        # Skip a block whose text is fully contained in a block already
        # nested inside it (e.g. an <li> wrapping a <p> would otherwise
        # yield the same text twice).
        if el.find(BLOCK_TAGS):
            continue
        text = re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()
        if text:
            paras.append(text)
    return paras


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("epub", type=Path)
    ap.add_argument("--id")
    ap.add_argument("--title")
    ap.add_argument("--author")
    ap.add_argument("--evidence-type", help="e.g. textbook, expert_commentary, patient_experience")
    ap.add_argument("--evidence-level", help="high | moderate | low | anecdotal")
    ap.add_argument("--year", type=int)
    args = ap.parse_args()

    lib = load_library(args.slug)
    if not args.epub.exists():
        sys.exit(f"No such file: {args.epub}")

    with zipfile.ZipFile(args.epub) as zf:
        opf_file = opf_path(zf)
        docs, epub_title, epub_author = spine_documents(zf, opf_file)
        if not docs:
            sys.exit("No spine documents found — malformed or DRM-protected EPUB?")

        all_paras = []
        for doc in docs:
            try:
                raw = zf.read(doc)
            except KeyError:
                print(f"  warning: spine references missing file {doc}", file=sys.stderr)
                continue
            all_paras.extend(extract_paragraphs(raw))

    if not all_paras:
        sys.exit("No text could be extracted from any spine document.")

    title = args.title or epub_title or args.epub.stem
    author = args.author or epub_author
    source_id = args.id or slugify(title)
    retrieved = datetime.date.today().isoformat()

    body = "\n\n".join(f"[¶{i}] {p}" for i, p in enumerate(all_paras, start=1))
    header = (
        f"TITLE: {title}\n"
        + (f"AUTHOR: {author}\n" if author else "")
        + f"SOURCE FILE: {args.epub.name}\n"
        + f"RETRIEVED: {retrieved}\n"
        + f"PARAGRAPH COUNT: {len(all_paras)}\n"
        + "=" * 70 + "\n\n"
    )

    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{source_id}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    entry = {
        "id": source_id,
        "kind": "epub",
        "title": title,
        "author": author,
        "clean_file": f"clean/{source_id}.txt",
        "word_count": len(body.split()),
        "retrieved_date": retrieved,
        "anchor": {"kind": "paragraph", "format": "¶N", "bound_field": "paragraph_count",
                   "bound": len(all_paras)},
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
    print(f"  {len(all_paras)} paragraphs, {len(body.split())} words, id: {source_id}")
    print(f"  Write libraries/{args.slug}/notes/{source_id}.md, then:")
    print(f"  python3 scripts/check_notes.py {args.slug} {source_id}")


if __name__ == "__main__":
    main()
