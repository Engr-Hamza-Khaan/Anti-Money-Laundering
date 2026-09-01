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

### Task 10: Module 03 — review console

**Files:**

- Modify: `aml-compliance-academy.html:1677-1845` (`missionConsole`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `custArt`, `clearActors`.

This module's dossier-and-case layout is its point — a two-panel review console is what an analyst actually looks at. The re-skin gives it a scene and a face, and leaves the console intact.

- [ ] **Step 1: Open with Elena's briefing**

Replace the trailing `draw();` at the end of `missionConsole()` with:

```js
  brief(m, 'bg-opsfloor', 'elena-explain', 'Elena Vance', [
    'This is the live queue. Every case in it is a real transaction waiting on a disposition from you: clear it, flag it, or escalate it.',
    'Flagging is not enough on its own. You have to name the indicator you are acting on, because an STR has to record the basis for the decision \u2014 and so does a decision not to file one.'
  ]).then(()=>{
    clearActors();
    setScene('bg-opsfloor');
    draw();
  });
```

- [ ] **Step 2: Put the customer on stage per case**

In `draw()`, after `const cust = CUSTOMERS[c.cust];` (line 1684), add:

```js
    actor(custArt(cust.seed), 'left', {id:'cust'});
```

Because `actor()` returns the existing handle and cross-fades when called again with the same `id`, moving from case to case swaps the portrait rather than stacking figures.

- [ ] **Step 3: Remove the duplicated avatar from the dossier**

The dossier now duplicates the on-stage figure. Delete the avatar block (lines 1705–1707):

```js
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--border);display:flex;justify-content:center">
            <div style="width:88px">${avatar(cust.seed,'neutral')}</div>
          </div>
```

This removal leaves `avatar()` with no remaining callers anywhere in the file — module 01 dropped its use in Task 8 and module 04 never used it. **Leave the function defined.** It is the documented fallback for any future case whose customer has no dedicated portrait, and deleting it would force the dev team to rewrite it. The same applies to `radarSVG()` (unused after Task 9) and `artBankVault()` (unused after Task 7) — all three become dead code by design and are recorded as such in Task 13's dev-brief update.

- [ ] **Step 4: Shift the console clear of the character**

Change the `.con-wrap` opening tag to `<div class="con-wrap" style="max-width:min(100%,880px);margin-left:auto">`.

- [ ] **Step 5: Add a mentor reaction on decision**

Inside `function resolve(a)` (line 1769), the correctness flag is `const ok = a === c.correct;` on line 1771. Locate the stamp block (lines 1805–1808) and add the actor call immediately after `beep(ok?'good':'bad');`:

```js
      actor(ok ? 'elena-explain' : 'elena-concern', 'right', {id:'mentor'});
```

- [ ] **Step 6: Restyle the next button**

In `resolve()`, the feedback slot's button on line 1817 is `<button class="btn primary wide" id="nextbtn" style="margin-top:14px">`. Replace that line with the right-aligned `.cnext` form used in Task 8 Step 6:

```js
        <div style="display:flex;margin-top:14px"><button class="cnext" id="nextbtn">${i+1>=CASES.length?'See assessment':'Next case'} ${icon('arrow')}</button></div>`;
```

- [ ] **Step 7: Clean up on exit**

Add `clearActors();` at the top of this module's `finish()` (line 1824).

- [ ] **Step 8: Verify module 03**

Play through several cases. You must observe:

1. Elena briefs you over the ops floor first, then leaves; a customer portrait stands on the left, changing between cases.
2. Only one figure is ever on the left — portraits swap, they do not stack.
3. The dossier, thermometer, amount, detail rows, narrative, three action buttons and the justification chips all still work.
4. The stamp animation still fires.
5. Elena appears on the right reacting to each decision.
6. The by-category breakdown and XP are unchanged.

- [ ] **Step 9: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: stage review console with customer portraits"
```

---


