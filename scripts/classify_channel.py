#!/usr/bin/env python3
"""Split the full channel listing into health/human-body videos and the rest.

The channel has two eras: a newer restorative-health/physiology run, and an older
physics-and-metaphysics run. The boundary is not a clean date cut -- physics videos
appear inside the later range and physiology videos appear inside the earlier one --
so classification is by subject, not position.

Rule applied: INCLUDE anything whose subject is human physiology, anatomy, ageing,
sensory systems, or embodied psychology. EXCLUDE pure physics, cosmology, metaphysics,
philosophy of identity, and post-mortem/decomposition topics, which carry nothing a
restorative-health guide can act on.

Borderline cases are included, not dropped -- subtitles are cheap and the brief was
"every video that pertains to health and the human body".
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Excluded by video id, with the reason recorded so 00_README can report it honestly.
EXCLUDE = {
    # --- physics, cosmology, quantum ---
    "HdSzogi-x3w": "physics — electrical conduction",
    "q_J8LrPOjoY": "physics — properties of water",
    "Fm5dlA2MMbY": "physics — nuclear blast",
    "fdFsDiQFTFs": "physics — combustion",
    "hHTVbWELwqY": "physics — atomic structure",
    "GviiD1a4bbM": "physics — zero-point vibration",
    "MEDNsDnQUZM": "physics — general relativity",
    "sP_6mtYPcVY": "physics — arrow of time",
    "T7QkjKjVfcc": "physics — geomagnetism",
    "IrsNj9rADqA": "physics — interstellar travel",
    "nK8wsFFuEaY": "physics — magnetism",
    "DFAaQcTZUsg": "physics — geomagnetism",
    "NAFhLOuL3Qs": "physics — black holes",
    "DTkdiVJ7ap0": "physics — stellar fusion",
    "RJImwcmyLk8": "physics — quantum entanglement",
    "KEIVgsgbDIw": "physics — speed of light",
    "Me-iusRI7bM": "physics — origin of mass",
    "lkKacsNy17w": "physics — optics",
    "hCfY71UAsnk": "physics — magnetism",
    "tULEZUsK9vE": "physics — gravity",
    "lKuFLqComqg": "physics — speed of light",
    "_8QWXUdOb-k": "physics — nuclear energy",
    "iNPKfzj1nvI": "physics — QED / time travel",
    "bCxddWwf1vM": "physics — nature of time",
    "XlP7Xihx2F8": "physics — geomagnetism",
    "tPfw6iBk3J0": "physics — gravitational waves",
    "5fVEpT-Gphw": "physics — atmospheric scattering",
    "rOgdevbhEMk": "physics — vacuum",
    "ppMhVzoMkls": "physics — magnetism",
    "lsXWDBoUiwQ": "physics — nature of time",
    "2On4u6pNnaU": "botany — tree biology",
    "EvBgcC5Ps_g": "quantum biology, not human physiology",
    "93RkAyNoz9A": "quantum theories of consciousness",
    # --- metaphysics, philosophy of mind and identity ---
    "OCOdeRfhYUE": "metaphysics — relativity and death",
    "9e9APoYO2MU": "metaphysics — why anything exists",
    "7rDQAHs1paM": "metaphysics — improbability of existence",
    "7EgV7ms7xTU": "metaphysics — memory after death",
    "VwRgijBm6kk": "metaphysics — energy after death",
    "dAEsOqnMsyc": "metaphysics — personal identity",
    "EKXCuqE2QRk": "metaphysics — consciousness after death",
    "GYHJYZgnW3U": "metaphysics — cognition without a brain",
    "P6xIOcV1siw": "metaphysics — death",
    "ZbbNPpfRbrk": "metaphysics — matter and identity",
    "VS4TD9BcVKo": "metaphysics — dreams and reality",
    "NUzrRI_V3lU": "philosophy — free will",
    "liSEa7clRlg": "philosophy — machine cognition",
    "zMgHxkfScqQ": "philosophy — nature of thought",
    "EfZ7pc0Eci8": "cosmology — symmetry breaking",
    "aq0LESwp3sc": "physics — foundations of quantum mechanics",
    "N0J1g_P-4Oc": "metaphysics — nature of reality",
    "7Id25KkupFo": "biographical",
    # --- post-mortem / decomposition: human body, but nothing a health guide can act on ---
    "0w7xf-HSG6o": "post-mortem decomposition",
    "EJkFixZIlsw": "post-mortem decomposition",
    "3b1Tj0SbPYI": "post-mortem — cremation vs burial",
    "xKz0XJw79R8": "post-mortem — cremation and DNA",
    "z8O6eIOOfEo": "post-mortem — cremation",
}


def main():
    rows = []
    for line in (ROOT / "scripts" / "channel_full.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        p = line.split("\\t")
        rows.append({"id": p[0], "dur": float(p[2]), "title": "\\t".join(p[3:]).strip()})

    inc = [r for r in rows if r["id"] not in EXCLUDE]
    exc = [r for r in rows if r["id"] in EXCLUDE]

    out = ROOT / "scripts" / "video_ids_full.txt"
    out.write_text(
        "# Every video on @The_Feynman_Way pertaining to health and the human body.\n"
        f"# {len(inc)} of {len(rows)} channel videos. {len(exc)} excluded (see excluded_videos.tsv).\n"
        + "".join(f"https://www.youtube.com/watch?v={r['id']}\n" for r in inc),
        encoding="utf-8",
    )
    (ROOT / "scripts" / "excluded_videos.tsv").write_text(
        "id\treason\ttitle\n"
        + "".join(f"{r['id']}\t{EXCLUDE[r['id']]}\t{r['title']}\n" for r in exc),
        encoding="utf-8",
    )

    hrs = sum(r["dur"] for r in inc) / 3600
    print(f"included : {len(inc)}  (~{hrs:.0f} h, ~{hrs*60*150/1000:.0f}k words of transcript)")
    print(f"excluded : {len(exc)}")
    missing = set(EXCLUDE) - {r["id"] for r in rows}
    if missing:
        print("WARNING — exclude ids not found in listing:", missing)


if __name__ == "__main__":
    main()
