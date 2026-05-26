from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

from dateutil import parser

VIENNA = ZoneInfo("Europe/Vienna")

_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_MONTHS = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]
_MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def meta_value(item: object, key: str, default: str = "") -> str:
    value = getattr(item, key, None)
    if value is None and hasattr(item, "metadata"):
        value = getattr(item, "metadata", {}).get(key)
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None:
        return default
    return str(value)


def article_category(article: object) -> str:
    return str(getattr(article, "category", "")).lower()


def category_articles(articles: list[object], category: str) -> list[object]:
    return [article for article in articles if article_category(article) == category]


def event_datetime(article: object) -> datetime | None:
    raw = meta_value(article, "event_date") or getattr(article, "date", None)
    if raw is None:
        return None
    if isinstance(raw, datetime):
        parsed = raw
    elif isinstance(raw, date):
        parsed = datetime(raw.year, raw.month, raw.day)
    else:
        parsed = parser.parse(str(raw))

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=VIENNA)
    return parsed.astimezone(VIENNA)


def build_now() -> datetime:
    raw = os.environ.get("PYCARINTHIA_NOW")
    if raw:
        parsed = parser.parse(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=VIENNA)
        return parsed.astimezone(VIENNA)
    return datetime.now(VIENNA)


def sorted_events(articles: list[object]) -> list[object]:
    events = category_articles(articles, "events")
    return sorted(events, key=lambda article: event_datetime(article) or datetime.max.replace(tzinfo=VIENNA))


def upcoming_events(articles: list[object]) -> list[object]:
    now = build_now()
    return [article for article in sorted_events(articles) if (event_datetime(article) or now) >= now]


def past_events(articles: list[object]) -> list[object]:
    now = build_now()
    events = [article for article in sorted_events(articles) if (event_datetime(article) or now) < now]
    return list(reversed(events))


def event_month(article: object) -> str:
    dt = event_datetime(article)
    return _MONTHS_SHORT[dt.month - 1] if dt else "TBA"


def event_day(article: object) -> str:
    dt = event_datetime(article)
    return str(dt.day) if dt else "--"


def event_time(article: object) -> str:
    dt = event_datetime(article)
    return dt.strftime("%H:%M") if dt else "TBA"


def event_date_long(article: object) -> str:
    dt = event_datetime(article)
    if not dt:
        return "Date TBA"
    return f"{_DAYS[dt.weekday()]}, {dt.day} {_MONTHS[dt.month - 1]} {dt.year}"


def event_date_short(article: object) -> str:
    dt = event_datetime(article)
    if not dt:
        return "Date TBA"
    return f"{dt.day} {_MONTHS_SHORT[dt.month - 1]} {dt.year}"


def resource_articles(articles: list[object]) -> list[object]:
    resources = category_articles(articles, "resources")
    return sorted(resources, key=lambda article: (int(meta_value(article, "order", "100")), article.title))


def gcal_url(article: object) -> str:
    UTC = timezone.utc
    start = event_datetime(article)
    if not start:
        return ""

    end_raw = meta_value(article, "end_date")
    if end_raw:
        end_dt = parser.parse(str(end_raw))
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=VIENNA)
        end_dt = end_dt.astimezone(UTC)
    else:
        end_dt = start.astimezone(UTC) + timedelta(hours=2)

    start_utc = start.astimezone(UTC)
    fmt = "%Y%m%dT%H%M%SZ"

    title = getattr(article, "title", "")
    description = meta_value(article, "description", "")
    venue = meta_value(article, "venue", "")
    address = meta_value(article, "address", "")
    city = meta_value(article, "city", "")
    location = ", ".join(part for part in [venue, address, city] if part)

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start_utc.strftime(fmt)}/{end_dt.strftime(fmt)}",
        "details": description,
        "location": location,
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)


def group_resources(resources: list[object]) -> list[dict[str, object]]:
    labels = {
        "learn": "Learn Python",
        "ai": "Python and AI",
        "community": "Regional communities",
        "support": "Support PyCarinthia",
        "tools": "Tools",
    }
    groups = {key: [] for key in labels}
    for resource in resource_articles(resources):
        key = meta_value(resource, "resource_category", "tools").lower()
        if key not in groups:
            key = "tools"
        groups[key].append(resource)

    return [
        {"key": key, "label": label, "items": groups[key]}
        for key, label in labels.items()
        if groups[key]
    ]
