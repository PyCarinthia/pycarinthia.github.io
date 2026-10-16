Title: PyCarinthia #1 – hello_world
Date: 2026-10-14 17:30
Event_date: 2026-10-14T17:30:00+02:00
End_date: 2026-10-14T19:30:00+02:00
Category: events
Slug: kickoff-python-ai-carinthia
Venue: Omansaal, University of Klagenfurt
Address: Universitätsstraße 67
City: Klagenfurt
Map_url: https://campusplan.aau.at/?campus=1&q=Z.1.29#map
Lat: 46.61633
Lon: 14.26558
Format: Intro + 2–3 talks
Description: The first PyCarinthia meetup: a short intro, two to three talks, open discussion, and drinks afterwards. Supported by the FTF (Förderverein Technische Fakultät).
External_url: https://www.meetup.com/pycarinthia/events/316488225/
External_label: RSVP on Meetup
Image: assets/events/kickoff/social.jpg
Poster: assets/events/kickoff/poster.jpg
Slides: slides/1/

The first PyCarinthia meetup. The goal is simple: meet the people in Carinthia who build with Python and AI, and shape the community together.

The evening opens with a short intro to what PyCarinthia is and what it can become, followed by two to three talks on Python, AI, and everything around them. Afterwards there is open discussion and drinks. Details on the exact schedule will follow.

## How it went

<div class="recap" markdown="1">

On 14 October the Omansaal at the University of Klagenfurt filled up for the very first PyCarinthia meetup. Three talks, plenty of questions, and conversations that carried on well past the official end over drinks.

<a class="lightbox photo-hero" href="{static}/assets/events/kickoff/photos/00.jpg"><img src="{static}/assets/events/kickoff/photos/00.jpg" alt="A full Omansaal seen from the back row during the first talk of PyCarinthia #1"></a>

<a class="button dark" href="/slides/1/" target="_blank" rel="noopener">View the slides</a>

### The talks

**Benjamin Hackl – Musings from Maintaining Manim.** Benjamin showed why code-driven animation still beats prompted video when precision and consistency matter, and told the story of the Manim Community fork. He walked through the long road to an OpenGL 3D renderer, where AI turned out to be a real force multiplier for the refactoring, and the less glamorous side of maintenance: floods of low-quality AI pull requests, governance, and why a project needs a clear AI policy.

**Alina Nessel – LiveSaferOverview.** Tunnel accidents are rare, which makes them chaotic for rescue teams, and GPS does not work underground. Alina's system reuses the existing tunnel cameras: a detection model trained on footage recorded with fire brigade, Red Cross and police tracks emergency vehicles and shows on a live map which emergency exits are occupied. The project has won several awards, including the Bosch Innovation Award.

**Christian Klimbacher – When AI Calls a Multimeter for Help.** Old industrial machines often come without schematics. Christian's pipeline starts from a phone photo of a circuit board: a vision model locates and reads the components, datasheets are fetched automatically to build a bill of materials, and a multimeter checks the values in-circuit before anything is trusted. Next up: rebuilding the netlist from the traces, always with the technician in the loop.

<div class="photo-grid">
<a class="lightbox" href="{static}/assets/events/kickoff/photos/01.jpg"><img src="{static}/assets/events/kickoff/photos/01-thumb.jpg" alt="Harald Nezbeda walking the audience through the evening's agenda" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/02.jpg"><img src="{static}/assets/events/kickoff/photos/02-thumb.jpg" alt="Benjamin Hackl next to his title slide, Musings from Maintaining Manim" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/03.jpg"><img src="{static}/assets/events/kickoff/photos/03-thumb.jpg" alt="Benjamin Hackl live-demoing Manim shapes in a Jupyter notebook" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/04.jpg"><img src="{static}/assets/events/kickoff/photos/04-thumb.jpg" alt="Benjamin Hackl pointing at a chart of Manim pull request reviewers per year" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/05.jpg"><img src="{static}/assets/events/kickoff/photos/05-thumb.jpg" alt="Alina Nessel opening her LiveSaferOverview talk on saving lives in tunnels with AI" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/06.jpg"><img src="{static}/assets/events/kickoff/photos/06-thumb.jpg" alt="Alina Nessel presenting AI detection of emergency vehicles in tunnel camera feeds" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/07.jpg"><img src="{static}/assets/events/kickoff/photos/07-thumb.jpg" alt="Christian Klimbacher beside his title slide, When AI Calls a Multimeter for Help" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/08.jpg"><img src="{static}/assets/events/kickoff/photos/08-thumb.jpg" alt="The audience following a system diagram during the third talk" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/09.jpg"><img src="{static}/assets/events/kickoff/photos/09-thumb.jpg" alt="Christian Klimbacher taking a live measurement with multimeter probes on stage" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/10.jpg"><img src="{static}/assets/events/kickoff/photos/10-thumb.jpg" alt="Christian Klimbacher showing his circuit board analysis tool on the projector" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/11.jpg"><img src="{static}/assets/events/kickoff/photos/11-thumb.jpg" alt="Organiser Harald Nezbeda, speakers Benjamin Hackl, Alina Nessel and Christian Klimbacher, and organiser Gabriel Lipnik in front of the PyCarinthia #1 title slide" loading="lazy"></a>
<a class="lightbox" href="{static}/assets/events/kickoff/photos/12.jpg"><img src="{static}/assets/events/kickoff/photos/12-thumb.jpg" alt="Attendees chatting around the multimeter after the talks" loading="lazy"></a>
</div>

<p class="photo-credit">Photos: Gabriel Lipnik and Harald Nezbeda</p>

</div>

## Speakers

<div class="speakers" markdown="1">

<div class="speaker" markdown="1">

### Christian Klimbacher: When AI Calls a Multimeter for Help, You Get More Than Expected

[![Speaker card for Christian Klimbacher]({static}/assets/events/kickoff/speaker-christian-klimbacher.jpg){: .speaker-card }]({static}/assets/events/kickoff/speaker-christian-klimbacher.jpg){: .lightbox }

Given nothing but a photo of an unknown circuit board, can we work out what is on it? This talk walks through a Python system that loops over imperfect sources: a vision LLM reads the board, datasheets supply expectations, and a simple multimeter measures in-circuit, where parallel paths make any single reading unclear. Each source only knows part of the answer, but together they find values that were unknown before. Live measurement on stage included.

</div>

<div class="speaker" markdown="1">

### Benjamin Hackl: Musings from Maintaining Manim

[![Speaker card for Benjamin Hackl]({static}/assets/events/kickoff/speaker-benjamin-hackl.jpg){: .speaker-card }]({static}/assets/events/kickoff/speaker-benjamin-hackl.jpg){: .lightbox }

Manim is a Python library for creating mathematical animations, originally built by popular math communicator Grant “3Blue1Brown” Sanderson. After a quick interactive demo, I’ll talk about my path into open source and explain why my car mechanic is responsible both for me being rude to people on the internet and for me occasionally getting to press the “new Manim release” button. On a more serious note, I will share some thoughts about community building and dealing with AI slop in the age of the clankers.

</div>

<div class="speaker" markdown="1">

### Alina Nessel: LiveSaferOverview: Saving Lives in Tunnels with AI

[![Speaker card for Alina Nessel]({static}/assets/events/kickoff/speaker-alina-nessel.jpg){: .speaker-card }]({static}/assets/events/kickoff/speaker-alina-nessel.jpg){: .lightbox }

When an accident happens in a highway tunnel, rescue teams face a major challenge: keeping a clear overview of the situation. LiveSaferOverview uses Artificial Intelligence to solve this problem. I trained the AI with 80,000 images so it can automatically track emergency vehicles using normal tunnel cameras. It then shows their exact positions on a digital, real-time map on a smartphone. This clear overview prevents rescue teams from driving to the wrong location. By saving these critical minutes, the AI helps to save lives.

</div>

</div>

## Good to know

Just here to listen? Perfect. Come along, ask questions, or simply see who else is around.

RSVPs run through our [Meetup group](https://www.meetup.com/pycarinthia/events/316488225/). This page stays the canonical record of the event, so the details here hold even if Meetup does not.

Python, AI, data, web, automation, open source, research, hobby projects - all of it is welcome. The only prerequisite is curiosity.

This kickoff is kindly supported by the [FTF (Förderverein Technische Fakultät)](https://www.ftf.or.at/).
