---
title: What Gets Lost in the Handoff
date: 2026-04-01
tags: design, process, craft
excerpt: Design intent degrades between the screen and the implementation. The gap isn't always about tools or specs — it's about the reasoning that never got written down.
linkedinUrl:
---

The most expensive moment in a design process isn't a failed usability test or a late pivot. It's the quiet erosion that happens during implementation — when a decision that took two weeks of thinking gets reversed in an afternoon because nobody wrote down why it was made.

I've watched this happen at every scale. A spacing decision rooted in optical balance becomes a round number in code because "4px is cleaner." A button state built for low vision gets flattened because a developer didn't realize the contrast was intentional. A careful microcopy choice — the one that took four rounds of testing to land on — gets swapped for something faster to type.

None of these changes are malicious. They're almost always the result of people working without enough context.

## The documentation that actually helps

The answer isn't more specs. Specs document *what* a design is. What survives a handoff is documentation of *why*.

Why does this component use a border instead of a background color to indicate focus? Because the background color creates ambiguity with the selected state on certain displays. Why is this label 14px instead of 12px? Because we tested it with real users on low-resolution screens and legibility dropped sharply. Why does this error message say "Check your entry" instead of "Invalid input"? Because testing showed the second phrasing made users think their data was rejected, not just formatted incorrectly.

Those whys are the design. The pixels are just their current representation.

## What design systems get right — and miss

A good design system closes some of this gap by encoding decisions into reusable components. If the accessible focus style is built into the button component, individual implementers don't need to know why it exists — it just works.

But design systems don't capture everything. They handle the repeating patterns well and fall apart at the edges: new component types, novel interaction patterns, one-off screens that don't fit neatly into the library. That's exactly where the hardest accessibility and usability work lives.

For those cases, the best thing I've found is proximity. Designers embedded in delivery teams, doing code reviews. Engineers invited into usability sessions. Regular pairing sessions that aren't about shipping features but about understanding the reasoning behind decisions.

## The real question

When I review a built product against its designs, I'm not asking "did they follow the specs?" I'm asking whether the person who implemented this understood what the design was trying to do — and had enough context to make good judgment calls when reality diverged from the mockup.

That understanding doesn't live in a Figma file. It lives in conversations, in documentation culture, in the relationship between design and engineering on a team. Getting that relationship right is more important than any handoff tool — and harder to fix once it's broken.
