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

### Task 11: Module 04 — threshold trainer

**Files:**

- Modify: `aml-compliance-academy.html:1906-2005` (`missionThresholds`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `choices`, `ringHTML`, `ringSet`, `clearActors`.

- [ ] **Step 1: Declare the actor handle**

After `const perKind = {};` (line 1912), add:

```js
  let elenaA = null;
```

- [ ] **Step 2: Swap the timer bar for the ring and restage the panel**

Replace the `timerbar` div and the `.tt-wrap` block (lines 1924–1942) with:

```js
      <div class="panel" style="max-width:min(100%,720px)">
        <div style="display:flex;align-items:center;gap:18px;margin-bottom:14px">
          ${ringHTML('tring')}
          <div class="tt-ctx" style="flex:1;margin:0">
            <div class="who">${tx.who} \u00b7 ${tx.type}</div>
            <div class="note">${tx.note}</div>
          </div>
        </div>
        <div class="gauge">${gaugeSVG(tx.amount, tx.cash)}</div>
        <div style="font-size:11px;color:var(--muted);text-align:center;margin-bottom:14px;line-height:1.6">
          Name the <b style="color:var(--ink)">primary</b> obligation. Where more than one could apply the higher duty wins:
          STR &rsaquo; EDD &rsaquo; CTR &rsaquo; verify &rsaquo; none.
        </div>
        <div id="choiceslot"></div>
        <div id="fbslot"></div>
      </div>
```

Note the panel is left-aligned here because Elena stands on the right in this module.

- [ ] **Step 3: Render the options through** `choices`

Replace the tail of `draw()` from `bindBack();` through the `#opts .opt` binding (lines 1943–1957) with:

```js
    bindBack();
    ringSet('tring', 1, LIMIT);
    choices(TT_OPTIONS.map(o=>({t:`<b style="color:var(--ink)">${o.n}</b> \u2014 ${o.d}`})),
            {prompt:'Name the primary obligation.'})
      .then(ix=>{ const o = TT_OPTIONS[ix];
                  pick(o.k, document.querySelector(`#crows .crow[data-i="${ix}"]`)); });

    const t = setInterval(()=>{
      left -= 0.1;
      ringSet('tring', left/LIMIT, left);
      if (left <= 0){ clearInterval(t); if (!locked) pick(null); }
    }, 100);
    activeTimers.push(t);
```

- [ ] **Step 4: Update** `pick()` **to the new row classes**

Replace the `#opts .opt` loop (lines 1971–1976):

```js
      document.querySelectorAll('#crows .crow').forEach((el,ix)=>{
        el.disabled = true;
        el.onclick = null;
        if (TT_OPTIONS[ix].k === ans.k) el.classList.add('good');
        else if (el === btn) el.classList.add('bad');
        else el.classList.add('faded');
      });
      elenaA.mood(ok ? 'elena-explain' : 'elena-concern');
```

- [ ] **Step 5: Restyle the next button and clean up**

Change the `#fbslot` button (line 1984) to the `.cnext` form with the right-aligned wrapper, as in Task 8 Step 6. Add `clearActors();` at the top of `finish()`.

- [ ] **Step 6: Open with Elena's briefing**

Replace the trailing `draw();` at the end of `missionThresholds()` with:

```js
  brief(m, 'bg-boardroom', 'elena-explain', 'Elena Vance', [
    'Thresholds are the part you cannot look up mid-conversation. Two million rupees in cash triggers a CTR whether or not anything looks wrong. Five hundred thousand from a walk-in triggers identity verification. An STR has no floor at all.',
    'Twelve drills, twenty-two seconds each. Where more than one obligation could apply, the higher duty wins.'
  ]).then(()=>{
    clearActors();
    setScene('bg-boardroom');
    elenaA = actor('elena-explain','right',{id:'mentor'});
    draw();
  });
```

- [ ] **Step 7: Verify module 04**

Play through several drills. You must observe:

1. Elena briefs you over the boardroom first, then stays on the right for the drills.
2. The ring counts down from `0:22` and turns coral near the end.
3. The five obligation options render as rows with the obligation name bolded before its description; number keys still select.
4. The gauge still renders and the streak still counts.
5. Timeout still scores as a miss.
6. The by-obligation-type breakdown is unchanged.

- [ ] **Step 8: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: restage threshold trainer with countdown ring"
```

---


