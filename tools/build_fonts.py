# -*- coding: utf-8 -*-
"""
Subset and convert the webfonts to self-hosted WOFF2.

    python tools/build_fonts.py

Loading these from fonts.googleapis.com cost a third-party DNS lookup, TLS
handshake and a render-blocking stylesheet before the browser even discovered
the font files. On mobile that was a large part of a 4.0s First Contentful
Paint. Self-hosting on the same origin removes the whole chain, and Cloudflare
serves them from the edge next to the HTML.

Latin subset only. Variable fonts cover their whole weight range in one file.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".fonts")
DST = os.path.join(ROOT, "assets", "fonts")

# Latin + Latin-1 punctuation, plus the few symbols the UI actually renders.
UNICODES = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC," \
           "U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191," \
           "U+2193,U+2212,U+2215,U+2713,U+2715,U+FEFF,U+FFFD"

# Variable sources keep their full weight axis: fontTools.subset preserves
# variations automatically, and clamping the range needs a separate
# varLib.instancer pass that is not worth the extra kilobytes it would save.
JOBS = [
    ("Poppins-Medium.ttf", "poppins-500.woff2"),
    ("Poppins-SemiBold.ttf", "poppins-600.woff2"),
    ("Poppins-Bold.ttf", "poppins-700.woff2"),
    ("Inter-Variable.ttf", "inter-var.woff2"),
    ("JetBrainsMono-Variable.ttf", "jetbrains-var.woff2"),
]


def run(job):
    src, out = job
    src_path = os.path.join(SRC, src)
    if not os.path.exists(src_path):
        print(f"  SKIP {src} (not found)")
        return None

    cmd = [sys.executable, "-m", "fontTools.subset", src_path,
           f"--unicodes={UNICODES}",
           "--layout-features=kern,liga,calt,ccmp",
           "--flavor=woff2",
           "--no-hinting",
           "--desubroutinize",
           f"--output-file={os.path.join(DST, out)}"]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FAIL {out}: {r.stderr.strip().splitlines()[-1] if r.stderr else 'unknown'}")
        return None

    before = os.path.getsize(src_path) / 1024
    after = os.path.getsize(os.path.join(DST, out)) / 1024
    print(f"  {out:<24} {before:6.0f} KB -> {after:5.1f} KB  ({100 - after / before * 100:.0f}% smaller)")
    return after


def main():
    os.makedirs(DST, exist_ok=True)
    total = 0
    for job in JOBS:
        got = run(job)
        if got:
            total += got
    print(f"\n  total self-hosted font payload: {total:.1f} KB")


if __name__ == "__main__":
    main()
