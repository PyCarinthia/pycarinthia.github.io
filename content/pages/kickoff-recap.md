Title: PyCarinthia #1 – hello_world: the recap
Slug: kickoff-python-ai-carinthia-recap
Url: events/kickoff-python-ai-carinthia/recap/
Save_as: events/kickoff-python-ai-carinthia/recap/index.html
Template: recap
Description: Talk summaries, slides, and photos from the first PyCarinthia meetup on 14 October 2026 at the University of Klagenfurt.
Event_date_label: 14 October 2026
Venue: Omansaal, University of Klagenfurt
Event: events/kickoff-python-ai-carinthia/
Slides: slides/1/
Image: assets/events/kickoff/photos/00.jpg

<div class="photo-hero">
<figure><a class="lightbox" data-gallery="hero" href="{static}/assets/events/kickoff/photos/00.jpg"><img src="{static}/assets/events/kickoff/photos/00.jpg" alt="A full Omansaal seen from the back row during the first talk of PyCarinthia #1"></a><figcaption>A full Omansaal seen from the back row during the first talk of PyCarinthia #1</figcaption></figure>
</div>

On 14 October 2026 the Omansaal at the University of Klagenfurt filled up for the very first PyCarinthia meetup. After a short welcome, three speakers took the stage: a maintainer's view on one of the best-known Python animation libraries, an AI system that helps rescue teams in highway tunnels, and a pipeline that teaches a language model to ask a multimeter for help. Plenty of questions followed each talk, and the conversations carried on well past the official end.

<a class="button dark" href="/slides/1/" target="_blank" rel="noopener">View the slides</a>

## Opening

Harald Nezbeda and Gabriel Lipnik opened the evening with what PyCarinthia is meant to be: a free, open meetup for everyone in Carinthia who builds with Python and AI, from students and researchers to professionals and hobbyists. They introduced the Code of Conduct, thanked the FTF (Förderverein Technische Fakultät) and the University of Klagenfurt for their support, and walked through the agenda.

<div class="photo-grid photo-grid--1">
<figure><a class="lightbox" data-gallery="opening" href="{static}/assets/events/kickoff/photos/01.jpg"><img src="{static}/assets/events/kickoff/photos/01-thumb.jpg" alt="Harald Nezbeda walking the audience through the evening's agenda" loading="lazy"></a><figcaption>Harald Nezbeda walking the audience through the evening's agenda</figcaption></figure>
</div>

## The talks

### Benjamin Hackl: Musings from Maintaining Manim

Benjamin talked about the evolution, the technical challenges, and the community side of Manim, the Python library for programmatic mathematical animations.

- **Programmed, not prompted.** Generative AI can produce videos from a text prompt, but code-based animation gives precise control over every detail and stays consistent, which matters for educational content.
- **The community fork.** He explained the history of the split between the original Manim by Grant Sanderson (3Blue1Brown) and the community-maintained version, created to offer a stable, documented release cycle instead of breaking changes between videos.
- **Moving to 3D.** A large part of the talk covered the long refactoring towards an OpenGL-based 3D renderer. Because the community version had diverged so far from the original, this was a massive undertaking, and AI turned out to be a real force multiplier for the large-scale refactoring.
- **Maintenance in the age of AI.** Benjamin also showed the unglamorous side: floods of low-quality, automated pull requests from AI agents hunting for good first issues, governance and interpersonal conflicts in a community-led project, sustainable onboarding for new contributors, and why a project needs a clear AI policy so that humans stay in charge of its direction.

<div class="photo-grid">
<figure><a class="lightbox" data-gallery="benjamin" href="{static}/assets/events/kickoff/photos/02.jpg"><img src="{static}/assets/events/kickoff/photos/02-thumb.jpg" alt="Benjamin Hackl next to his title slide, Musings from Maintaining Manim" loading="lazy"></a><figcaption>Benjamin Hackl next to his title slide, Musings from Maintaining Manim</figcaption></figure>
<figure><a class="lightbox" data-gallery="benjamin" href="{static}/assets/events/kickoff/photos/03.jpg"><img src="{static}/assets/events/kickoff/photos/03-thumb.jpg" alt="Benjamin Hackl live-demoing Manim shapes in a Jupyter notebook" loading="lazy"></a><figcaption>Benjamin Hackl live-demoing Manim shapes in a Jupyter notebook</figcaption></figure>
<figure><a class="lightbox" data-gallery="benjamin" href="{static}/assets/events/kickoff/photos/04.jpg"><img src="{static}/assets/events/kickoff/photos/04-thumb.jpg" alt="Benjamin Hackl pointing at a chart of Manim pull request reviewers per year" loading="lazy"></a><figcaption>Benjamin Hackl pointing at a chart of Manim pull request reviewers per year</figcaption></figure>
</div>

### Alina Nessel: LiveSaferOverview: Saving Lives in Tunnels with AI

Alina presented a project that helps emergency services keep an overview during accidents in highway tunnels, where high speeds and confined spaces make every incident dangerous.

- **The problem.** Tunnel accidents are rare, so they are chaotic for fire brigades, police, and paramedics alike. Without a clear, real-time picture of where vehicles are inside the tunnel, coordinating a rescue is difficult and risky.
- **The idea.** GPS does not work reliably underground, and sirens or flashing lights are no help for tracking. LiveSaferOverview therefore uses the camera infrastructure that tunnels already have.
- **The dataset.** No public dataset of Austrian emergency vehicles existed, so footage was recorded together with the fire brigade, the Red Cross, and the police, showing vehicles in many positions and manoeuvres.
- **The system.** A detection model identifies emergency vehicles in the camera feeds in real time. Because the tunnel's distances were measured, the system can show on a live map exactly where each vehicle is and where rescuers need to go.
- **Recognition.** Tunnel emergency services welcomed the visual confirmation of where help is needed, and the project has won several awards, including the Bosch Innovation Award.

<div class="photo-grid">
<figure><a class="lightbox" data-gallery="alina" href="{static}/assets/events/kickoff/photos/05.jpg"><img src="{static}/assets/events/kickoff/photos/05-thumb.jpg" alt="Alina Nessel opening her LiveSaferOverview talk on saving lives in tunnels with AI" loading="lazy"></a><figcaption>Alina Nessel opening her LiveSaferOverview talk on saving lives in tunnels with AI</figcaption></figure>
<figure><a class="lightbox" data-gallery="alina" href="{static}/assets/events/kickoff/photos/13.jpg"><img src="{static}/assets/events/kickoff/photos/13-thumb.jpg" alt="Alina Nessel explaining how LiveSaferOverview supports rescue teams" loading="lazy"></a><figcaption>Alina Nessel explaining how LiveSaferOverview supports rescue teams</figcaption></figure>
<figure><a class="lightbox" data-gallery="alina" href="{static}/assets/events/kickoff/photos/06.jpg"><img src="{static}/assets/events/kickoff/photos/06-thumb.jpg" alt="Alina Nessel presenting AI detection of emergency vehicles in tunnel camera feeds" loading="lazy"></a><figcaption>Alina Nessel presenting AI detection of emergency vehicles in tunnel camera feeds</figcaption></figure>
</div>

### Christian Klimbacher: When AI Calls a Multimeter for Help, You Get More Than Expected

In the final talk, Christian showed a system for reverse-engineering printed circuit boards when no schematics, documentation, or bill of materials exist, a common problem when maintaining legacy hardware and industrial machines.

- **Lost documentation.** Many industrial machines have been running for decades, and when they fail, the original schematics are often gone. Technicians rely on experience, searching for components and following traces by eye.
- **The eyes.** The pipeline starts from a smartphone photo of the board. A localiser model finds the components (capacitors, ICs, resistors), and a vision-language model reads their markings.
- **The knowledge.** From those markings the system fetches datasheets automatically, builds a bill of materials, and works out the function of individual IC pins.
- **The verification.** Models can misread labels or hallucinate, so the system is deliberately conservative: a multimeter measures components in-circuit, for example confirming that a resistor really is 10 kΩ, before a value is trusted. Christian demonstrated this live on stage.
- **What comes next.** Phase 1, reconstructing the bill of materials, works today. Phase 2, rebuilding the netlist from the traces, has started. Phase 3 aims at understanding the circuit's original logic.
- **Human in the loop.** The goal is not to replace technicians but to give them an assistant that reads hundreds of pages of datasheets and repeats measurements instantly, so they can focus on the actual repair.

<div class="photo-grid photo-grid--2">
<figure><a class="lightbox" data-gallery="christian" href="{static}/assets/events/kickoff/photos/07.jpg"><img src="{static}/assets/events/kickoff/photos/07-thumb.jpg" alt="Christian Klimbacher beside his title slide, When AI Calls a Multimeter for Help" loading="lazy"></a><figcaption>Christian Klimbacher beside his title slide, When AI Calls a Multimeter for Help</figcaption></figure>
<figure><a class="lightbox" data-gallery="christian" href="{static}/assets/events/kickoff/photos/08.jpg"><img src="{static}/assets/events/kickoff/photos/08-thumb.jpg" alt="The audience following a system diagram during the third talk" loading="lazy"></a><figcaption>The audience following a system diagram during the third talk</figcaption></figure>
<figure><a class="lightbox" data-gallery="christian" href="{static}/assets/events/kickoff/photos/09.jpg"><img src="{static}/assets/events/kickoff/photos/09-thumb.jpg" alt="Christian Klimbacher taking a live measurement with multimeter probes on stage" loading="lazy"></a><figcaption>Christian Klimbacher taking a live measurement with multimeter probes on stage</figcaption></figure>
<figure><a class="lightbox" data-gallery="christian" href="{static}/assets/events/kickoff/photos/10.jpg"><img src="{static}/assets/events/kickoff/photos/10-thumb.jpg" alt="Christian Klimbacher showing his circuit board analysis tool on the projector" loading="lazy"></a><figcaption>Christian Klimbacher showing his circuit board analysis tool on the projector</figcaption></figure>
</div>

## After the talks

The evening closed with a group photo of the speakers and organisers, followed by drinks. Small groups formed around each of the speakers, and the conversations carried on long after the last slide.

<div class="photo-grid photo-grid--2">
<figure><a class="lightbox" data-gallery="after" href="{static}/assets/events/kickoff/photos/11.jpg"><img src="{static}/assets/events/kickoff/photos/11-thumb.jpg" alt="Organiser Harald Nezbeda, speakers Benjamin Hackl, Alina Nessel and Christian Klimbacher, and organiser Gabriel Lipnik in front of the PyCarinthia #1 title slide" loading="lazy"></a><figcaption>Organiser Harald Nezbeda, speakers Benjamin Hackl, Alina Nessel and Christian Klimbacher, and organiser Gabriel Lipnik in front of the PyCarinthia #1 title slide</figcaption></figure>
<figure><a class="lightbox" data-gallery="after" href="{static}/assets/events/kickoff/photos/12.jpg"><img src="{static}/assets/events/kickoff/photos/12-thumb.jpg" alt="One of the groups that formed around the speakers after the talks, here with Christian and his multimeter" loading="lazy"></a><figcaption>One of the groups that formed around the speakers after the talks, here with Christian and his multimeter</figcaption></figure>
</div>

<p class="photo-credit">Photos: Gabriel Lipnik and Harald Nezbeda</p>
