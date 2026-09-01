# SENTINEL Cinematic Re-skin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-skin `aml-compliance-academy.html` from a dark compliance dashboard into a bright, character-driven situational-judgement game matching The Talent Games' C-Factor, without altering any regulatory content or scoring logic.

**Architecture:** The existing engine (rule data, scoring, ranks, persistence) is untouched. A new cinematic layer — a persistent background image layer, animated character PNGs, typed speech bubbles, and a staged answer list — is added *outside* the `#stage` element so it survives the router's `innerHTML` replacement. The dark CSS palette is replaced wholesale with a light one. Each of the four mission render functions is rewritten to compose the cinematic helpers instead of emitting flat panels.

**Tech Stack:** Single-file HTML, vanilla JS (no build step, no framework, no dependencies beyond a Google Fonts link). AI-generated PNG assets in a sibling `assets/` folder.

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



## Deviations from standard plan format

This codebase has **no test framework and no test files** — it is a single browser HTML prototype. Test-first steps are therefore replaced with **explicit browser verification steps**: each states exactly what to open, what to do, and what you must observe. Treat a failed observation exactly as you would a failed assertion — stop and fix before proceeding.

Full code is given for all **new** infrastructure (palette, cinematic CSS, the five helpers, the cold open), because those must be defined exactly. For the **transformations** of existing render functions, the plan gives the exact target markup and the exact lines being replaced; the implementer reads the surrounding code in the file rather than having it duplicated here.

**There is no version control on this project, by the owner's decision.** Every step in this plan headed **"Commit"** is therefore to be **skipped** — ignore its `git` commands entirely. In its place, after a task's verification steps pass, run the backup refresh from Task 0 Step 3. The single rolling backup is the only rollback available, so a task's verification must genuinely pass before you overwrite it.

---



### Task 0: Safety net

The next thirteen tasks rewrite most of a working 2,118-line file. The owner has declined version control, so file copies are the entire safety net. Do not skip this task.

**Files:**

- Create: `_backup/aml-compliance-academy.ORIGINAL.html`
- Create: `_backup/aml-compliance-academy.LAST-GOOD.html`

- [ ] **Step 1: Create the backup folder**

```powershell
mkdir _backup
```

- [ ] **Step 2: Preserve the pristine original — never overwrite this one**

```powershell
Copy-Item "aml-compliance-academy.html" "_backup\aml-compliance-academy.ORIGINAL.html"
```

This file is the guaranteed way back to the working academy no matter how badly a later task goes. Nothing in this plan writes to it again.

- [ ] **Step 3: Create the rolling backup — this is the "commit" substitute**

```powershell
Copy-Item "aml-compliance-academy.html" "_backup\aml-compliance-academy.LAST-GOOD.html" -Force
```

**Run this exact command again at the end of every task, in place of that task's skipped Commit step, but only after its verification steps have actually passed.** To roll back a failed task, copy `LAST-GOOD` back over the working file.

- [ ] **Step 4: Verify both backups exist**

```powershell
Get-ChildItem _backup
```

Expected: two `.html` files, both the same size as `aml-compliance-academy.html`.

---



### Task 1: Character assets

**Files:**

- Create: `assets/elena-explain.png`, `assets/elena-concern.png`, `assets/marcus-neutral.png`, `assets/marcus-alarm.png`, `assets/cust-trader.png`, `assets/cust-elder.png`, `assets/cust-student.png`, `assets/cust-pep.png`, `assets/cust-ngo.png`, `assets/cust-foreign.png`
- Create: `assets/_preview.html`

**Interfaces:**

- Produces: the ten filenames above, consumed by the `ART` registry in Task 5.

**Shared style prefix.** Every character generation prompt must begin with this exact sentence so the cast looks like one production:

> "Semi-3D corporate cartoon character illustration, clean vector style with soft gradient shading and rounded forms, full body, three-quarter turn, standing, modern business setting art direction, completely transparent background, no shadow on ground, no background elements whatsoever."

- [ ] **Step 1: Create the assets folder**

```bash
mkdir assets
```

- [ ] **Step 2: Generate Elena — explaining**

Aspect ratio `3:4`, filename `elena-explain.png`. Prompt = shared style prefix + :
"A confident woman in her late thirties, Head of Financial Crime Compliance. Magenta-purple tailored blazer, white trousers, dark hair pulled up. Warm, open expression, mid-gesture with one hand raised as if explaining a point."

- [ ] **Step 3: Generate Elena — concerned, using Step 2 as reference**

Aspect ratio `3:4`, filename `elena-concern.png`, and pass `assets/elena-explain.png` in `reference_image_paths`. Prompt = shared style prefix + :
"The exact same woman as the reference image — identical face, identical hairstyle, identical magenta-purple blazer and white trousers. Same character, different pose: arms folded, serious and concerned expression, brow slightly furrowed."

The reference image is what keeps it the same person. Do not skip it.

- [ ] **Step 4: Generate Marcus — neutral**

Aspect ratio `3:4`, filename `marcus-neutral.png`. Prompt = shared style prefix + :
"A man in his early thirties, senior AML analyst. Teal-green tailored suit, white shirt, dark tie, short dark hair, neatly trimmed beard. Relaxed confident standing pose, hands at his sides, calm neutral expression."

- [ ] **Step 5: Generate Marcus — alarmed, using Step 4 as reference**

Aspect ratio `3:4`, filename `marcus-alarm.png`, and pass `assets/marcus-neutral.png` in `reference_image_paths`. Prompt = shared style prefix + :
"The exact same man as the reference image — identical face, identical beard, identical teal-green suit. Same character, different pose: one hand raised in a stop gesture, alarmed and concerned expression, eyes wide."

- [ ] **Step 6: Generate the six customers**

All aspect ratio `3:4`, each prompt = shared style prefix + the description below. The cast must be **visibly diverse in ethnicity, age and build** — the training content uses South Asian customer names, so the cast should read as an international mix rather than uniformly Western.


| Filename           | Prompt suffix                                                                                                                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cust-trader.png`  | "A middle-aged South Asian man, cash-heavy wholesale trader. Open-collar shirt, no tie, slightly rumpled jacket, holding a document case against his chest. Uneasy, evasive expression, avoiding eye contact." |
| `cust-elder.png`   | "A dignified elderly woman in her seventies, silver hair, soft cardigan over a blouse, holding a handbag with both hands. Polite, patient, slightly puzzled expression."                                       |
| `cust-student.png` | "A young woman in her early twenties, university student. Casual clothes, denim jacket, backpack over one shoulder. Cheerful, slightly nervous expression."                                                    |
| `cust-pep.png`     | "A polished man in his fifties, senior politician. Expensive navy three-piece suit, silk tie, small lapel pin, greying hair. Confident, self-assured, faintly impatient expression."                           |
| `cust-ngo.png`     | "A woman in her forties, charity organisation director. Smart-casual blazer over a simple top, ID lanyard around her neck, holding a folder. Earnest, sincere expression."                                     |
| `cust-foreign.png` | "A sharply dressed East Asian businessman in his forties, dark tailored suit, holding a passport wallet and boarding documents. Brisk, businesslike, slightly hurried expression."                             |


- [ ] **Step 6b: Convert the painted checkerboard into a real alpha channel**

**The generator does not produce transparency.** Asked for a transparent background it *paints a checkerboard* — the visual convention for transparency — into an opaque RGB PNG. The result looks correct in any preview that shows a checkerboard behind images, so eyeballing it will not catch this. Composited over a background it renders as a checkered rectangle.

Confirm the problem before and after with the PNG colour-type byte (2 = RGB, no alpha; 6 = RGBA):

```powershell
Get-ChildItem assets\*.png | ForEach-Object { $b=[System.IO.File]::ReadAllBytes($_.FullName)[0..30]; $t = switch($b[25]){2{"RGB"}6{"RGBA"}default{"?"}}; "{0,-22} {1}" -f $_.Name,$t }
```

Run `tools/make_transparent.py` (pure standard library — Pillow and ImageMagick are not available here) over the ten character files only. It flood-fills inward from the border across pixels matching the checker greys and writes alpha 0 there, ramping alpha at the boundary to avoid a pale halo.

```powershell
Copy-Item assets "_backup\assets-raw" -Recurse -Force
python tools\make_transparent.py assets\elena-explain.png assets\elena-concern.png assets\marcus-neutral.png assets\marcus-alarm.png assets\cust-trader.png assets\cust-elder.png assets\cust-student.png assets\cust-pep.png assets\cust-ngo.png assets\cust-foreign.png
```

Flood-fill rather than a global colour key because half the cast wears white, cream or grey; a global key would punch holes through Elena's trousers and Marcus's shirt. For the same reason `TOL_HARD` is 12: at 26 the fill nibbled the edges of near-white trousers into a ragged outline. If a figure comes out with checker fringe still attached, raise `TOL_HARD` for that file and re-run it from `_backup\assets-raw`; if a figure loses part of a pale garment, lower it.

**Do not run this on the five backgrounds.** They are meant to stay opaque, and the script would eat any pale sky connected to the frame edge.

- [ ] **Step 7: Build a contact sheet to verify the assets**

Create `assets/_preview.html`:

```html
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Asset preview</title>
<style>
 body{background:#E3EEF7;font-family:system-ui;padding:24px;color:#10202F}
 h2{font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:#6B7F92;margin:24px 0 10px}
 .row{display:flex;flex-wrap:wrap;gap:14px}
 .c{background:repeating-conic-gradient(#fff 0 25%,#dbe6f0 0 50%) 0 0/18px 18px;
    border-radius:10px;padding:8px;text-align:center;box-shadow:0 10px 30px -12px rgba(16,32,47,.18)}
 .c img{height:210px;display:block}
 .c span{font-size:10px;color:#6B7F92;display:block;margin-top:6px}
 .bg img{width:340px;height:auto;border-radius:8px;display:block}
</style></head><body>
<h2>Characters — checkerboard shows transparency</h2><div class="row" id="ch"></div>
<h2>Backgrounds</h2><div class="row" id="bg"></div>
<script>
const CH=['elena-explain','elena-concern','marcus-neutral','marcus-alarm',
          'cust-trader','cust-elder','cust-student','cust-pep','cust-ngo','cust-foreign'];
const BG=['bg-skyline','bg-branch','bg-opsfloor','bg-boardroom','bg-hall'];
ch.innerHTML=CH.map(n=>`<div class="c"><img src="${n}.png" alt="${n}"><span>${n}</span></div>`).join('');
bg.innerHTML=BG.map(n=>`<div class="c bg"><img src="${n}.png" alt="${n}"><span>${n}</span></div>`).join('');
</script></body></html>
```

- [ ] **Step 8: Verify the characters**

Open `assets/_preview.html` in a browser. You must observe:

1. All ten character images load (no broken-image icons).
2. **On the dark strip**, no figure carries a pale outline, fringe, or rectangular patch. This strip — not the checkerboard one — is what actually proves the cut-out worked, because a *painted* checkerboard looks identical to real alpha when shown on a checkerboard.
3. **In the two composited scenes**, every silhouette edge sits cleanly on the background, with no halo and no visible checker pattern.
4. `elena-explain` and `elena-concern` are recognisably the same woman in the same outfit. Same for the two Marcus images.
5. The style is consistent across all ten — they look like one illustration set, not ten different artists.

If (2) or (3) fails for a file, re-run Step 6b on it from `_backup\assets-raw` with an adjusted `TOL_HARD`. If (4) fails, regenerate the second image with a stronger reference instruction. If (5) fails on one outlier, regenerate that one using a good image as reference.

Backgrounds will show as broken here until Task 2 — that is expected.

- [ ] **Step 9: Commit**

```bash
git add assets
git commit -m "feat: add generated character assets and contact sheet"
```

---



### Task 2: Background assets

**Files:**

- Create: `assets/bg-skyline.png`, `assets/bg-branch.png`, `assets/bg-opsfloor.png`, `assets/bg-boardroom.png`, `assets/bg-hall.png`

**Interfaces:**

- Consumes: `assets/_preview.html` from Task 1.
- Produces: the five filenames above, consumed by the `ART` registry in Task 5.

**Shared style prefix.** Every background prompt must begin with:

> "Semi-3D corporate cartoon environment illustration, clean vector style with soft gradient lighting, bright and airy daylight, wide establishing shot, completely empty with no people and no characters present, slightly soft focus in the background suitable for placing characters in front of."

- [ ] **Step 1: Generate all five backgrounds**

All aspect ratio `16:9`.


| Filename           | Prompt suffix                                                                                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bg-skyline.png`   | "A modern financial district of glass office towers under a bright blue sky with soft white clouds, green trees and a wide plaza at street level, optimistic and welcoming." |
| `bg-branch.png`    | "The interior of a modern retail bank branch, sunlit through tall windows, a clean teller counter with glass dividers, potted plants, light wood and white surfaces."        |
| `bg-opsfloor.png`  | "A bright modern compliance monitoring room, a curved wall of wide screens showing abstract dashboards and charts, light grey desks, large daylight windows along one side." |
| `bg-boardroom.png` | "A modern executive boardroom, long polished table, comfortable chairs, floor-to-ceiling windows looking out over a daylight city skyline, warm natural light."              |
| `bg-hall.png`      | "A bright modern corporate atrium, high glass ceiling, a wide staircase, plants and a subtle stage area, celebratory and open feeling."                                      |


- [ ] **Step 2: Verify the backgrounds**

Reload `assets/_preview.html`. You must observe:

1. All five load.
2. **No people appear in any of them.** A baked-in figure will collide with the character PNGs composited on top. Regenerate any that contain a person, adding "absolutely no human figures, no silhouettes of people" to the prompt.
3. Each is bright enough that dark navy text on a white frosted card will sit comfortably on top.
4. The centre-bottom of each frame is relatively uncluttered — that is where characters and the answer panel will sit.

- [ ] **Step 3: Commit**

```bash
git add assets
git commit -m "feat: add generated background assets"
```

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



### Task 3b: Recolour the JavaScript-drawn graphics

Task 3 converted the stylesheet, but roughly a third of the interface is drawn as inline SVG from JavaScript, and those functions carry their own hard-coded dark-theme hex literals. The stylesheet is now light while the instruments drawn on top of it are still painted for a dark page. The worst case is `gaugeSVG()`, which prints the transaction amount — the single most important number on the Threshold Trainer screen — in `#E9EFF5` on what is now a white panel.

Two colour tables also feed *text* colour on white cards (`.mcard .mk` and `.play` use `var(--c)`), so the old bright accents fail contrast as labels.

**Files:**

- Modify: `aml-compliance-academy.html` — `CATS` (lines 502–506), `radarSVG()` (~970–995), `thermoSVG()` (~998–1018), `gaugeSVG()` (~1021–1051), `MISSIONS` (lines 1182–1194), `screenCertificate()` (line 2084)

**Interfaces:**

- Consumes: the palette established in Task 3.
- Produces: `CATS[k].color` and `MISSIONS[i].c` values that are legible as text on white; SVG instruments that read correctly on light panels.

Use these replacements exactly. Every "to" value is from the Global Constraints palette.

| From (dark theme) | To (light theme) | Role |
| --- | --- | --- |
| `#4C8DF6` | `#3B7DE8` | blue |
| `#F2B138` | `#E39A0C` | amber |
| `#A57BFF` | `#8B5CF6` | violet |
| `#2BD9B0` | `#0FA98A` | teal |
| `#FF5F52` | `#E2493C` | coral |
| `#F5D06B` | `#C9962C` | gold |
| `#55677A`, `#7A8DA0` | `#6B7F92` | muted label text |
| `#1E2B3A` | `#DCE6EF` | instrument track / unfilled arc |
| `#22303F` | `#DCE6EF` | instrument hairlines |

- [ ] **Step 1: Recolour the `CATS` table**

Lines 502–506 — change only the `color:` value on each row, leaving `key` and `name` untouched:
`A` → `#3B7DE8`, `B` → `#E39A0C`, `C` → `#8B5CF6`, `D` → `#0FA98A`, `E` → `#E2493C`.

- [ ] **Step 2: Recolour the `MISSIONS` table**

Lines 1182–1194 — change only the `c:` value on each entry:
`onboarding` → `#3B7DE8`, `radar` → `#E39A0C`, `console` → `#0FA98A`, `thresholds` → `#8B5CF6`, `vault` → `#C9962C`.

Then line 2084 in `screenCertificate()`, which passes a literal mission-like object: `c:'#F5D06B'` → `c:'#C9962C'`.

- [ ] **Step 3: Recolour `radarSVG()`**

- The `sw` gradient's two `stop-color="#2BD9B0"` → `#0FA98A`
- Dial face: `fill="#0B131B" stroke="#22303F"` → `fill="#F5F8FB" stroke="#DCE6EF"`
- The ring/crosshair group `stroke="#22303F"` → `stroke="#DCE6EF"`
- The three blips, the centre dot, and the pulsing ring: `#2BD9B0` → `#0FA98A` (four occurrences)

- [ ] **Step 4: Recolour `thermoSVG()`**

- The `col` ternary: `'#4C8DF6'`→`'#3B7DE8'`, `'#FF5F52'`→`'#E2493C'`, `'#F2B138'`→`'#E39A0C'`, `'#2BD9B0'`→`'#0FA98A'`
- Track rect `fill="#1E2B3A"` → `fill="#DCE6EF"`
- Label group `fill="#55677A"` → `fill="#6B7F92"`
- Threshold marker lines: `stroke="#F2B138"` → `#E39A0C`, `stroke="#FF5F52"` → `#E2493C`
- The position dot's outline `stroke="#070B11"` → `stroke="#FFFFFF"` — it exists to separate the dot from the surface behind it, so on a light panel it must become white, not dark

- [ ] **Step 5: Recolour `gaugeSVG()` — this is the critical one**

- Base arc `arc(-180,-0.01,r,'#1E2B3A',13)` → `'#DCE6EF'`
- Banded arcs: `'#2BD9B0'`→`'#0FA98A'`, `'#F2B138'`→`'#E39A0C'`, `'#FF5F52'`→`'#E2493C'`; non-cash arc `'#4C8DF6'`→`'#3B7DE8'`
- Tick label group `fill="#55677A"` → `fill="#6B7F92"`
- **Needle** `fill="#E9EFF5"` → `fill="#10202F"`
- Hub `fill="#111A24" stroke="#2E4155"` → `fill="#10202F" stroke="#FFFFFF"`
- **Amount readout** `fill="#E9EFF5"` → `fill="#10202F"` — this is the near-invisible number
- Sub-label `fill="#7A8DA0"` → `fill="#6B7F92"`

- [ ] **Step 6: Audit the remaining generators — report, do not change**

`avatar()`, `artBankVault()`, `sealSVG()` and `badgeArt()` also contain dark literals, but each is a special case: `artBankVault()` is removed from the page in Task 7, `avatar()` loses its last caller in Task 10, and `sealSVG()`/`badgeArt()` sit on the cream certificate and badge chips handled in Task 12. `avatar()` in particular draws a self-contained dark medallion, which reads as a deliberate portrait frame on white rather than a bug.

Inspect all four and **report** anything that will look broken on a light page. Change none of them — later tasks own them.

- [ ] **Step 7: Verify**

Search the file for any remaining occurrence of the six old accent hexes:

```powershell
rg -n "#4C8DF6|#F2B138|#A57BFF|#2BD9B0|#FF5F52|#F5D06B" aml-compliance-academy.html
```

Expected: matches only inside `avatar()`, `artBankVault()`, `sealSVG()`, `badgeArt()`, and the `.stamp` CSS tints. Any match inside `CATS`, `MISSIONS`, `radarSVG`, `thermoSVG`, `gaugeSVG` or `screenCertificate` means a replacement was missed.

Then confirm no near-white fills remain on light panels:

```powershell
rg -n "#E9EFF5" aml-compliance-academy.html
```

Expected: one match only, inside `avatar()` (line ~924).

- [ ] **Step 8: Commit**

Skipped — see the Deviations note. Refresh the rolling backup instead.

---

### Task 3c: Recolour the always-visible chrome and award art

Task 3b's audit surfaced four more generators carrying old-palette hexes that no task owned. Two of them (`rankBadge`, the brand mark) are on screen on *every* screen, and `sealSVG()`'s pale gold `#F5D06B` on the now-cream certificate was a real legibility failure, worst on the letter-spaced SENTINEL wordmark.

**Files:**

- Modify: `aml-compliance-academy.html` — brand mark SVG (~line 452), `rankBadge()` (~950), `sealSVG()` (~1054), `badgeArt()` (~1071)

- [ ] **Step 1: Brand mark** — gradient stops `#2BD9B0`→`#0FA98A`, `#4C8DF6`→`#3B7DE8`; shield fill `rgba(43,217,176,.08)`→`rgba(15,169,138,.08)`
- [ ] **Step 2: `rankBadge()`** — star dots `#F5D06B`→`#C9962C`; gradient stops as above; shield fill `rgba(43,217,176,.1)`→`rgba(15,169,138,.10)`
- [ ] **Step 3: `sealSVG()`** — all five `#F5D06B`→`#C9962C`; inner fill `rgba(245,208,107,.09)`→`rgba(201,150,44,.10)`
- [ ] **Step 4: `badgeArt()`** — the six map entries to `#3B7DE8`, `#E39A0C`, `#0FA98A`, `#8B5CF6`, `#C9962C`, `#E2493C`, matching `MISSIONS` so a module header and its badge agree
- [ ] **Step 5: Verify** — `rg -n "#4C8DF6|#F2B138|#A57BFF|#2BD9B0|#FF5F52|#F5D06B|#E9EFF5" aml-compliance-academy.html` must return matches **only** inside `artBankVault()` (removed from the page in Task 7), `avatar()` (last caller removed in Task 10), and the `#fx`/`confetti()` canvas code (Task 13 Steps 1–2). Anything else is a miss.

**Status: completed inline by the controller**, not dispatched — four verified mechanical colour swaps did not warrant a subagent.

---

### Task 4: Cinematic layer — CSS

**Files:**

- Modify: `aml-compliance-academy.html` — insert a new CSS block immediately before the closing `</style>` (currently line 425).

**Interfaces:**

- Produces: the classes `.cine`, `.cine-bg`, `.cine-scrim`, `.cine-actors`, `.actor`, `.cbubble`, `.crow`, `.cchoices`, `.cprompt`, `.cnext`, `.ring`, consumed by Tasks 5–12.

- [ ] **Step 1: Insert the cinematic CSS**

```css
/* ================= cinematic layer ================= */
#cine{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.cine-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:0;transition:opacity .6s ease;transform:scale(1.04)}
.cine-bg.in{opacity:1}
.cine-scrim{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(244,249,253,.55) 0%,rgba(244,249,253,.20) 35%,rgba(227,238,247,.72) 100%)}

#actors{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.actor{position:absolute;bottom:0;height:74vh;max-height:640px;width:auto;
  opacity:0;transition:opacity .35s ease,transform .45s cubic-bezier(.2,.9,.3,1);
  filter:drop-shadow(0 18px 34px rgba(16,32,47,.22))}
.actor.left{left:2vw;transform:translateX(-60px)}
.actor.right{right:2vw;transform:translateX(60px)}
.actor.in{opacity:1;transform:translateX(0)}
.actor.idle{animation:float 4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@media(max-width:900px){.actor{height:42vh;opacity:.35!important}}

/* speech bubble */
.cbubble{position:relative;background:var(--surface);border-radius:16px;
  padding:20px 24px;font-size:16px;line-height:1.65;color:var(--ink);
  box-shadow:var(--shadow-lg);max-width:62ch;
  animation:bpop .32s cubic-bezier(.2,1.2,.4,1)}
.cbubble::before{content:'';position:absolute;inset:-2px;border-radius:18px;z-index:-1;
  background:linear-gradient(120deg,var(--grad-a),var(--grad-b))}
.cbubble .who{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.cbubble .caret{display:inline-block;width:2px;height:1em;background:var(--ink);
  vertical-align:-2px;animation:blink .7s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
@keyframes bpop{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}

/* answer list */
.cprompt{display:inline-flex;align-items:center;gap:8px;background:var(--green);color:#fff;
  font-weight:700;font-size:13px;letter-spacing:.01em;padding:10px 18px;border-radius:8px;
  box-shadow:var(--shadow);margin-bottom:14px}
.cchoices{display:flex;flex-direction:column;gap:10px}
.crow{display:flex;align-items:center;gap:14px;text-align:left;width:100%;
  background:rgba(255,255,255,.9);backdrop-filter:blur(14px);
  border:1px solid rgba(255,255,255,.9);border-radius:12px;padding:14px 18px;
  font-family:var(--sans);font-size:14.5px;line-height:1.55;color:var(--text);
  cursor:pointer;box-shadow:var(--shadow);
  opacity:0;transform:translateY(10px);
  transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease,background .16s ease}
.crow.shown{opacity:1;transform:none;transition:opacity .3s ease,transform .3s ease}
.crow:hover:not(:disabled){transform:translateY(-2px);box-shadow:var(--shadow-lg);border-color:var(--grad-b)}
.crow .ic{flex:none;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;
  background:var(--surface2);color:var(--muted);font-family:var(--mono);font-size:13px;font-weight:600;
  transition:.16s}
.crow:hover:not(:disabled) .ic{background:color-mix(in srgb,var(--teal) 14%,transparent);color:var(--teal)}
.crow.good{border-color:var(--teal);background:color-mix(in srgb,var(--teal) 10%,#fff)}
.crow.good .ic{background:var(--teal);color:#fff}
.crow.meh{border-color:var(--amber);background:color-mix(in srgb,var(--amber) 12%,#fff)}
.crow.meh .ic{background:var(--amber);color:#fff}
.crow.bad{border-color:var(--coral);background:color-mix(in srgb,var(--coral) 10%,#fff)}
.crow.bad .ic{background:var(--coral);color:#fff}
.crow.faded{opacity:.4}
.crow:disabled{cursor:default}

.cnext{position:relative;margin-left:auto;display:inline-flex;align-items:center;gap:9px;
  background:linear-gradient(135deg,var(--grad-a),var(--grad-b));color:#0C2A25;font-weight:700;
  font-size:14px;padding:13px 26px;border:none;border-radius:10px;cursor:pointer;
  box-shadow:var(--shadow-lg);transition:.16s}
.cnext:hover{filter:brightness(1.06);transform:translateY(-1px)}

/* countdown ring */
.ring{position:relative;width:82px;height:82px;flex:none}
.ring svg{transform:rotate(-90deg);width:100%;height:100%}
.ring .trk{fill:rgba(255,255,255,.75);stroke:var(--line);stroke-width:7}
.ring .prg{fill:none;stroke:var(--teal);stroke-width:7;stroke-linecap:round;
  transition:stroke-dashoffset .1s linear,stroke .3s ease}
.ring.danger .prg{stroke:var(--coral)}
.ring .lbl{position:absolute;inset:0;display:grid;place-items:center;
  font-family:var(--mono);font-size:17px;font-weight:600;color:var(--ink)}
.ring.danger .lbl{color:var(--coral)}

/* scene-mode screens sit above the cinematic layer */
body.scene #stage{position:relative;z-index:2;max-width:1180px}
body.scene .panel,body.scene .hudpill,body.scene .mhead .back{
  background:rgba(255,255,255,.88);backdrop-filter:blur(14px)}
.skipbtn{position:fixed;right:20px;bottom:20px;z-index:130;background:rgba(255,255,255,.9);
  backdrop-filter:blur(10px);border:1px solid var(--line);border-radius:30px;
  padding:9px 18px;font-family:var(--sans);font-size:12.5px;font-weight:600;color:var(--muted);
  cursor:pointer;box-shadow:var(--shadow)}
.skipbtn:hover{color:var(--ink)}
```

- [ ] **Step 2: Verify nothing regressed**

Reload the file. You must observe that home and all four modules look and behave exactly as they did at the end of Task 3 — this task adds unused classes only, so any visual change means a typo has broken a rule above it. Check the browser console for CSS parse warnings.

- [ ] **Step 3: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: add cinematic layer stylesheet"
```

---



### Task 5: Cinematic layer — JS helpers

**Files:**

- Modify: `aml-compliance-academy.html` — add two containers to the body markup (after line 429, alongside `<canvas id="confetti">`), and insert the helper block into the engine `<script>` immediately after `numberKeys` (line 1307).

**Interfaces:**

- Consumes: `ART` asset paths from Tasks 1–2; CSS classes from Task 4.
- Produces, for all later tasks:
  - `ART` — object mapping key → path, e.g. `ART['elena-explain']`
  - `setScene(bgKey)` → `void` — cross-fades the background; `setScene(null)` clears it and exits scene mode
  - `actor(artKey, side, opts)` → `{el, mood(artKey), exit()}` — `side` is `'left'` or `'right'`
  - `clearActors()` → `void`
  - `say(name, text, opts)` → `Promise<void>` — `opts.el` is the container element to render into; resolves when typing finishes
  - `choices(items, opts)` → `Promise<number>` — `items` is `[{t, ic}]`; resolves with the chosen index
  - `brief(m, bgKey, artKey, name, lines)` → `Promise<void>` — renders the pre-module briefing; resolves when the user presses Start
  - `ringHTML(id)` → `string`; `ringSet(id, frac, secs)` → `void`

- [ ] **Step 1: Add the layer containers to the markup**

Immediately after `<canvas id="confetti"></canvas>` (line 429), add:

```html
<div id="cine"><img class="cine-bg" id="cbgA" alt=""><img class="cine-bg" id="cbgB" alt=""><div class="cine-scrim" id="cscrim" style="opacity:0;transition:opacity .6s ease"></div></div>
<div id="actors"></div>
```

These sit outside `#app`, so `go()` replacing `#stage`'s innerHTML never destroys them. That is the whole reason the background can cross-fade between screens.

- [ ] **Step 2: Insert the helper block**

Insert after `numberKeys` (line 1307), before `</script>`:

```js
/* =====================================================================
   CINEMATIC LAYER — background, actors, typed speech, staged choices
   ===================================================================== */
const ART = {
  'elena-explain':'assets/elena-explain.png',
  'elena-concern':'assets/elena-concern.png',
  'marcus-neutral':'assets/marcus-neutral.png',
  'marcus-alarm':'assets/marcus-alarm.png',
  'cust-trader':'assets/cust-trader.png',
  'cust-elder':'assets/cust-elder.png',
  'cust-student':'assets/cust-student.png',
  'cust-pep':'assets/cust-pep.png',
  'cust-ngo':'assets/cust-ngo.png',
  'cust-foreign':'assets/cust-foreign.png',
  'bg-skyline':'assets/bg-skyline.png',
  'bg-branch':'assets/bg-branch.png',
  'bg-opsfloor':'assets/bg-opsfloor.png',
  'bg-boardroom':'assets/bg-boardroom.png',
  'bg-hall':'assets/bg-hall.png'
};
const CUST_ART = ['cust-trader','cust-elder','cust-student','cust-pep','cust-ngo','cust-foreign'];
const custArt = seed => CUST_ART[Math.abs(seed|0) % CUST_ART.length];

/* ---- background ---- */
let _bgTop = false, _bgKey = null;
function setScene(key){
  const scrim = document.getElementById('cscrim');
  if (!key){
    _bgKey = null;
    document.getElementById('cbgA').classList.remove('in');
    document.getElementById('cbgB').classList.remove('in');
    scrim.style.opacity = 0;
    document.body.classList.remove('scene');
    return;
  }
  document.body.classList.add('scene');
  scrim.style.opacity = 1;
  if (key === _bgKey) return;
  _bgKey = key;
  const incoming = document.getElementById(_bgTop ? 'cbgA' : 'cbgB');
  const outgoing = document.getElementById(_bgTop ? 'cbgB' : 'cbgA');
  _bgTop = !_bgTop;
  incoming.src = ART[key];
  incoming.classList.add('in');
  outgoing.classList.remove('in');
}

/* ---- actors ---- */
const _actors = {};
function clearActors(){
  Object.keys(_actors).forEach(k=>_actors[k].exit());
}
function actor(artKey, side, opts){
  opts = opts || {};
  const id = opts.id || side;
  if (_actors[id]){ _actors[id].mood(artKey); return _actors[id]; }
  const el = document.createElement('img');
  el.className = 'actor ' + side;
  el.alt = '';
  el.src = ART[artKey];
  document.getElementById('actors').appendChild(el);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    el.classList.add('in');
    setTimeout(()=>el.classList.add('idle'), 500);
  }));
  const handle = {
    el,
    mood(nextKey){
      if (el.src.endsWith(ART[nextKey])) return;
      el.style.opacity = 0;
      setTimeout(()=>{ el.src = ART[nextKey]; el.style.opacity = 1; }, 200);
    },
    exit(){
      el.classList.remove('in','idle');
      setTimeout(()=>el.remove(), 450);
      delete _actors[id];
    }
  };
  _actors[id] = handle;
  return handle;
}

/* ---- typed speech ---- */
let _typing = null;
function say(name, text, opts){
  opts = opts || {};
  const host = opts.el || document.getElementById('bubbleslot');
  const speed = opts.speed == null ? 18 : opts.speed;
  return new Promise(resolve=>{
    const b = document.createElement('div');
    b.className = 'cbubble';
    b.innerHTML = (name ? `<span class="who">${name}</span>` : '') +
                  `<span class="body"></span><span class="caret"></span>`;
    if (opts.append) host.appendChild(b); else { host.innerHTML = ''; host.appendChild(b); }
    const body = b.querySelector('.body');
    const caret = b.querySelector('.caret');
    let i = 0;
    const done = ()=>{
      if (_typing){ clearInterval(_typing); _typing = null; }
      body.textContent = text;
      caret.remove();
      b.onclick = null;
      resolve();
    };
    b.onclick = done;
    if (speed === 0){ done(); return; }
    _typing = setInterval(()=>{
      body.textContent = text.slice(0, ++i);
      if (i >= text.length) done();
    }, speed);
    activeTimers.push(_typing);
  });
}

/* ---- staged choices ---- */
function choices(items, opts){
  opts = opts || {};
  const host = opts.el || document.getElementById('choiceslot');
  return new Promise(resolve=>{
    host.innerHTML =
      (opts.prompt === false ? '' : `<div class="cprompt">${opts.prompt || 'Select The Most Effective Answer.'}</div>`) +
      `<div class="cchoices" id="crows">` +
      items.map((c,ix)=>`<button class="crow" data-i="${ix}">
        <span class="ic">${c.ic == null ? ix+1 : c.ic}</span><span>${c.t}</span></button>`).join('') +
      `</div>`;
    const rows = [...host.querySelectorAll('.crow')];
    rows.forEach((r,ix)=>setTimeout(()=>r.classList.add('shown'), 60*ix));
    setKeys(numberKeys(()=>rows));
    rows.forEach(r=>{ r.onclick = ()=>{ beep('pick'); resolve(parseInt(r.dataset.i,10)); }; });
  });
}

/* ---- module briefing ---- */
function brief(m, bgKey, artKey, name, lines){
  return new Promise(resolve=>{
    setKeys(null);
    clearActors();
    setScene(bgKey);
    actor(artKey, 'right', {id:'mentor'});
    go(`${missionHead(m,'')}
      <div style="max-width:min(100%,700px);padding:4vh 0 0">
        <div id="bubbleslot"></div>
        <div id="ctaslot" style="display:flex;margin-top:20px"></div>
      </div>`);
    bindBack();
    (async ()=>{
      for (const line of lines) await say(name, line, {append:true});
      document.getElementById('ctaslot').innerHTML =
        `<button class="cnext" id="startbtn">Start ${icon('arrow')}</button>`;
      const sb = document.getElementById('startbtn');
      sb.onclick = ()=>{ beep('pick'); resolve(); };
      setKeys(e=>{ if (e.key==='Enter'||e.key===' '){ e.preventDefault(); sb.click(); } });
    })();
  });
}

/* ---- countdown ring ---- */
const RING_C = 2 * Math.PI * 34;
function ringHTML(id){
  return `<div class="ring" id="${id}">
    <svg viewBox="0 0 82 82">
      <circle class="trk" cx="41" cy="41" r="34"/>
      <circle class="prg" cx="41" cy="41" r="34"
        stroke-dasharray="${RING_C.toFixed(1)}" stroke-dashoffset="0"/>
    </svg>
    <div class="lbl">0:00</div>
  </div>`;
}
function ringSet(id, frac, secs){
  const w = document.getElementById(id);
  if (!w) return;
  frac = Math.max(0, Math.min(1, frac));
  w.querySelector('.prg').style.strokeDashoffset = (RING_C * (1 - frac)).toFixed(1);
  const s = Math.max(0, Math.ceil(secs));
  w.querySelector('.lbl').textContent = Math.floor(s/60) + ':' + String(s%60).padStart(2,'0');
  w.classList.toggle('danger', frac <= 0.28);
}
```

- [ ] **Step 3: Verify the helpers in isolation**



Reload the page, open the browser console and run:

```js
setScene('bg-branch');
const a = actor('elena-explain','right');
document.getElementById('stage').insertAdjacentHTML('afterbegin','<div id="bubbleslot"></div><div id="choiceslot"></div>');
say('Elena Vance','This is a test of the typed speech bubble.').then(()=>console.log('typed'));
```

You must observe:

1. The branch background fades in behind the page over roughly half a second.
2. Elena slides in from the right and settles into a slow up-and-down float.
3. A white bubble with a purple-to-mint gradient edge types the sentence out character by character, then `typed` logs.

Then run:

```js
a.mood('elena-concern');
choices([{t:'First option'},{t:'Second option'},{t:'Third option'}]).then(i=>console.log('picked',i));
```

You must observe: Elena cross-fades to the folded-arms pose; a green "Select The Most Effective Answer" pill appears above three white rows that fade in one after another; clicking one logs its index; pressing `2` also works.

Then test the briefing end to end:

```js
brief(MISSIONS[0],'bg-boardroom','elena-explain','Elena Vance',
      ['First briefing line.','Second briefing line.']).then(()=>console.log('briefed'));
```

You must observe: the background cross-fades to the boardroom, Elena re-enters on the right, both lines type in sequence and remain stacked, a Start button appears, and clicking it logs `briefed`.

Finally run `ringSet('r',0.2,12)` after inserting `ringHTML('r')` and confirm the ring turns coral and reads `0:12`. Then `setScene(null)` and confirm the background clears and the page returns to the plain light theme.

- [ ] **Step 4: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: add cinematic layer helpers"
```

---



### Task 6: Cold open

**Files:**

- Modify: `aml-compliance-academy.html:1182` (the `S` default object), and the boot block (lines 2099–2114).

**Interfaces:**

- Consumes: `setScene`, `actor`, `say`, `clearActors` from Task 5.
- Produces: `async function coldOpen()` → `Promise<void>`, called from boot.

- [ ] **Step 1: Add the persistence flag**

Change line 1182 from:

```js
let S = {xp:0, best:{}, badges:[], seen:[], muted:false};
```

to:

```js
let S = {xp:0, best:{}, badges:[], seen:[], muted:false, seenIntro:false};
```

`load()` does `Object.assign(S, JSON.parse(r))`, so existing saved progress simply lacks the key and correctly defaults to `false`.

- [ ] **Step 2: Add the cold open function**

Insert immediately before the `BOOT` comment block (line 2096):

```js
/* =====================================================================
   COLD OPEN
   ===================================================================== */
function coldOpen(){
  return new Promise(resolve=>{
    setKeys(null);
    setScene('bg-skyline');

    const skip = document.createElement('button');
    skip.className = 'skipbtn';
    skip.textContent = 'Skip intro';
    document.body.appendChild(skip);

    let cancelled = false;
    const finish = ()=>{
      if (cancelled) return;
      cancelled = true;
      skip.remove();
      clearActors();
      S.seenIntro = true; save();
      resolve();
    };
    skip.onclick = finish;

    stage.innerHTML = `<div class="screen" style="min-height:66vh;display:flex;flex-direction:column;
      align-items:center;justify-content:center;gap:26px;text-align:center">
      <div id="titleslot">
        <div class="eyebrow" style="justify-content:center">SBP AML/CFT &middot; Training simulation</div>
        <h1 style="font-size:44px;line-height:1.08;font-weight:700;letter-spacing:-.02em;margin-top:12px">
          SENTINEL</h1>
      </div>
      <div id="bubbleslot" style="max-width:640px"></div>
      <div id="ctaslot"></div>
    </div>`;

    (async ()=>{
      await new Promise(r=>setTimeout(r, 700));
      if (cancelled) return;

      const elena = actor('elena-explain','right');
      await new Promise(r=>setTimeout(r, 500));
      if (cancelled) return;
      await say('Elena Vance \u00b7 Head of Financial Crime Compliance',
        'You are the last control before the money moves. Everything upstream of you is paperwork. Everything downstream is somebody else\u2019s problem.');
      if (cancelled) return;

      const marcus = actor('marcus-neutral','left');
      await new Promise(r=>setTimeout(r, 450));
      if (cancelled) return;
      await say('Marcus Hale \u00b7 Senior AML Analyst',
        'Four modules. Onboard a customer who does not want to be onboarded properly, learn the red-flag families by sight, work a live transaction queue, and drill the thresholds until they are reflex.',
        {append:true});
      if (cancelled) return;

      document.getElementById('ctaslot').innerHTML =
        `<button class="cnext" id="beginbtn" style="margin:0">Begin training</button>`;
      const bb = document.getElementById('beginbtn');
      bb.onclick = ()=>{ beep('pick'); finish(); };
      setKeys(e=>{ if (e.key==='Enter'||e.key===' '){ e.preventDefault(); bb.click(); } });
    })();
  });
}
```

- [ ] **Step 3: Wire it into boot**

Replace the final four lines of the file's script (lines 2111–2114):

```js
load();
renderRank();
renderSoundBtn();
home();
```

with:

```js
load();
renderRank();
renderSoundBtn();
if (S.seenIntro) home();
else coldOpen().then(home);
```

- [ ] **Step 4: Add an intro replay to the reset handler**

In the `resetbtn` handler (line 2106), change the state reset to also clear the flag:

```js
S = {xp:0, best:{}, badges:[], seen:[], muted:S.muted, seenIntro:true};
```

Progress resets but the intro does not replay — resetting scores is a deliberate act by someone who has already seen it.

- [ ] **Step 5: Verify the cold open**

In the console run `localStorage.removeItem('sentinel_aml_v1')`, then reload. You must observe:

1. The skyline fades in, the SENTINEL title card shows.
2. Elena slides in from the right and her line types out.
3. Marcus slides in from the left and his line types out *below* hers, both bubbles visible.
4. A "Begin training" button appears; clicking it clears the actors and lands on the home screen.
5. Reload again — the intro does **not** replay; you land straight on home.
6. Repeat from step 1, but click "Skip intro" during Elena's line. You must land on home immediately with no actors left on screen, and the intro must not replay on the next reload.
7. Repeat once more and click directly on a bubble while it is typing — the full text must appear at once and the sequence must continue.

- [ ] **Step 6: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: add cold open intro sequence"
```

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



### Task 8: Module 01 — onboarding as scenario stage

**Files:**

- Modify: `aml-compliance-academy.html:1437-1561` (`missionOnboarding`)

**Interfaces:**

- Consumes: `setScene`, `actor`, `say`, `choices`, `custArt`, `clearActors`.

This is the module the reference screenshots most directly describe: a customer opposite you, speaking, with five ranked responses.

- [ ] **Step 1: Declare the actor handles**

At the top of `missionOnboarding()`, after `const P = DIALOGUE.persona;`, add:

```js
  let custA = null;
  let mentorA = null;
```

These are `let`, not `const`, because the customer is not mounted until the briefing in Step 8 finishes.

- [ ] **Step 2: Replace the persona panel with the staged layout**

In `draw()`, replace the whole `<div class="dlg-wrap">…</div>` block (lines 1462–1493) with:

```js
      <div class="panel" style="max-width:min(100%,760px);margin-left:auto">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">
          <div>
            <div style="font-size:15px;font-weight:600;color:var(--ink)">${P.name}</div>
            <div style="font-size:12px;color:var(--muted)">${P.role}</div>
          </div>
          <div style="flex:1"></div>
          <div class="meter" style="width:150px;margin:0">
            <div class="mrow"><span>File integrity</span><span style="color:${integrity>=80?'var(--teal)':integrity>=50?'var(--amber)':'var(--coral)'}">${integrity}%</span></div>
            <div class="bar"><i style="width:${integrity}%;background:${integrity>=80?'var(--teal)':integrity>=50?'var(--amber)':'var(--coral)'}"></i></div>
          </div>
          <div class="meter" style="width:150px;margin:0">
            <div class="mrow"><span>Rapport</span><span style="color:var(--blue)">${rapport}%</span></div>
            <div class="bar"><i style="width:${rapport}%;background:var(--blue)"></i></div>
          </div>
        </div>
        ${b.sys ? `<div class="bubble sys"><span class="who">Eleven days later</span>${b.sys}</div>` : ''}
        ${i===0 ? `<div class="bubble sys"><span class="who">Branch floor</span>${DIALOGUE.intro}</div>` : ''}
        <div id="bubbleslot"></div>
        ${b.note ? `<div class="narr" style="margin:14px 0 0"><b style="color:var(--amber);font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:6px">On the file</b>${b.note}</div>` : ''}
        <div id="choiceslot" style="margin-top:18px"></div>
        <div id="fbslot"></div>
      </div>
```

The scrolling `.dlg-log` history is removed: with the customer physically present and speaking, a transcript above the bubble reads as clutter. The information it carried — what you already said — is not needed to answer the current beat.

- [ ] **Step 3: Drive the beat with the cinematic helpers**

Replace the tail of `draw()` (lines 1494–1500, from `bindBack();` to the end of the function) with:

```js
    bindBack();
    custA.mood(custArt(P.seed));
    (async ()=>{
      await say(P.name, b.say);
      const ix = await choices(b.choices.map(c=>({t:c.t})));
      const btn = document.querySelector(`#crows .crow[data-i="${ix}"]`);
      answer(ix, btn);
    })();
```

- [ ] **Step 4: Update** `answer()` **to the new row classes**

In `answer()`, replace the selector block (lines 1516–1520):

```js
    document.querySelectorAll('#crows .crow').forEach(el=>{
      el.disabled = true;
      el.onclick = null;
      if (el !== btn) el.classList.add('faded');
    });
    btn.classList.add(c.v);
```

- [ ] **Step 5: Make the mentor react**

Immediately after `btn.classList.add(c.v);` in `answer()`, add:

```js
    mentorA = actor(c.v === 'good' ? 'elena-explain' : 'elena-concern', 'right', {id:'mentor'});
```

- [ ] **Step 6: Restyle the continue button**

In `answer()`, change the feedback slot's button (line 1528) from `class="btn primary wide"` to `class="cnext"` and wrap it so it sits right-aligned:

```js
      <div style="display:flex;margin-top:14px"><button class="cnext" id="nextbtn">${i+1>=seq.length && branchResolved()?'See assessment':'Next'} ${icon('arrow')}</button></div>`;
```

- [ ] **Step 7: Clean up on exit**

At the top of `finish()`, add:

```js
    clearActors();
```

- [ ] **Step 8: Open with Elena's briefing**

Replace the trailing `draw();` at the end of `missionOnboarding()` with:

```js
  brief(m, 'bg-branch', 'elena-explain', 'Elena Vance', [
    'There is a new relationship waiting at the counter. Your job is customer due diligence: identify them, verify the identity against a reliable source, establish who really owns the business, and then decide how much scrutiny this file needs.',
    'The customer will be helpful right up to the moment you ask something inconvenient. Remember that rapport is not what the file is judged on.'
  ]).then(()=>{
    clearActors();
    setScene('bg-branch');
    custA = actor(custArt(P.seed), 'left', {id:'cust'});
    draw();
  });
```

- [ ] **Step 9: Verify module 01**

Open the module from home and play it to the end. You must observe:

1. Elena briefs you over the branch background first, two bubbles typing in sequence, then a Start button. On starting, Elena leaves and a customer stands on the left.
2. The customer's line types into a gradient-edged bubble, then the answer rows fade in one by one under a green "Select The Most Effective Answer." pill.
3. Pressing a number key selects that row; clicking works too.
4. On answering, the chosen row turns teal / amber / coral, the others fade, and Elena appears on the right — explaining pose for a correct answer, folded-arms for a wrong one.
5. The verdict text and its regulation citation still appear.
6. The integrity and rapport meters still move, and the CDD step strip still advances.
7. The branch into EDD still triggers, and the results screen still shows the by-CDD-step breakdown with the same numbers you would have got before.
8. Going back to the academy mid-module clears both characters.

- [ ] **Step 10: Commit**

```bash
git add aml-compliance-academy.html
git commit -m "feat: restage onboarding module as scenario stage"
```

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



## Notes for the implementer

**Line numbers drift.** Every line reference in this plan is against the original 2,118-line file. After Task 3 and Task 4 insert their blocks, everything below shifts by several hundred lines. Locate code by the function name and surrounding text given in each step, and treat the line numbers as a hint about where to look, not an address.

**The** `stage` **collision is the one trap.** `const stage = document.getElementById('stage')` exists at line 1263. The background helper is `setScene`. If you find yourself writing `stage(` for anything other than the DOM element, stop.

**Abandoned promises are expected.** `choices()` and `say()` return promises that never resolve if the screen changes first — for example when a countdown expires and auto-answers while `choices()` is still pending. This leaks nothing observable because every path that abandons a promise also disables the rows and guards re-entry with the module's `locked` flag. Do not add cancellation machinery to "fix" it; do keep the `locked` guards intact.

**Verification is not optional.** There is no test suite to catch a regression, so the browser checks in each task are the only safety net. Run them before committing.