from pathlib import Path
from datetime import datetime
import os
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))

from jinja_filters import (  # noqa: E402
    category_articles,
    event_day,
    event_month,
    event_time,
    event_date_long,
    event_date_short,
    gcal_url,
    group_resources,
    past_events,
    resource_articles,
    upcoming_events,
)

AUTHOR = "PyCarinthia"
SITENAME = "PyCarinthia"
SITEURL = ""
SITEDESCRIPTION = (
    "A Python and AI community in Carinthia, Austria. Meetups, talks, "
    "workshops, and hands-on sessions for everyone building with Python and AI."
)

PATH = "content"
OUTPUT_PATH = "output"
THEME = "theme/pycarinthia"
TIMEZONE = "Europe/Vienna"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%d %B %Y"
WITH_FUTURE_DATES = True
CURRENTYEAR = datetime.now().year

ARTICLE_PATHS = ["events", "resources", "_remote/events", "_remote/resources"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["assets", "CNAME"]

ARTICLE_URL = "{category}/{slug}/"
ARTICLE_SAVE_AS = "{category}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

DIRECT_TEMPLATES = ["index", "events", "resources", "contact", "propose"]
INDEX_SAVE_AS = "index.html"
EVENTS_SAVE_AS = "events/index.html"
RESOURCES_SAVE_AS = "resources/index.html"
CONTACT_SAVE_AS = "contact/index.html"
PROPOSE_SAVE_AS = "propose/index.html"

DEFAULT_PAGINATION = False
RELATIVE_URLS = True

AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAG_SAVE_AS = ""
TAGS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
    },
    "output_format": "html5",
}

JINJA_FILTERS = {
    "category_articles": category_articles,
    "event_day": event_day,
    "event_month": event_month,
    "event_time": event_time,
    "event_date_long": event_date_long,
    "event_date_short": event_date_short,
    "gcal_url": gcal_url,
    "group_resources": group_resources,
    "past_events": past_events,
    "resource_articles": resource_articles,
    "upcoming_events": upcoming_events,
}

CONTACT_EMAIL = os.environ.get("PYCARINTHIA_CONTACT_EMAIL", "").strip()
CONTACT_FORM_URL = (
    os.environ.get("PYCARINTHIA_CONTACT_FORM_URL")
    or "https://docs.google.com/forms/d/e/1FAIpQLSePGyf31A5aACrihtroRjplqEsf8Gp0unqoSopHRhrkc8L3Rw/viewform"
).strip()
PROPOSAL_FORM_URL = (
    os.environ.get("PYCARINTHIA_PROPOSAL_FORM_URL")
    or "https://docs.google.com/forms/d/e/1FAIpQLSc-QutaLbcQtLzWISr9uv57bqpRBMiz9AM50ScVYflTZWluhA/viewform"
).strip()
RSVP_PLATFORM_URL = (
    os.environ.get("PYCARINTHIA_RSVP_PLATFORM_URL")
    or "https://docs.google.com/forms/d/e/1FAIpQLScMr_JMksm4Awxjmjms07zOjZducAnPaH0AwYO68BebWPGVcQ/viewform"
).strip()
NEWSLETTER_URL = (
    os.environ.get("PYCARINTHIA_NEWSLETTER_URL")
    or "https://docs.google.com/forms/d/e/1FAIpQLSeJ5nA5ygbk7nOagc4Zy9OS2inouvzudlgtEAUhx3YU3178IQ/viewform"
).strip()
CONTACT_URL = "/contact/"
PROPOSAL_URL = "/propose/"
DEFAULT_CITY = "Klagenfurt"
VENUE_MAP_EMBED = (
    "/assets/basemap.html?lat=46.6149&lon=14.2654&zoom=16"
    "&label=Lakeside%20Science%20and%20Technology%20Park"
)

FORMATS = [
    {
        "label": "Talks",
        "text": "One focused session on a Python library, AI tool, LLM application, production story, or data workflow people can learn from.",
    },
    {
        "label": "Lightning talks",
        "text": "Five-minute demos and ideas. Low pressure, useful for first-time speakers, and good for discovering what people are building.",
    },
    {
        "label": "Hands-on sessions",
        "text": "Workshops, pairing, coding nights, open-source sprints, and practical sessions where people bring a laptop.",
    },
    {
        "label": "Social evenings",
        "text": "Unstructured time after the program for questions, hiring chats, AI project ideas, and meeting other Python and AI people nearby.",
    },
]

CONNECT_LINKS = [
    {
        "label": "Talks",
        "title": "Proposal form",
        "href": PROPOSAL_URL,
        "text": "Suggest a talk, demo, workshop, or lightning introduction.",
    },
    {
        "label": "Contact",
        "title": "Contact form",
        "href": CONTACT_URL,
        "text": "Questions, venue offers, sponsors, and organizing help.",
    },
    {
        "label": "Communities",
        "title": "Regional communities",
        "href": "/resources/#category-community",
        "text": "Python, PyData, AI, and ML groups across Austria, Slovenia, and Italy.",
    },
]
