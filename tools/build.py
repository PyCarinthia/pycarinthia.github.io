from __future__ import annotations

import argparse
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from dateutil import parser

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
REMOTE = CONTENT / "_remote"
OUTPUT = ROOT / "output"
VIENNA = ZoneInfo("Europe/Vienna")


def slugify(value: str) -> str:
    chars = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum() and char.isascii():
            chars.append(char)
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True
    return "".join(chars).strip("-") or "item"


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\r", " ").replace("\n", " ").strip()


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    parsed = parser.parse(str(value))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=VIENNA)
    return parsed.astimezone(VIENNA)


def pelican_date(value: Any) -> str:
    parsed = parse_datetime(value) or datetime.now(VIENNA)
    return parsed.strftime("%Y-%m-%d %H:%M")


def write_markdown(path: Path, metadata: dict[str, Any], body: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for key, value in metadata.items():
        text = clean_text(value)
        if text:
            lines.append(f"{key}: {text}")
    lines.append("")
    lines.append(body.strip() or clean_text(metadata.get("Description", "")))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def fetch_json_array(env_name: str, key: str) -> list[dict[str, Any]]:
    url = os.environ.get(env_name)
    if not url:
        return []
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        print(f"Skipping {env_name}: {exc}", file=sys.stderr)
        return []

    rows = payload if isinstance(payload, list) else payload.get(key, [])
    return [row for row in rows if isinstance(row, dict)]


def sync_remote_content() -> None:
    if REMOTE.exists():
        shutil.rmtree(REMOTE)

    for row in fetch_json_array("PYCARINTHIA_EVENTS_API", "events"):
        title = clean_text(row.get("title"))
        event_date = clean_text(row.get("date") or row.get("event_date"))
        venue = clean_text(row.get("venue"))
        description = clean_text(row.get("description"))
        if not (title and event_date and venue and description):
            continue

        slug = clean_text(row.get("id")) or slugify(f"{title}-{event_date}")
        write_markdown(
            REMOTE / "events" / f"{slug}.md",
            {
                "Title": title,
                "Date": pelican_date(event_date),
                "Event_date": event_date,
                "End_date": row.get("endDate") or row.get("end_date"),
                "Category": "events",
                "Slug": slug,
                "Venue": venue,
                "Address": row.get("address"),
                "City": row.get("city") or "Klagenfurt",
                "Format": row.get("format") or "Meetup",
                "Description": description,
                "External_url": row.get("externalUrl") or row.get("external_url") or row.get("url"),
                "Map_url": row.get("mapUrl") or row.get("map_url"),
                "Lat": row.get("lat") or row.get("latitude"),
                "Lon": row.get("lon") or row.get("lng") or row.get("longitude"),
            },
            clean_text(row.get("body")) or description,
        )

    for row in fetch_json_array("PYCARINTHIA_RESOURCES_API", "resources"):
        title = clean_text(row.get("title"))
        url = clean_text(row.get("url") or row.get("externalUrl") or row.get("external_url"))
        description = clean_text(row.get("description"))
        if not (title and url and description):
            continue

        slug = clean_text(row.get("id")) or slugify(title)
        write_markdown(
            REMOTE / "resources" / f"{slug}.md",
            {
                "Title": title,
                "Date": "2026-01-01",
                "Category": "resources",
                "Slug": slug,
                "Resource_category": row.get("category") or "tools",
                "External_url": url,
                "Description": description,
                "Order": row.get("order") or 100,
            },
            description,
        )


def read_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    return metadata


def content_files(*parts: str) -> list[Path]:
    files: list[Path] = []
    for part in parts:
        directory = CONTENT / part
        if directory.exists():
            files.extend(sorted(directory.glob("*.md")))
    return files


def load_events() -> list[dict[str, Any]]:
    events = []
    for path in content_files("events", "_remote/events"):
        meta = read_metadata(path)
        event_date = parse_datetime(meta.get("event_date") or meta.get("date"))
        if not event_date:
            continue
        source = "remote" if "_remote" in path.parts else "markdown"
        events.append(
            {
                "id": meta.get("slug") or path.stem,
                "slug": meta.get("slug") or path.stem,
                "title": meta.get("title", ""),
                "date": event_date.isoformat(),
                "endDate": (parse_datetime(meta.get("end_date")) or "").isoformat()
                if meta.get("end_date")
                else None,
                "venue": meta.get("venue", ""),
                "address": meta.get("address", ""),
                "city": meta.get("city", "Klagenfurt"),
                "format": meta.get("format", "Meetup"),
                "description": meta.get("description", ""),
                "externalUrl": meta.get("external_url", ""),
                "mapUrl": meta.get("map_url", ""),
                "lat": meta.get("lat", ""),
                "lon": meta.get("lon", ""),
                "source": source,
            }
        )
    return sorted(events, key=lambda event: event["date"])


def load_resources() -> list[dict[str, Any]]:
    resources = []
    for path in content_files("resources", "_remote/resources"):
        meta = read_metadata(path)
        source = "remote" if "_remote" in path.parts else "markdown"
        resources.append(
            {
                "id": meta.get("slug") or path.stem,
                "title": meta.get("title", ""),
                "url": meta.get("external_url", ""),
                "category": meta.get("resource_category", "tools"),
                "description": meta.get("description", ""),
                "order": int(meta.get("order", "100")),
                "source": source,
            }
        )
    return sorted(resources, key=lambda item: (item["category"], item["order"], item["title"]))


def utc_stamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def escape_ics(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")


def write_calendar(events: list[dict[str, Any]]) -> None:
    now = datetime.now(VIENNA)
    upcoming = [event for event in events if parse_datetime(event["date"]) and parse_datetime(event["date"]) >= now]
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//PyCarinthia//Meetups//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    if upcoming:
        event = upcoming[0]
        start = parse_datetime(event["date"]) or now
        end = parse_datetime(event.get("endDate")) or (start + timedelta(hours=2))
        location = ", ".join(filter(None, [event.get("venue"), event.get("address"), event.get("city")]))
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{escape_ics(event['id'])}@pycarinthia.com",
                f"DTSTAMP:{utc_stamp(now)}",
                f"DTSTART:{utc_stamp(start)}",
                f"DTEND:{utc_stamp(end)}",
                f"SUMMARY:{escape_ics(event['title'])}",
                f"DESCRIPTION:{escape_ics(event.get('description', ''))}",
                f"LOCATION:{escape_ics(location)}",
            ]
        )
        if event.get("externalUrl"):
            lines.append(f"URL:{escape_ics(event['externalUrl'])}")
        lines.append("END:VEVENT")
    lines.extend(["END:VCALENDAR", ""])
    (OUTPUT / "calendar.ics").write_text("\r\n".join(lines), encoding="utf-8")


def export_static_feeds() -> None:
    api = OUTPUT / "api"
    api.mkdir(parents=True, exist_ok=True)
    events = load_events()
    resources = load_resources()
    (api / "events.json").write_text(json.dumps({"events": events}, indent=2), encoding="utf-8")
    (api / "resources.json").write_text(json.dumps({"resources": resources}, indent=2), encoding="utf-8")
    write_calendar(events)


def run_pelican(settings: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pelican", "content", "-s", settings, "-o", str(OUTPUT)],
        cwd=ROOT,
        check=True,
    )


def serve(port: int) -> None:
    mimetypes.add_type("text/calendar", ".ics")
    mimetypes.add_type("application/json", ".json")
    os.chdir(OUTPUT)
    server = ThreadingHTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"Serving PyCarinthia at http://localhost:{port}")
    server.serve_forever()


def main() -> None:
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument("--settings", default="pelicanconf.py")
    parser_arg.add_argument("--serve", action="store_true")
    parser_arg.add_argument("--port", type=int, default=8000)
    args = parser_arg.parse_args()

    sync_remote_content()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    run_pelican(args.settings)
    export_static_feeds()

    if args.serve:
        serve(args.port)


if __name__ == "__main__":
    main()
