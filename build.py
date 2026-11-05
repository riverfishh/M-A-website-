#!/usr/bin/env python3
"""Inline every local font and image referenced by src/index.html into dist/index.html.

Usage:  python3 build.py
References must be written as  assets/<file>  or  fonts/<file>  (an optional ./ prefix is fine)
inside src="...", href="...", srcset="...", or url(...). The output is a single self-contained file.
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
SRC = SRC_DIR / "index.html"
OUT = ROOT / "dist" / "index.html"

MIME = {
    ".webp": "image/webp",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
}
REF = re.compile(r"(?<![\w/.-])(?:\./)?((?:assets|fonts)/[A-Za-z0-9._-]+\.(?:webp|png|jpe?g|svg|woff2))")

cache: dict[str, str] = {}


def data_uri(rel: str) -> str:
    if rel not in cache:
        path = SRC_DIR / rel
        if not path.exists():
            sys.exit(f"build failed: missing asset {rel}")
        mime = MIME[path.suffix.lower()]
        cache[rel] = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    return cache[rel]


html = SRC.read_text(encoding="utf-8")

# The icon sprite lives in its own file so the page source stays readable.
SPRITE = ROOT / "icons.svgsprite"
if "<!--ICONS-->" in html:
    html = html.replace("<!--ICONS-->", SPRITE.read_text(encoding="utf-8").strip(), 1)

out = REF.sub(lambda m: data_uri(m.group(1)), html)

# Anything still pointing at a relative file would break in the single-file build.
leftovers = re.findall(
    r"""(?:src|href|srcset)=["'](?!https?:|mailto:|tel:|#|data:)([^"']+)["']|url\(\s*["']?(?!data:|https?:|#)([^"')]+)""",
    out,
)
leftovers = [a or b for a, b in leftovers]
if leftovers:
    sys.exit("build failed: relative references remain: " + ", ".join(sorted(set(leftovers))))

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(out, encoding="utf-8")
print(f"inlined {len(cache)} files -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")
for rel in sorted(cache):
    print(f"  {rel:34s} {(SRC_DIR / rel).stat().st_size / 1024:6.0f} KB")
