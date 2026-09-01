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

### Task 7: Home screen as day map

**Files:**

- Modify: `aml-compliance-academy.html:1314-1387` (`home`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `clearActors` from Task 5.

- [ ] **Step 1: Stage the scene at the top of** `home()`

Immediately after `setKeys(null);` in `home()` (line 1315), add:

```js
  clearActors();
  setScene('bg-skyline');
  actor('elena-explain','right');
```

- [ ] **Step 2: Drop the hero's SVG art panel**

The hero currently reserves a 330px column for `artBankVault()`, which now competes with Elena standing in the same place. In the `home()` template literal, change the hero opening tag to `<div class="hero" style="grid-template-columns:1fr">` and delete the `<div class="hero-art">${artBankVault()}</div>` line (line 1334).

`artBankVault()` stays defined — Task 12 reuses it on the credential screen.

- [ ] **Step 3: Constrain the hero width so Elena is not covered**

Add `max-width:min(100%,720px)` to the same inline style on the hero.

- [ ] **Step 4: Relabel the mission cards as days**

In the `.mgrid` map (line 1341), replace `<div class="mk">${m.k}</div>` with:

```js
<div class="mk">${m.id==='vault' ? m.k : 'Day ' + (MISSIONS.filter(x=>x.id!=='vault').findIndex(x=>x.id===m.id) + 1) + ' \u00b7 ' + m.k}</div>
```

- [ ] **Step 5: Verify the home screen**

Reload. You must observe:

1. The skyline sits behind the page and Elena stands on the right, floating gently.
2. The hero panel is a frosted white card that does not overlap Elena on a desktop-width window.
3. The four scored modules read "Day 1 · …" through "Day 4 · …"; the Reference Vault keeps its own label.
4. Clicking a module still opens it; clicking the SENTINEL brand returns home and Elena is still there.
5. Narrow the window below 900px — Elena fades back to 35% opacity and the layout stays readable.

- [ ] **Step 6: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: stage home screen as day map"
```

---


