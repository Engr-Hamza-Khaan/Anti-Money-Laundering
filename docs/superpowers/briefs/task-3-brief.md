## Global Constraints

- **No regulatory content string may change.** `RULES`, `CATS`, `FLAGS`, `GLOSSARY`, `CDD_STEPS`, `DIALOGUE`, `CUSTOMERS`, `CASES`, `TT_OPTIONS`, `TT_NAMES`, `TT_NOTE`, `ACTION_LABELS`, `resolveObligation`, `makeDrill` are read-only for this plan.
- **No scoring or progression change.** `RANKS`, `BADGES`, `MISSIONS`, `KEY`, `S`, `load`, `save`, `rankOf`, `nextRank`, `awardXP`, `awardBadge`, `grade`, `shuffle` are read-only, with the single exception of adding `seenIntro:false` to the `S` default object.
- **Helper name is** `setScene`**, not** `stage`**.** `const stage = document.getElementById('stage')` already exists at line 1263. Using `stage` for the background helper shadows the router's element reference and breaks every screen.
- **Exact light palette** — use these values verbatim, no substitutions:
`--page-a #F4F9FD` · `--page-b #E3EEF7` · `--surface #FFFFFF` · `--surface2 #F5F8FB` · `--ink #10202F` · `--text #2A3B4C` · `--muted #6B7F92` · `--line #DCE6EF` · `--teal #0FA98A` · `--blue #3B7DE8` · `--violet #8B5CF6` · `--amber #E39A0C` · `--coral #E2493C` · `--gold #C9962C` · `--green #22C55E` · `--grad-a #C084FC` · `--grad-b #34E0C0` · `--shadow 0 10px 30px -12px rgba(16,32,47,.18)`
- **Every animated beat must be skippable on click**, and the cold open must never replay once `S.seenIntro` is true.
- **Characters are transparent-background PNGs; backgrounds are 16:9 with no people in them.**
- `aml-transaction-simulator.html` is not touched.




---

### Task 3: Light theme conversion

**Files:**

- Modify: `aml-compliance-academy.html:11-31` (the `:root` block) and the CSS rules through line 424 that reference dark-only values.

**Interfaces:**

- Produces: the CSS custom properties consumed by every later task.

This task changes only colour, shadow and border treatment. **No layout, no sizing, no structural CSS changes** — those come per-module later. Keeping this task purely chromatic is what makes it independently reviewable.

- [ ] **Step 1: Replace the** `:root` **block**

Replace lines 11–31 with:

```css
:root{
  --page-a:#F4F9FD;
  --page-b:#E3EEF7;
  --surface:#FFFFFF;
  --surface2:#F5F8FB;
  --line:#DCE6EF;
  --ink:#10202F;
  --text:#2A3B4C;
  --muted:#6B7F92;
  --teal:#0FA98A;
  --blue:#3B7DE8;
  --amber:#E39A0C;
  --coral:#E2493C;
  --violet:#8B5CF6;
  --gold:#C9962C;
  --green:#22C55E;
  --grad-a:#C084FC;
  --grad-b:#34E0C0;
  --shadow:0 10px 30px -12px rgba(16,32,47,.18);
  --shadow-lg:0 22px 50px -20px rgba(16,32,47,.28);
  --mono:'IBM Plex Mono',ui-monospace,monospace;
  --sans:'IBM Plex Sans',system-ui,sans-serif;
  --r:12px;

  /* legacy aliases — the existing rules below still reference these names.
     Mapping them here converts the whole sheet without touching every rule. */
  --bg:var(--page-a);
  --bg2:var(--page-b);
  --panel:var(--surface);
  --panel2:var(--surface2);
  --panel3:#E9F0F7;
  --border:var(--line);
  --border2:#C6D5E4;
  --dim:#8FA1B3;
}
```

The legacy alias block is deliberate: `--panel`, `--border`, `--dim` and friends are referenced by roughly a hundred rules further down. Aliasing them converts the sheet in one edit instead of a hundred, and later tasks that rewrite a section can drop to the new names naturally.

- [ ] **Step 2: Convert the page background and body text**

Replace the `body` rule (line 34–40):

```css
body{
  background:linear-gradient(160deg,var(--page-a) 0%,var(--page-b) 100%);
  background-attachment:fixed;
  color:var(--text);
  font-family:var(--sans);
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
```

- [ ] **Step 3: Convert the top bar**

In the `.topbar` rule (lines 46–52), replace `background:rgba(7,11,17,.82)` with `background:rgba(255,255,255,.78)`, and replace `border-bottom:1px solid var(--border)` with `border-bottom:1px solid var(--line); box-shadow:0 4px 20px -14px rgba(16,32,47,.35)`.

- [ ] **Step 4: Convert headings to ink**

Add immediately after the `body` rule:

```css
h1,h2,h3,h4{color:var(--ink)}
```

- [ ] **Step 5: Convert shadows from dark-drop to soft-lift**

Three rules use black drop shadows tuned for a dark page. Replace each shadow value:

- `.mcard:hover` (line 120): `box-shadow:0 16px 40px -18px rgba(0,0,0,.85)` → `box-shadow:var(--shadow-lg)`
- `.toast` (line ~411): `box-shadow:0 14px 34px -14px rgba(0,0,0,.9)` → `box-shadow:var(--shadow-lg)`
- `.persona .av` (line 170): `filter:drop-shadow(0 12px 24px rgba(0,0,0,.5))` → `filter:drop-shadow(0 12px 24px rgba(16,32,47,.22))`

- [ ] **Step 6: Give cards lift instead of outline**

Add after the `.panel` rule (line 148):

```css
.panel,.mcard,.stat,.hudpill,.rankchip,.iconbtn{box-shadow:var(--shadow)}
.stat{background:var(--surface)}
```

- [ ] **Step 7: Fix the primary button contrast**

`.btn.primary` (line 141) sets `color:#04140F` — near-black text, which was correct on the old bright teal but is now low-contrast on the darker `--teal`. Replace the rule:

```css
.btn.primary{background:linear-gradient(135deg,var(--teal),#0B8F74);color:#FFFFFF;border-color:transparent;box-shadow:var(--shadow)}
```

- [ ] **Step 8: Convert the hero gradient**

Replace the `.hero` background (line 83) with `background:linear-gradient(135deg,#FFFFFF 0%,#F3F8FD 60%,#EAF3FB 100%)` and its border with `border:1px solid var(--line)`. In `.hero::after`, raise both radial-gradient alphas from `.14`/`.12` to `.20`/`.16` so the accent glow still reads on white.

- [ ] **Step 9: Convert the certificate**

In `.cert` (line 392) replace `background:linear-gradient(150deg,#0F1A24,#0A121A)` with `background:linear-gradient(150deg,#FFFDF6,#FFF8E8)`.

- [ ] **Step 10: Verify the theme**

Open `aml-compliance-academy.html` in a browser and walk every screen: home, then each of the four modules through at least two questions and into its results screen, then the Reference Vault (flip a card), then complete enough to reach the credential — or temporarily set `S.best` in the console to unlock it.

You must observe:

1. No white-on-white or dark-on-dark text anywhere. Every string is readable.
2. Cards read as raised white surfaces, not outlined boxes.
3. Correct/partial/incorrect verdict colours are still clearly distinguishable from each other.
4. All four modules still function — timers run, answers register, scores compute.

- [ ] **Step 11: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: convert academy to light theme"
```

---


