# PyCarinthia Website

Python-native static site for PyCarinthia, built with Pelican.

## Requirements

- Python 3.11 or newer
- Pelican dependencies from `requirements.txt` or `pyproject.toml`

With `uv`:

```sh
.local/bin/uv sync
.local/bin/uv run python tools/build.py
```

With an existing Python installation:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python tools/build.py
```

The generated static site is written to `output/`.

## Run locally

```sh
.local/bin/uv run python tools/build.py --serve
```

Then open `http://localhost:8000`.

## Add events with Markdown

Create a file in `content/events/`:

```md
Title: Your meetup title
Date: 2026-11-03 18:30
Event_date: 2026-11-03T18:30:00+01:00
End_date: 2026-11-03T20:30:00+01:00
Category: events
Slug: your-meetup-title
Venue: Venue name
Address: Street, city
City: Klagenfurt
Format: Talks + lightning talks
Description: Short summary for listings.
External_url: https://example.com/rsvp
Map_url: https://www.google.com/maps/dir/?api=1&destination=Venue%20name%2C%20Klagenfurt

Longer event details go here.
```

## Add resources with Markdown

Create a file in `content/resources/`:

```md
Title: python.org
Date: 2026-01-01
Category: resources
Slug: python-org
Resource_category: learn
External_url: https://www.python.org/
Description: Official Python downloads, documentation, and news.
Order: 10
```

## Add remote APIs

The Python build script can merge remote JSON into generated Markdown before
Pelican runs:

```sh
PYCARINTHIA_EVENTS_API=https://example.com/events.json python tools/build.py
PYCARINTHIA_RESOURCES_API=https://example.com/resources.json python tools/build.py
```

## Configure forms and RSVP links

The site does not require groupware or a configured mailbox. Contact and talk
proposal pages are static pages that can link to Google Forms when the form URLs
are configured:

```sh
PYCARINTHIA_CONTACT_FORM_URL=https://forms.gle/example-contact python tools/build.py
PYCARINTHIA_PROPOSAL_FORM_URL=https://forms.gle/example-proposal python tools/build.py
```

For GitHub Pages, set these as repository variables:

- `PYCARINTHIA_CONTACT_FORM_URL`
- `PYCARINTHIA_PROPOSAL_FORM_URL`
- `PYCARINTHIA_RSVP_PLATFORM_URL`

For event RSVPs, add the registration URL to the event Markdown. A Google Form
is enough for the first meetup:

```md
External_url: https://docs.google.com/forms/d/e/example/viewform
```

Later, a Lu.ma event can be used instead. Lu.ma can keep the event registration
page live while the venue is still to be announced. Once the venue is confirmed,
update the Lu.ma event location and the event Markdown in this repository.

Expected event payload:

```json
{
  "events": [
    {
      "id": "example-event",
      "title": "Example event",
      "date": "2026-11-03T18:30:00+01:00",
      "endDate": "2026-11-03T20:30:00+01:00",
      "venue": "Venue",
      "address": "Address",
      "city": "Klagenfurt",
      "format": "Talk",
      "description": "Short event summary",
      "externalUrl": "https://example.com/rsvp",
      "mapUrl": "https://www.google.com/maps/dir/?api=1&destination=Venue%20name%2C%20Klagenfurt"
    }
  ]
}
```

Expected resource payload:

```json
{
  "resources": [
    {
      "id": "example-resource",
      "title": "Example",
      "url": "https://example.com/",
      "category": "learn",
      "description": "A useful Python resource",
      "order": 50
    }
  ]
}
```

If a remote request fails, the build continues with local Markdown.
