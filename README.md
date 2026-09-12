# PyCarinthia Website

Python-native static site for PyCarinthia, built with Pelican.

## Requirements

- Python 3.11 or newer
- Pelican dependencies from `requirements.txt` or `pyproject.toml`

With `uv`:

```sh
uv sync
uv run python tools/build.py
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
uv run python tools/build.py --serve
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
Address: Street and number
City: Klagenfurt
Format: Talks + lightning talks
Description: Short summary for listings.
External_url: https://example.com/rsvp
External_label: RSVP on Meetup
Map_url: https://www.google.com/maps/dir/?api=1&destination=Venue%20name%2C%20Klagenfurt

Longer event details go here.
```

`External_label` is optional and sets the text on the RSVP button; it defaults
to `RSVP` when omitted.

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

## Regenerate icons and logo assets

`content/assets/logo-source.png` is the pristine, opaque source logo and the
only file to replace when the logo changes. Every other logo and icon asset
in `content/assets/` is derived from it and regenerated with:

```sh
uv run --with pillow python tools/make_icons.py
```

This script is a one-off tool, not part of the site build, so Pillow is
deliberately not a project dependency — it is installed ad hoc for this one
run instead. The command writes:

- `logo.png` — transparent logo
- `logo-mark.png` — square brand mark
- `favicon.ico`
- `icon-192.png` and `icon-512.png`
- `apple-touch-icon.png`
- `og-image.png` — social preview image

Commit the generated files alongside the source; they are read back as-is by
the site and must never be edited by hand.

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

For event RSVPs, set `External_url` on the event Markdown to that event's
registration page — currently a Meetup event for PyCarinthia. `External_label`
sets the RSVP button text:

```md
External_url: https://www.meetup.com/pycarinthia/events/316488225/
External_label: RSVP on Meetup
```

`RSVP_PLATFORM_URL` (built from `PYCARINTHIA_RSVP_PLATFORM_URL`) is still
defined in `pelicanconf.py` and still listed above as a repository variable,
but no template currently reads it. It is unused legacy configuration, not
the thing that drives RSVP links.

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
