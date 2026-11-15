#!/usr/bin/env python3
"""Build static pages and the published-only WORKS list without runtime JavaScript."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
WORKS_MARKER = "<!-- WORKS_SECTION -->"
STATIC_FILES = ("privacy.html", "404.html", "favicon.svg", ".nojekyll")
STATIC_ASSETS = (
    "assets/css/style.css",
    "assets/og.png",
    "assets/hero-layers-03a.webp",
)


def load_published_works(root):
    """Ignore unpublished records before reading their remaining fields."""
    entries = json.loads((root / "data/works.json").read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("data/works.json must contain a JSON array")
    works = []
    seen = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"WORKS item {index} must be an object")
        if entry.get("status") != "published":
            continue
        work = {}
        for key in ("id", "name", "description", "icon", "published_at", "url"):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"WORKS item {index}: {key} must be a non-empty string")
            work[key] = value.strip()
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", work["id"]):
            raise ValueError(f"WORKS item {index}: id must be a lowercase ASCII slug")
        if work["id"] in seen:
            raise ValueError(f"WORKS item {index}: duplicate published id")
        seen.add(work["id"])
        platforms = entry.get("platforms")
        if not isinstance(platforms, list) or not platforms or any(
            not isinstance(platform, str) or not platform.strip() for platform in platforms
        ):
            raise ValueError(f"WORKS item {index}: platforms must be a non-empty string array")
        work["platforms"] = [platform.strip() for platform in platforms]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", work["published_at"]):
            raise ValueError(f"WORKS item {index}: published_at must be YYYY-MM-DD")
        work["date"] = date.fromisoformat(work["published_at"])
        destination = urlsplit(work["url"])
        if (
            destination.scheme != "https"
            or not destination.hostname
            or destination.username is not None
            or destination.password is not None
            or any(character.isspace() or ord(character) < 32 for character in work["url"])
        ):
            raise ValueError(f"WORKS item {index}: url must be an absolute HTTPS URL without credentials")
        icon = PurePosixPath(work["icon"])
        if (
            icon.is_absolute()
            or ".." in icon.parts
            or any(character in work["icon"] for character in "\\?#")
            or icon.parts[:2] != ("assets", "works")
            or icon.suffix.lower() not in (".png", ".webp", ".jpg", ".jpeg")
        ):
            raise ValueError(f"WORKS item {index}: icon must be a local raster image under assets/works/")
        source = root / icon
        if not source.resolve().is_relative_to(root.resolve() / "assets/works") or not source.is_file():
            raise ValueError(f"WORKS item {index}: icon file is missing or outside assets/works/")
        works.append(work)
    # Stable sort: entries with the same release date keep their JSON order.
    return sorted(works, key=lambda work: work["date"], reverse=True)


def render_works(works):
    if not works:
        return ""
    items = []
    for work in works:
        name = escape(work["name"])
        released = work["date"]
        label = "App Storeで見る" if urlsplit(work["url"]).hostname == "apps.apple.com" else "公式配信ページへ"
        items.append(f'''              <li>
                <article class="work-item" aria-labelledby="work-{work['id']}-title">
                  <img class="work-icon" src="{quote(work['icon'], safe='/-._~')}" width="64" height="64" alt="{name}のアイコン" loading="lazy" decoding="async" />
                  <div>
                    <h3 id="work-{work['id']}-title">{name}</h3>
                    <p class="work-meta"><span>{escape(' / '.join(work['platforms']))}</span><span>公開日：{released.year}年{released.month}月{released.day}日</span></p>
                    <p class="work-description">{escape(work['description'])}</p>
                    <a class="work-link" href="{escape(work['url'], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="{name}の配信ページ（新しいタブで開きます）">{label} <span aria-hidden="true">↗</span></a>
                  </div>
                </article>
              </li>''')
    return '''<section class="section wrap works" id="works" aria-labelledby="works-title">
        <div class="section-label"><p class="eyebrow">WORKS</p></div>
        <div class="section-body">
          <h2 id="works-title">つくったもの。</h2>
          <p class="section-intro">好きでつくった、あれこれ。</p>
          <ul class="works-list">
''' + "\n".join(items) + '''
          </ul>
        </div>
      </section>'''


def build_site(root=ROOT, base="/"):
    if (
        not base.startswith("/")
        or not base.endswith("/")
        or any(character not in "/-_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" for character in base)
        or ".." in base
    ):
        raise ValueError("base must be an absolute URL path ending in / without traversal")
    works = load_published_works(root)
    index = (root / "index.html").read_text(encoding="utf-8")
    if index.count(WORKS_MARKER) != 1:
        raise ValueError("index.html must have exactly one WORKS_SECTION marker")
    index = index.replace(WORKS_MARKER, render_works(works))
    output = root / "dist"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    (output / "index.html").write_text(index, encoding="utf-8")
    for name in STATIC_FILES + STATIC_ASSETS:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
    # Do not publish raw JSON, drafts, unused icons or other unreferenced assets.
    for work in works:
        target = output / work["icon"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / work["icon"], target)
    error = output / "404.html"
    error.write_text(error.read_text(encoding="utf-8").replace('href="/', f'href="{base}'), encoding="utf-8")
    return output, len(works)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="/", help="/ for custom domain; /hijikilabo-site/ for project Pages")
    args = parser.parse_args()
    try:
        output, count = build_site(base=args.base)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Build failed: {error}\n")
    print(f"Built {output} (base: {args.base}, published works: {count}); no deployment performed.")


if __name__ == "__main__":
    main()
