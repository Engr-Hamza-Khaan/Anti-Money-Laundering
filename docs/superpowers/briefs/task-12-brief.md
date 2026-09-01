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

### Task 12: Results, vault and credential

**Files:**

- Modify: `aml-compliance-academy.html:1392-1432` (`results`), `:2010-2050` (`screenVault`), `:2055-2094` (`screenCertificate`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `clearActors`.

- [ ] **Step 1: Stage the results screen**

In `results()`, after `setKeys(null);` (line 1393), add:

```js
  clearActors();
  setScene('bg-boardroom');
  actor(pctIsGood(o) ? 'elena-explain' : 'elena-concern', 'right', {id:'mentor'});
```

and define the helper immediately above `function results(o){`:

```js
const pctIsGood = o => Math.round(o.pct) >= 70;
```

- [ ] **Step 2: Shift the results panel clear of Elena**

Change the results `<div class="panel">` (line 1406) to `<div class="panel" style="max-width:min(100%,760px)">`.

- [ ] **Step 3: Restyle the results actions**

Change the "Run it again" button (line 1423) from `class="btn primary"` to `class="cnext"`.

- [ ] **Step 4: Stage the vault**

In `screenVault()`, after `setKeys(null);` (line 2011), add:

```js
  clearActors();
  setScene(null);
```

The vault is a reference document, not a scene. Clearing the background returns it to the plain light theme where dense text is easiest to read.

- [ ] **Step 5: Stage the credential**

In `screenCertificate(avg)`, after `setKeys(null);` (line 2056), add:

```js
  clearActors();
  setScene('bg-hall');
  actor('elena-explain','left',{id:'mentor'});
  actor('marcus-neutral','right',{id:'peer'});
```

- [ ] **Step 6: Keep the print stylesheet correct**

The credential's print block (lines 2061–2065) hides chrome for PDF export but does not know about the new layers. Add `#cine,#actors,.skipbtn` to its `display:none!important` selector list:

```css
body{background:#fff}#fx,#confetti,#cine,#actors,.skipbtn,.topbar,.res-actions,#toasts,.mhead{display:none!important}
```

- [ ] **Step 7: Verify**

You must observe:

1. Finishing any module lands on a boardroom-staged results screen with Elena reacting to the grade — explaining pose at 70% or above, concerned below.
2. The score, grade, XP gain and category breakdown are unchanged.
3. Opening the Reference Vault clears the background and characters entirely; cards still flip and the seen-counter still increments.
4. The credential screen shows the atrium with Elena and Marcus flanking the certificate.
5. Print preview on the credential (Ctrl+P) shows the certificate on white with no background image, no characters and no chrome.

- [ ] **Step 8: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: stage results, vault and credential screens"
```

---


