#!/usr/bin/env python3
"""
Detect dropouts in the source caption tracks.

YouTube auto-captions occasionally stop for a stretch and resume later. The text
either side of such a gap can read as one continuous (but garbled) sentence, so
gaps must be found from the timestamps rather than the prose. Anything reported
here is missing from the source and must never be filled in by inference.

Writes source_transcripts/caption_gaps.json and prints a summary.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "source_transcripts" / "raw"
OUT = ROOT / "source_transcripts" / "caption_gaps.json"

GAP_THRESHOLD_SEC = 45


def mmss(s):
    return f"{int(s) // 60:02d}:{int(s) % 60:02d}"


def caption_path(vid):
    for suffix in (".en-orig.json3", ".en.json3"):
        p = RAW / f"{vid}{suffix}"
        if p.exists():
            return p
    return None


def main():
    manifest = json.loads((ROOT / "source_transcripts" / "manifest.json").read_text())
    report = {}

    for v in manifest["videos"]:
        vid = v["id"]
        cap = caption_path(vid)
        if cap is None:
            continue
        data = json.loads(cap.read_text(encoding="utf-8"))

        times = []
        for ev in data.get("events", []):
            if ev.get("aAppend") or not ev.get("segs"):
                continue
            text = "".join(s.get("utf8", "") for s in ev["segs"]).strip()
            if text:
                times.append((ev.get("tStartMs", 0) / 1000.0,
                              ev.get("dDurationMs", 0) / 1000.0))
        if not times:
            continue

        gaps = []
        for (t1, d1), (t2, _) in zip(times, times[1:]):
            silence = t2 - (t1 + d1)
            if silence >= GAP_THRESHOLD_SEC:
                gaps.append({
                    "from": mmss(t1 + d1),
                    "to": mmss(t2),
                    "seconds": round(silence),
                })

        duration = v.get("duration_seconds") or 0
        tail = duration - (times[-1][0] + times[-1][1]) if duration else 0
        if tail >= GAP_THRESHOLD_SEC:
            gaps.append({
                "from": mmss(times[-1][0] + times[-1][1]),
                "to": mmss(duration),
                "seconds": round(tail),
                "note": "trailing",
            })

        if gaps:
            report[vid] = {
                "title": v["title"],
                "duration": v["duration"],
                "gaps": gaps,
                "total_missing_seconds": sum(g["seconds"] for g in gaps),
            }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if not report:
        print("No caption gaps found above threshold.")
    else:
        print(f"Videos with caption dropouts (>= {GAP_THRESHOLD_SEC}s): {len(report)}\n")
        for vid, r in sorted(report.items(),
                             key=lambda kv: -kv[1]["total_missing_seconds"]):
            mins = r["total_missing_seconds"] / 60
            print(f"{vid}  {mins:5.1f} min missing  {r['title'][:58]}")
            for g in r["gaps"]:
                tag = " (trailing)" if g.get("note") else ""
                print(f"      {g['from']} -> {g['to']}  ({g['seconds']}s){tag}")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
