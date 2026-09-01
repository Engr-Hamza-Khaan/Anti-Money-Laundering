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
