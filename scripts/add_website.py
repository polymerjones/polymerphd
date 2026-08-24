#!/usr/bin/env python3
"""Ingest a web page into a library: paragraph-anchored text extraction.

Fetches the page ONCE at ingest time and saves a clean, paragraph-anchored
local copy — a [¶N]-anchored text file exactly like a video transcript's
[mm:ss] anchors or a PDF's [p.N] anchors. The app only ever renders this
local copy afterward, never the live URL, so browsing stays fully offline
and stable even if the source page later changes, paywalls, or disappears.
The URL is kept purely as an attribution/citation reference.

Same script handles an authoritative article and a patient-experience thread
(e.g. a forum post) alike — the distinction is an --evidence-type tag, not a
different code path.

Multiple URLs are treated as chapters of ONE source (e.g. a NICE guidance
page split across /chapter/1-Recommendations, /chapter/2-..., etc.) — fetched
in the order given, concatenated with paragraph numbering continuous across
all of them, one manifest entry, one clean text file. The first URL given is
kept as the entry's citation link.

Usage:
  python3 scripts/add_website.py <slug> <url> [<url2> ...] [--id ID] [--title T]
                                   [--author A] [--evidence-type ...] [--evidence-level ...]
"""
import argparse
import datetime
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import load_library  # noqa: E402


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "source"


def fetch(url):
    """Fetch with a real browser User-Agent — some sites (e.g. PubMed) block
    trafilatura's default fetcher but allow this."""
    import urllib.request
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
    except Exception as e:
        sys.exit(f"Could not fetch {url}: {e}")


def extract(html, url):
    import trafilatura
    text = trafilatura.extract(html, include_comments=False, include_tables=True,
                                output_format="txt", url=url, favor_recall=True)
    metadata = trafilatura.extract_metadata(html, default_url=url)
    return text, metadata


def paragraphs(text):
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


# PubMed's own page requires cookies and blocks scraping, but NCBI's free
# E-utilities API serves the same citation + abstract as clean text — used
# here instead of a generic HTML fetch for any pubmed.ncbi.nlm.nih.gov URL.
# First segment requires 4+ letters so short inline abbreviations used as
# comparison labels (e.g. "PNF versus LF: mean difference...") don't get
# mistaken for a section header; later segments (e.g. the "OF" in "LEVEL OF
# EVIDENCE:") only need 2+. A real match (not a lookahead) so re.finditer
# naturally gives leftmost-longest, non-overlapping spans — "CLINICAL
# QUESTION/LEVEL OF EVIDENCE:" comes back as one match, not four.
PUBMED_LABEL_RE = re.compile(r"[A-Z]{4,}(?:[ /][A-Z]{2,})*:")


def split_pubmed_abstract(abstract):
    matches = list(PUBMED_LABEL_RE.finditer(abstract))
    if not matches:
        return [abstract] if abstract else []
    parts = []
    if matches[0].start() > 0:
        parts.append(abstract[:matches[0].start()].strip())
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(abstract)
        parts.append(abstract[m.start():end].strip())
    return [p for p in parts if p]


def pubmed_pmid(url):
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
    return m.group(1) if m else None


def fetch_pubmed(pmid):
    api = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
           f"?db=pubmed&id={pmid}&rettype=abstract&retmode=text")
    return fetch(api)


def pubmed_paragraphs(text):
    """(title, author_line, [citable paragraphs]) from an efetch abstract-text block."""
    blocks = [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) < 2:
        return None, None, blocks
    citation, title = blocks[0], blocks[1]
    authors = blocks[2] if len(blocks) > 2 and not blocks[2].startswith("Author information") else None
    rest = blocks[3 if authors else 2:]
    abstract_parts, trailing = [], []
    for b in rest:
        if b.startswith("Author information") or b.startswith("Comment in") or b.startswith("Erratum in"):
            continue
        if b.startswith(("Copyright", "©", "DOI:", "PMID:", "PMCID:")):
            trailing.append(b)
        else:
            abstract_parts.append(b)
    abstract = " ".join(abstract_parts)
    sections = split_pubmed_abstract(abstract)
    paras = [citation, title] + ([authors] if authors else []) + (sections or [abstract]) + trailing
    return title, authors, [p for p in paras if p]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slug")
    ap.add_argument("urls", nargs="+", metavar="url")
    ap.add_argument("--id")
    ap.add_argument("--title")
    ap.add_argument("--author")
    ap.add_argument("--evidence-type", help="e.g. guideline, systematic_review, rct, "
                                             "expert_commentary, patient_experience")
    ap.add_argument("--evidence-level", help="high | moderate | low | anecdotal")
    ap.add_argument("--year", type=int)
    args = ap.parse_args()

    lib = load_library(args.slug)

    all_paras = []
    title = args.title
    author = args.author
    for i, url in enumerate(args.urls):
        pmid = pubmed_pmid(url)
        if pmid:
            raw = fetch_pubmed(pmid)
            pm_title, pm_author, paras = pubmed_paragraphs(raw)
            if i == 0:
                title = title or pm_title
                author = author or pm_author
            all_paras.extend(paras)
            continue

        html = fetch(url)
        text, metadata = extract(html, url)
        if not text or not text.strip():
            print(f"  warning: no text extracted from {url}", file=sys.stderr)
            continue
        if i == 0:
            title = title or (metadata.title if metadata and metadata.title else None) \
                or urlparse(url).netloc
            author = author or (metadata.author if metadata and metadata.author else None)
        all_paras.extend(paragraphs(text))

    if not all_paras:
        sys.exit("No article text could be extracted from any of the given pages.")

    source_id = args.id or slugify(title)
    retrieved = datetime.date.today().isoformat()

    body = "\n\n".join(f"[¶{i}] {p}" for i, p in enumerate(all_paras, start=1))
    header = (
        f"TITLE: {title}\n"
        + (f"AUTHOR: {author}\n" if author else "")
        + f"SOURCE URL: {args.urls[0]}\n"
        + (f"ADDITIONAL PAGES: {', '.join(args.urls[1:])}\n" if len(args.urls) > 1 else "")
        + f"RETRIEVED: {retrieved}\n"
        + f"PARAGRAPH COUNT: {len(all_paras)}\n"
        + "=" * 70 + "\n\n"
    )

    lib.clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = lib.clean_dir / f"{source_id}.txt"
    clean_path.write_text(header + body + "\n", encoding="utf-8")

    entry = {
        "id": source_id,
        "kind": "website",
        "title": title,
        "author": author,
        "url": args.urls[0],
        "retrieved_date": retrieved,
        "clean_file": f"clean/{source_id}.txt",
        "word_count": len(body.split()),
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
