#!/usr/bin/env python3
"""Copy only public website files into dist; adapt 404 paths for project Pages."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("--base", default="/", help="/ for custom domain; /hijikilabo-site/ for project Pages")
args = parser.parse_args()
if not args.base.startswith("/") or not args.base.endswith("/") or any(c not in "/-_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" for c in args.base) or ".." in args.base:
    parser.error("base must be an absolute URL path ending in / without traversal")
output = ROOT / "dist"
if output.exists():
    shutil.rmtree(output)
output.mkdir()
for name in ("index.html", "privacy.html", "404.html", "favicon.svg", ".nojekyll"):
    shutil.copy2(ROOT / name, output / name)
shutil.copytree(ROOT / "assets", output / "assets")
error = output / "404.html"
error.write_text(error.read_text().replace('href="/', f'href="{args.base}'))
print(f"Built {output} (base: {args.base}); no deployment performed.")
