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

### Task 9: Module 02 — red-flag radar

**Files:**

- Modify: `aml-compliance-academy.html:1566-1672` (`missionRadar`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `choices`, `ringHTML`, `ringSet`, `clearActors`.

- [ ] **Step 1: Declare the actor handle**

After `const perCat = {}; …` (line 1572), add:

```js
  let marcusA = null;
```

- [ ] **Step 2: Swap the timer bar for the countdown ring**

In `draw()`, replace `<div class="timerbar" id="tbar"><i style="width:100%"></i></div>` (line 1582) with a ring placed beside the observation. Replace the `.radar-wrap` block (lines 1583–1605) with:

```js
      <div class="panel" style="max-width:min(100%,780px);margin-left:auto">
        <div style="display:flex;align-items:center;gap:18px;margin-bottom:16px">
          ${ringHTML('tring')}
          <div class="flagcard" style="flex:1;margin:0">
            <div class="obs">Observation ${String(i+1).padStart(2,'0')}</div>
            <div class="txt">${f.t}</div>
          </div>
        </div>
        <div id="choiceslot"></div>
        <div id="fbslot"></div>
      </div>
```

The decorative `radarSVG()` and the `.wm` watermark are dropped — the watermark printed the answer category as a background flourish, and the ops-floor screen wall behind the panel now supplies the atmosphere the radar graphic was providing. `radarSVG()` remains defined but unused; leave it for the dev team.

- [ ] **Step 3: Render the categories through** `choices`

Replace the tail of `draw()` from `bindBack();` through the `document.querySelectorAll('#cats .catbtn')` binding (lines 1606–1622) with:

```js
    bindBack();
    ringSet('tring', 1, LIMIT);
    choices(catKeys.map((k,ix)=>({t:CATS[k].name, ic:k})), {prompt:'Which red-flag family is this?'})
      .then(ix=>{ const k = catKeys[ix]; pick(k, document.querySelector(`#crows .crow[data-i="${ix}"]`)); });

    const t = setInterval(()=>{
      left -= 0.1;
      ringSet('tring', left/LIMIT, left);
      if (left <= 0){ clearInterval(t); if (!locked) pick(null); }
    }, 100);
    activeTimers.push(t);
```

The category letter goes in the row's circular icon, matching how the reference screenshots put a glyph in each option's circle.

- [ ] **Step 4: Update** `pick()` **to the new row classes**

In `pick()`, replace the `#cats .catbtn` loop (lines 1635–1640):

```js
      document.querySelectorAll('#crows .crow').forEach((el,ix)=>{
        el.disabled = true;
        el.onclick = null;
        if (catKeys[ix] === f.c) el.classList.add('good');
        else if (el === btn) el.classList.add('bad');
        else el.classList.add('faded');
      });
      marcusA.mood(ok ? 'marcus-neutral' : 'marcus-alarm');
```

- [ ] **Step 5: Restyle the next button and clean up**

In `pick()`, change the button in `#fbslot` (line 1650) to the `.cnext` form used in Task 8 Step 6, with the same right-aligned wrapper. Add `clearActors();` at the top of `finish()`.

- [ ] **Step 6: Open with Marcus's briefing**

Replace the trailing `draw();` at the end of `missionRadar()` with:

```js
  brief(m, 'bg-opsfloor', 'marcus-neutral', 'Marcus Hale', [
    'Five red-flag families, A through E, straight out of Annexure-II. If you cannot name the family an observation belongs to, you cannot reach for the right follow-up question.',
    'Ten observations, eighteen seconds each. Answer fast and the combo multiplier stays alive.'
  ]).then(()=>{
    clearActors();
    setScene('bg-opsfloor');
    marcusA = actor('marcus-neutral','left',{id:'mentor'});
    draw();
  });
```

- [ ] **Step 7: Verify module 02**

Play the module through several rounds. You must observe:

1. Marcus briefs you over the ops floor first, then moves to the left when you start.
2. A circular countdown ring sits beside the observation, ticking down from `0:18` and turning coral in the last few seconds.
3. The five families render as rows with their letter in the circle; number keys still select.
4. Letting the timer expire auto-answers as a miss, exactly as before.
5. The combo counter, per-category breakdown and XP still compute identically.
6. Marcus switches to the alarmed pose on a wrong answer.

- [ ] **Step 8: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: restage red-flag radar with countdown ring"
```

---


