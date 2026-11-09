#!/usr/bin/env python3
"""Collect the posts saved by the CMS into the two files the website reads.

  content/events/*.json  ->  data/events.json
  content/news/*.json    ->  data/news.json
  content/team/**/*.json ->  data/team.json  (folders made in the CMS are fine)
  content/departments.json -> data/departments.json
  content/alumni.json -> data/alumni.json

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
    "news": ["title", "category", "date", "pdf", "image", "summary", "body"],
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


def make_slug(path, base, seen, fallback):
    """The address of a post, from its file name. Posts may sit in folders made in the CMS."""
    slug = re.sub(r"[^a-z0-9-]+", "-", path.stem.lower()).strip("-") or fallback
    if slug in seen:  # the same file name in two folders: put the folder in front
        folder = "-".join(path.relative_to(base).parts[:-1] + (path.stem,))
        slug = re.sub(r"[^a-z0-9-]+", "-", folder.lower()).strip("-") or fallback
        n = 2
        while slug in seen:
            slug = f"{slug}-{n}"
            n += 1
    seen.add(slug)
    return slug


def clean_pdf(value):
    value = text(value)
    if value.startswith("https://") and value.lower().split("?")[0].endswith(".pdf"):
        return value
    value = value.lstrip("/")
    return value if value.startswith("assets/") and value.lower().endswith(".pdf") else ""


def build(kind):
    items = []
    base, seen = ROOT / "content" / kind, set()
    for path in sorted(base.rglob("*.json")):
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
        item = {"slug": make_slug(path, base, seen, "post")}
        for field in FIELDS[kind]:
            item[field] = text(raw.get(field))
        item["date"] = date[:10]
        item["image"] = clean_image(raw.get("image"))
        if kind == "news":
            item["pdf"] = clean_pdf(raw.get("pdf"))
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


def write(name, items):
    out = ROOT / "data" / f"{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{name}: {len(items)} published")


def build_team():
    people = []
    base, seen = ROOT / "content" / "team", set()
    for path in sorted(base.rglob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as err:
            warn(path, f"skipped, not valid JSON ({err})")
            continue
        if not isinstance(raw, dict) or raw.get("draft") is True:
            continue
        name = text(raw.get("name"))
        if not name:
            warn(path, "skipped, a name is required")
            continue
        try:
            order = float(raw.get("order"))
        except (TypeError, ValueError):
            order = 100
        people.append({
            "slug": make_slug(path, base, seen, "person"),
            "name": name,
            "department": text(raw.get("department")),
            "role": text(raw.get("role")),
            "photo": clean_image(raw.get("photo")),
            "order": order,
        })
    people.sort(key=lambda p: (p["order"], p["name"]))
    write("team", people)


def build_departments():
    path = ROOT / "content" / "departments.json"
    items = []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        entries = raw.get("departments", []) if isinstance(raw, dict) else []
    except (OSError, ValueError) as err:
        warn(path, f"skipped, not valid JSON ({err})")
        entries = []
    for entry in entries:
        if not isinstance(entry, dict) or not text(entry.get("name")):
            continue
        tasks = entry.get("tasks")
        items.append({
            "name": text(entry.get("name")),
            "summary": text(entry.get("summary")),
            "tasks": [text(t) for t in tasks if text(t)] if isinstance(tasks, list) else [],
        })
    write("departments", items)


def build_alumni():
    path = ROOT / "content" / "alumni.json"
    items = []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        entries = raw.get("companies", []) if isinstance(raw, dict) else []
    except (OSError, ValueError) as err:
        warn(path, f"skipped, not valid JSON ({err})")
        entries = []
    for entry in entries:
        if not isinstance(entry, dict) or not text(entry.get("name")):
            continue
        items.append({
            "name": text(entry.get("name")),
            "group": text(entry.get("group")),
            "logo": clean_image(entry.get("logo")),
        })
    write("alumni", items)


if __name__ == "__main__":
    for kind in FIELDS:
        build(kind)
    build_team()
    build_departments()
    build_alumni()
