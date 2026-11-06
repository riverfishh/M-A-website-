#!/usr/bin/env python3
"""Collect the posts saved by the CMS into the two files the website reads.

  content/events/*.json  ->  data/events.json
  content/news/*.json    ->  data/news.json

Runs on every deploy (see .github/workflows/static.yml). It never fails the deploy
because of one bad post: a post it cannot use is skipped with a warning.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
TIME = re.compile(r"^\d{1,2}:\d{2}$")

FIELDS = {
    "events": ["title", "category", "date", "start_time", "end_time", "location", "image", "speakers", "description"],
    "news": ["title", "category", "date", "image", "summary", "body"],
}


def warn(path, message):
    print(f"::warning file={path.relative_to(ROOT)}::{message}")


def text(value):
    return value.strip() if isinstance(value, str) else ""


def clean_image(value):
    value = text(value)
    if value.startswith("https://"):
        return value
    value = value.lstrip("/")
    return value if value.startswith("assets/") else ""


def build(kind):
    items = []
    for path in sorted((ROOT / "content" / kind).glob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as err:
            warn(path, f"skipped, not valid JSON ({err})")
            continue
        if not isinstance(raw, dict):
            warn(path, "skipped, expected a single post")
            continue
        if raw.get("draft") is True:
            continue
        title = text(raw.get("title"))
        date = text(raw.get("date"))
        if not title or not DATE.match(date):
            warn(path, "skipped, a title and a date are required")
            continue
        item = {"slug": re.sub(r"[^a-z0-9-]+", "-", path.stem.lower()).strip("-") or "post"}
        for field in FIELDS[kind]:
            item[field] = text(raw.get(field))
        item["date"] = date[:10]
        item["image"] = clean_image(raw.get("image"))
        for field in ("start_time", "end_time"):
            if item.get(field) and not TIME.match(item[field]):
                warn(path, f"{field} should look like 18:30, ignoring it")
                item[field] = ""
        items.append(item)
    items.sort(key=lambda i: (i["date"], i["title"]))
    out = ROOT / "data" / f"{kind}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{kind}: {len(items)} published")


if __name__ == "__main__":
    for kind in FIELDS:
        build(kind)
