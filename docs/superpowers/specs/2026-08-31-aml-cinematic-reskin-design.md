# SENTINEL — Cinematic Re-skin Design

**Date:** 2026-08-31
**Target:** `aml-compliance-academy.html`
**Goal:** Make the existing AML/KYC academy feel like a produced game rather than a compliance dashboard, matching the visual and staging language of The Talent Games' C-Factor situational judgement test.

---

## 1. Problem

The academy already works. It has four modules, a deterministic rule engine, XP/ranks/badges, persistence, and hand-built SVG art. What it lacks is *production value*: everything is a dark panel on a dark page, characters are 120px procedural SVG circles, and each screen appears instantly with no staging. A trainee experiences it as a form, not a scenario.

The C-Factor reference establishes what "feels like a game" actually means, and it is only half art:

- **Art** — illustrated characters with real faces and body language, standing in real environments.
- **Staging** — characters enter, speak one at a time, a timer counts down, options appear, a mentor reacts to your answer. Time passes between beats.

A re-skin that only swaps images would fix half the problem.

---

## 2. Approach

Keep the engine, replace the presentation layer, and add a story frame.

Untouched: `RULES`, `CATS`, `FLAGS`, `GLOSSARY`, `CDD_STEPS`, `DIALOGUE`, `CUSTOMERS`, `CASES`, `TT_OPTIONS`, `resolveObligation`, `RANKS`, `BADGES`, `MISSIONS`, `KEY`/`S`/`load`/`save`, `rankOf`, `awardXP`, `awardBadge`, `grade`, `shuffle`, `makeDrill`. The regulatory substance and the scoring model are correct and stay exactly as they are.

Replaced: the CSS theme, the four `mission*` render functions' markup, `home`, `results`, `screenVault`, `screenCertificate`, and the `go` router (which gains background/actor awareness).

Added: a cinematic layer of four helpers plus a cold-open sequence.

---

## 3. Art direction

Semi-3D corporate cartoon — clean vector illustration, soft gradient lighting, rounded forms. Generic international corporate setting: business suits, glass-tower offices, no regional signalling in the environments.

**Characters** are generated as full-body, three-quarter-turn figures on transparent backgrounds so they can be composited over any environment and animated independently. **Backgrounds** are generated empty at 16:9 so characters never fight with baked-in figures.

### Content/art alignment

The regulatory content is Pakistani — PKR amounts, SBP thresholds, NADRA verification, FMU reporting, and customer names like "Bilal Ahmed" and "Rehan Textiles (Pvt) Ltd". The art direction chosen is generic international corporate.

**Resolution:** the environments stay generic international (glass towers, modern branch interiors — these read as any major city). The customer cast is generated as an **internationally diverse** set of faces, which accommodates the existing South Asian customer names without either changing the content or making the art look mismatched. No content strings change.

### Character assets (10 files)

| File | Character | Role | Description |
|---|---|---|---|
| `elena-explain.png` | Elena Vance | Head of Financial Crime Compliance — the mentor | Magenta blazer, white trousers, dark hair up. Open, explaining posture, gesturing. |
| `elena-concern.png` | Elena Vance | same | Same character and outfit, arms folded, serious expression. |
| `marcus-neutral.png` | Marcus Hale | Senior AML Analyst — the peer | Teal suit, beard. Relaxed standing pose. |
| `marcus-alarm.png` | Marcus Hale | same | Same character, concerned expression, hand raised. |
| `cust-trader.png` | — | Cash-heavy trader | Middle-aged man, open collar, holding a document case. Uneasy. |
| `cust-elder.png` | — | Elderly woman | Dignified, handbag, cardigan. |
| `cust-student.png` | — | Young student | Casual, backpack, early twenties. |
| `cust-pep.png` | — | Politician (PEP) | Polished, expensive suit, lapel pin, confident. |
| `cust-ngo.png` | — | Charity/NGO director | Smart-casual, lanyard, earnest. |
| `cust-foreign.png` | — | Foreign businessman | Sharp suit, carrying a passport folder. |

Elena and Marcus must be recognisably the same person across their two expressions — this is the main generation risk and is handled by passing the first image as a reference when generating the second.

### Background assets (5 files, 16:9)

| File | Used by | Description |
|---|---|---|
| `bg-skyline.png` | Cold open, home | Bright daylight glass-tower financial district, soft clouds. |
| `bg-branch.png` | Module 01 (Onboarding) | Modern sunlit bank branch interior, teller counter, empty. |
| `bg-opsfloor.png` | Modules 02, 03 | Bright compliance monitoring room, wall of screens, daylight windows. |
| `bg-boardroom.png` | Module 04, results | Executive boardroom, large windows onto a daylight skyline. |
| `bg-hall.png` | Credential | Bright award atrium. |

All backgrounds are rendered bright/daylight to suit the light theme, including the ops floor which would conventionally be dark.

---

## 4. Theme — light

The current dark palette is replaced wholesale.

```
--page-a   #F4F9FD      page gradient start
--page-b   #E3EEF7      page gradient end
--surface  #FFFFFF      cards, panels, bubbles
--surface2 #F5F8FB      insets, secondary rows
--ink      #10202F      headings
--text     #2A3B4C      body
--muted    #6B7F92      labels, captions
--line     #DCE6EF      hairlines where a border is unavoidable
--teal     #0FA98A      primary accent / correct
--blue     #3B7DE8      category A
--violet   #8B5CF6      category C
--amber    #E39A0C      category B / partial
--coral    #E2493C      category E / incorrect
--gold     #C9962C      credential
--green    #22C55E      "Select The Most Effective Answer" pill
--grad-a   #C084FC      speech-bubble border gradient start
--grad-b   #34E0C0      speech-bubble border gradient end
--shadow   0 10px 30px -12px rgba(16,32,47,.18)
```

Depth comes from soft shadows, not borders — this is what makes the reference feel airy. Panels sitting over a background image use `rgba(255,255,255,.86)` with `backdrop-filter: blur(14px)`.

The two existing canvases need palette updates: `#fx` (ambient particles) becomes light-on-light at low opacity, and `confetti()` switches to the new accent set.

---

## 5. Cinematic layer

Five helpers, added above the existing engine section.

**`setScene(bgKey)`** — cross-fades the full-bleed background. (Named `setScene` rather than `stage` because `const stage = document.getElementById('stage')` already exists in the router.) Two stacked `<img>` layers; the incoming one fades in over 600ms, then the outgoing is removed. Also applies a bottom scrim so text over the image stays readable. Because `go()` replaces `#stage`'s innerHTML on every screen change, the background and actor layers live in their own containers **outside** `#stage` so they survive routing and can cross-fade independently.

**`actor(id, side, mood)`** — mounts a character PNG anchored to the bottom-left or bottom-right, slides it in from off-screen over 450ms, and applies a slow idle float (`translateY` ±6px, 4s ease-in-out, infinite). Calling it again with a different `mood` swaps the image with a 200ms cross-fade so expression changes read as reactions. Returns a handle with `.exit()`.

**`say(actorHandle, text, opts)`** — renders a speech bubble card near the actor and types the text in at roughly 22ms per character, skippable on click. Returns a Promise that resolves when typing completes, so briefing sequences are written as sequential `await`s. The bubble is a white card with the magenta→mint gradient border from the reference.

**`choices(items)`** — renders the answer list: a circular icon plus text per row, white frosted card, hover lift, teal glow on selection. Rows fade in staggered at 60ms intervals. Returns a Promise resolving to the chosen index. Keyboard number selection is preserved by routing through the existing `numberKeys` helper.

**`brief(m, bgKey, artKey, name, lines)`** — composes the four helpers above into the pre-module briefing: sets the scene, brings the mentor on, types each line in sequence, then shows a Start button. Returns a Promise that resolves when the user starts, so each module opens with `brief(...).then(() => { ...mount actors...; draw(); })`. One shared helper rather than four near-identical sequences.

An `ART` registry maps asset keys to `assets/` paths in one place, so the dev team can swap in final art without hunting through the file.

---

## 6. Screen flow

**Cold open** — first load only, gated on a new `S.seenIntro` flag, skippable via a persistent Skip button. The flag is added to the default `S` object; because `load()` does `Object.assign(S, JSON.parse(r))`, existing saved progress deserialises without the key and correctly defaults to unseen. Title card over `bg-skyline` with a slow scale-up, then Elena enters right and delivers the existing headline copy ("You are the last control before the money moves"), then Marcus enters left with a second line, then a BEGIN button.

**Home / Day map** — `bg-skyline`, Elena standing right, the four missions presented as Day 1–4 nodes carrying their existing lock and completion state. Rank chip and XP bar move into the top bar over the image.

**Module briefing** — before each mission, `brief()` cross-fades to that module's background, brings the mentor on, types two briefing lines, then shows a START button. This is where the story frame lives, and it costs one call per module.

**Scenario stage** — the core screen and the one the reference screenshots define. Full-bleed background with scrim; character anchored bottom-left or bottom-right with idle float; speech bubble card above with typed text; countdown ring top-left driven by the existing timer logic; the green "Select The Most Effective Answer" pill on the left; answer rows on the right; NEXT bottom-right.

**Feedback** — the chosen row turns teal, amber, or coral. The mentor cuts in with a reaction bubble whose mood matches the outcome (`elena-explain` on correct, `elena-concern` on incorrect). Correct answers fire the existing XP burst and confetti.

**Results** — the existing category breakdown and grade, staged over `bg-boardroom` with Elena presenting beside it.

**Credential** — the existing certificate over `bg-hall`.

### Per-module mapping

| Module | Background | Actors |
|---|---|---|
| 01 Customer Onboarding | `bg-branch` | Customer opposite (rotating from the six), Elena for hints and feedback |
| 02 Red-Flag Radar | `bg-opsfloor` | Marcus presenting; timer ring is the dominant element |
| 03 Review Console | `bg-opsfloor` | A customer portrait per case, Elena for feedback |
| 04 Threshold Trainer | `bg-boardroom` | Elena rapid-firing drills |

Module 03's cases each name a fixed customer from the `CUSTOMERS` table, so each is mapped onto one of the six portraits by hashing its existing `seed`. Module 04 generates drills procedurally from `TT_NAMES` and shows no portrait at all — it presents a transaction gauge, not a person, so there is nothing to illustrate.

This leaves `avatar()`, `radarSVG()` and `artBankVault()` with no callers. All three stay defined: they are the working hand-built SVG fallbacks for any content added later that has no illustration asset, and the dev brief records that they are deliberate rather than leftovers.

---

## 7. File structure

```
Anti Money Laundering/
  aml-compliance-academy.html     edited in place
  assets/
    elena-explain.png  elena-concern.png
    marcus-neutral.png marcus-alarm.png
    cust-*.png  (6)
    bg-*.png    (5)
```

The file stays single-HTML for portability, consistent with the existing dev brief, but now depends on a sibling `assets/` folder. This means it must be served or opened from its own directory rather than moved as a lone file — an acceptable trade for the visual gain, and noted for the dev team.

`aml-transaction-simulator.html` is not touched. It is a superseded earlier prototype of what is now Module 03.

---

## 8. Risks

**Character consistency across expressions.** Two images of the same person may not match. Mitigated by reference-image chaining; if a pair still diverges, the fallback is to ship one expression per character and convey mood through the bubble border colour instead.

**Text legibility over photographic backgrounds.** Mitigated by the bottom scrim in `stage()` and frosted panels; every text surface sits on a `rgba(255,255,255,.86)` backdrop, never directly on the image.

**File growth.** The file is already ~2,100 lines and this adds a CSS block plus roughly 150 lines of helpers, while the mission functions grow as they gain `await`ed staging. If it becomes unwieldy the natural split is `engine.js` / `cinematic.js` / `content.js`, but that breaks the single-file property and is out of scope here.

**Pacing.** Typed text and staged entrances add real seconds. Every animated beat must be skippable on click, and the whole cold open skippable outright, or repeat playthroughs become tedious.

---

## 9. Success criteria

- A first-time viewer, shown the home screen and one scenario, reads it as a game rather than a training form.
- All four modules, scoring, ranks, badges, and persistence behave identically to before the re-skin.
- Every animated beat can be skipped; the cold open never plays twice.
- No regulatory content string is altered.
