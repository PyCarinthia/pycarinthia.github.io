from __future__ import annotations

import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dateutil import parser

VIENNA = ZoneInfo("Europe/Vienna")


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
    return dt.strftime("%b") if dt else "TBA"


def event_day(article: object) -> str:
    dt = event_datetime(article)
    return dt.strftime("%d") if dt else "--"


def event_time(article: object) -> str:
    dt = event_datetime(article)
    return dt.strftime("%H:%M") if dt else "TBA"


def event_date_long(article: object) -> str:
    dt = event_datetime(article)
    return dt.strftime("%A, %-d %B %Y") if dt else "Date TBA"


def event_date_short(article: object) -> str:
    dt = event_datetime(article)
    return dt.strftime("%-d %b %Y") if dt else "Date TBA"


def resource_articles(articles: list[object]) -> list[object]:
    resources = category_articles(articles, "resources")
    return sorted(resources, key=lambda article: (int(meta_value(article, "order", "100")), article.title))


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
