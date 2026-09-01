# Dev Team Brief — AML/KYC Transaction Review Simulator (PoC Prototype)

## What this is
A working **interaction-design prototype** for one component of the UBL new-employee training PoC: the transaction-review simulation planned as the capstone (sub-module 6) of the AML/KYC training module. It runs standalone in any browser — open `aml-transaction-simulator.html` directly, no build step or dependencies beyond a Google Fonts import.

**This is a prototype, not production code.** Its job is to communicate the interaction design so you can rebuild it properly — not to be extended in place.

## Files in this package
1. `aml-transaction-simulator.html` — the working prototype
2. `AML-KYC-Content-Notes-PoC.md` — the source regulatory content (SBP AML/CFT thresholds, red-flag categories) that the prototype's case data is built from

## What the prototype demonstrates
- A queue of transaction "cases" a trainee reviews one at a time
- Three decision types per case: **Clear / Flag / Escalate** (not binary right/wrong — mirrors how an actual compliance analyst works)
- Flag/Escalate choices require selecting which red-flag indicator applies before submitting, so we're testing *why*, not just *what*
- Immediate feedback tied to the actual regulation logic behind each case
- A progress dial + final score breakdown **by red-flag category** — this category-level breakdown is what an adaptive engine would use to route remediation content

## What's reusable as-is vs. needs rebuilding

**Reuse the pattern, not the code:**
- The interaction flow: `queue → decide → select reason (if flag/escalate) → feedback → next case → score summary`
- The data shape: each case is a plain object with `amount, type, details[], narrative, correct action, category, explanation` — this shape is what should carry forward, whatever the actual implementation

**Rebuild properly:**
- State management — the prototype uses plain JS globals (`current`, `score`, `selectedReasons`); a real build should use proper state (React state/context, or whatever pattern the team standardizes on)
- Case data — currently a hardcoded array in the script; production should pull from a real content/config source so non-developers can add cases
- Scoring — currently client-side only, resets on refresh; production needs persistence and reporting back to whatever admin dashboard UBL will use
- Animations — the "stamp" effect is CSS-only proof of concept; feel free to reimplement with whatever animation approach fits the broader app

## Where this fits in the bigger picture
This is **one modality for one sub-module** of a larger 6-sub-module AML/KYC training design (which itself is one of 3 planned topics for the full PoC). Don't treat this prototype as defining the entire PoC's scope — it's the flagship/most complex piece, built first because it's the best demo of what "adaptive, interactive training" can look like beyond a standard quiz. Other sub-modules use different formats (dialogue simulation, card-based scenarios, document explorer) that are lighter to build.

## Suggested next conversation with the dev team
1. Walk through the live prototype together first — let them click through it before reading any code
2. Review the JS case-data structure — confirm it's a workable shape for however they plan to store/serve content
3. Scope what a "real" version needs beyond the prototype: auth, persistence, admin content-entry, reporting/analytics hooks
4. Decide build approach — React rebuild is expected given the team's stack; vanilla JS prototype is reference only

## Visual re-skin (Aug 2026)

`aml-compliance-academy.html` has been re-skinned into a character-driven
situational-judgement presentation, modelled on the C-Factor reference. What
this means for a production rebuild:

- **Assets** — the prototype now depends on `assets/` (10 character PNGs with
  transparency, 5 background PNGs). These are AI-generated placeholders that
  communicate the intended art direction. Commission or license real art before
  any client-facing use.
- **Reusable pattern** — the cinematic layer is five helpers: `setScene(bgKey)`,
  `actor(artKey, side, opts)`, `say(name, text, opts)` returning a Promise,
  `choices(items, opts)` returning a Promise of the chosen index, and
  `brief(m, bg, art, name, lines)` for the pre-module mentor briefing. That
  promise-based staging API is the part worth carrying into React, not the DOM
  code behind it.
- **Unchanged** — all regulatory content, thresholds, red-flag data, scoring,
  ranks, badges and persistence are exactly as previously reviewed.
- **Dead code left in place deliberately** — `avatar()`, `radarSVG()` and
  `artBankVault()` are no longer called. They are the hand-built SVG fallbacks
  for content that has no illustration asset. Keep or delete at your discretion,
  but know they were working code, not leftovers from a broken edit.
- **Known limitation** — the character layer is decorative and hidden below
  900px viewport width. A production build needs a real mobile treatment.
