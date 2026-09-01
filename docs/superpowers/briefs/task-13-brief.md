## Global Constraints

- **No regulatory content string may change.** `RULES`, `CATS`, `FLAGS`, `GLOSSARY`, `CDD_STEPS`, `DIALOGUE`, `CUSTOMERS`, `CASES`, `TT_OPTIONS`, `TT_NAMES`, `TT_NOTE`, `ACTION_LABELS`, `resolveObligation`, `makeDrill` are read-only for this plan.
- **No scoring or progression change.** `RANKS`, `BADGES`, `MISSIONS`, `KEY`, `S`, `load`, `save`, `rankOf`, `nextRank`, `awardXP`, `awardBadge`, `grade`, `shuffle` are read-only, with the single exception of adding `seenIntro:false` to the `S` default object.
- **Colour fields are the one exception to the two rules above.** The `color:` field in `CATS`, the `c:` field in `MISSIONS`, and the hex literals inside the SVG generator functions are presentation, not content or logic, and Task 3b retunes them for the light theme. Every other field — names, definitions, thresholds, ids, icons, scoring — stays frozen. If a change would alter what a screen *says* or how it *scores*, it is out of bounds; if it only alters what colour something is drawn in, it is in bounds.
- **Helper name is** `setScene`**, not** `stage`**.** `const stage = document.getElementById('stage')` already exists at line 1263. Using `stage` for the background helper shadows the router's element reference and breaks every screen.
- **Exact light palette** — use these values verbatim, no substitutions:
`--page-a #F4F9FD` · `--page-b #E3EEF7` · `--surface #FFFFFF` · `--surface2 #F5F8FB` · `--ink #10202F` · `--text #2A3B4C` · `--muted #6B7F92` · `--line #DCE6EF` · `--teal #0FA98A` · `--blue #3B7DE8` · `--violet #8B5CF6` · `--amber #E39A0C` · `--coral #E2493C` · `--gold #C9962C` · `--green #22C55E` · `--grad-a #C084FC` · `--grad-b #34E0C0` · `--shadow 0 10px 30px -12px rgba(16,32,47,.18)`
- **Every animated beat must be skippable on click**, and the cold open must never replay once `S.seenIntro` is true.
- **Characters are transparent-background PNGs; backgrounds are 16:9 with no people in them.**
- `aml-transaction-simulator.html` is not touched.




---

### Task 13: Final pass — effects, docs, regression

**Files:**

- Modify: `aml-compliance-academy.html` — the `#fx` canvas rule, `confetti()` (line 1118), the footer note (line 1369)
- Modify: `Dev-Team-Brief-AML-Simulator.md`

- [ ] **Step 1: Retune the ambient canvas for a light page**

The `ambient()` IIFE floats teal dots and faint currency glyphs upward. Its colours were chosen against a near-black page and will read as grey dirt on white.

Change the `#fx` rule (line 41) from `opacity:.55` to `opacity:.5`.

In `frame()`, change the dot colour (line 1100) from `ctx.fillStyle = '#2BD9B0';` to:

```js
    ctx.fillStyle = '#3B7DE8';
```

and the glyph colour (line 1108) from `ctx.fillStyle = '#4C8DF6';` to:

```js
      ctx.globalAlpha = g.a * 2.2; ctx.font = g.s+'px IBM Plex Mono, monospace'; ctx.fillStyle = '#8B5CF6';
```

The glyph alpha is multiplied because `build()` assigns `a:Math.random()*.05+.02` — alphas between 0.02 and 0.07, which are invisible against a light background.

If the effect still reads as dirt after this, set the `#fx` rule to `opacity:0` and record it in the dev brief rather than spending further time tuning it.

- [ ] **Step 2: Retune confetti to the new palette**

In `confetti()`, replace the colour array on line 1121 — it is named `cols`:

```js
  const cols = ['#0FA98A','#3B7DE8','#8B5CF6','#E39A0C','#C084FC','#34E0C0'];
```

- [ ] **Step 3: Update the footer note**

The keyboard tip on line 1372 still reads correctly, but the note should mention the asset dependency. Append to the note block:

```html
<br>This build loads illustration assets from the <span class="kbd">assets/</span> folder beside this file \u2014 keep them together.
```

- [ ] **Step 4: Update the dev brief**

In `Dev-Team-Brief-AML-Simulator.md`, add a section recording what changed, so the dev team is not surprised:

```markdown
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
```

- [ ] **Step 5: Full regression pass**

With `localStorage` cleared, play the entire application start to finish: cold open, home, all four modules briefing-to-completion, the vault with every card flipped, and the credential. You must observe:

1. No console errors at any point.
2. No screen where a character overlaps unreadable text.
3. Every timer, score, badge award, toast and rank promotion fires as before.
4. Backgrounds cross-fade between screens rather than flashing white.
5. No character is ever left on screen from a previous module or briefing.
6. Every module opens with its mentor briefing, and clicking a typing bubble completes it instantly.
7. Leaving a module mid-briefing via the "Academy" back button returns home cleanly with no actors left behind.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: retune effects for light theme and document the re-skin"
```

---


