# Task 3b Report — Recolour the JavaScript-drawn graphics

**File modified:** `aml-compliance-academy.html` (single file, no build)
**Status:** DONE_WITH_CONCERNS
**Steps 1–5:** complete · **Step 6:** audit delivered, no code changed · **Step 7:** both greps run, output pasted verbatim · **Step 8:** skipped per instruction (no git in project)

All "to" values were taken verbatim from the Global Constraints palette and the Task 3b mapping table. No colour was invented or adjusted. The CSS block was not touched. No user-visible text, regulatory string, threshold, id, icon, `meta`, or scoring value was altered — every edit below changes only a colour literal.

---

## Step 1 — `CATS` table (lines 502–506)

Only the `color:` field changed on each row; `key:` and `name:` are byte-identical.

| Row | Before | After |
| --- | --- | --- |
| `A` Inconsistent with customer profile | `#4C8DF6` | `#3B7DE8` |
| `B` Large cash activity | `#F2B138` | `#E39A0C` |
| `C` Cross-border / wire concerns | `#A57BFF` | `#8B5CF6` |
| `D` Unidentified or unclear parties | `#2BD9B0` | `#0FA98A` |
| `E` Suspicious account behaviour | `#FF5F52` | `#E2493C` |

After:

```502:506:aml-compliance-academy.html
  A:{key:'A', name:'Inconsistent with customer profile', color:'#3B7DE8'},
  B:{key:'B', name:'Large cash activity',                color:'#E39A0C'},
  C:{key:'C', name:'Cross-border / wire concerns',       color:'#8B5CF6'},
  D:{key:'D', name:'Unidentified or unclear parties',    color:'#0FA98A'},
  E:{key:'E', name:'Suspicious account behaviour',       color:'#E2493C'}
```

Note the original column alignment of the `name:`/`color:` fields was preserved, so the replacement is a pure in-place hex swap.

---

## Step 2 — `MISSIONS` table (lines 1181–1197) and `screenCertificate()` (line 2084)

Only the `c:` field changed on each entry. `id`, `k`, `n`, `icon`, `d` and `meta` are byte-identical — each edit targeted only the object's first line and left the `d:`/`meta:` continuation lines untouched.

| Entry | Before | After |
| --- | --- | --- |
| `onboarding` | `#4C8DF6` | `#3B7DE8` |
| `radar` | `#F2B138` | `#E39A0C` |
| `console` | `#2BD9B0` | `#0FA98A` |
| `thresholds` | `#A57BFF` | `#8B5CF6` |
| `vault` | `#F5D06B` | `#C9962C` |

After:

```1182:1194:aml-compliance-academy.html
  {id:'onboarding', k:'Module 01', n:'Customer Onboarding', icon:'dialogue', c:'#3B7DE8',
  {id:'radar', k:'Module 02', n:'Red-Flag Radar', icon:'radar', c:'#E39A0C',
  {id:'console', k:'Module 03', n:'Review Console', icon:'console', c:'#0FA98A',
  {id:'thresholds', k:'Module 04', n:'Threshold Trainer', icon:'gauge', c:'#8B5CF6',
  {id:'vault', k:'Reference', n:'Reference Vault', icon:'vault', c:'#C9962C',
```

(Lines shown are the five object-opening lines only; the intervening `d:`/`meta:` lines are unchanged and omitted here for brevity.)

`screenCertificate()` — the literal mission-like object passed to `missionHead()`:

- Before: `${missionHead({k:'Credential', n:'Programme record', c:'#F5D06B'}, '')}`
- After: `${missionHead({k:'Credential', n:'Programme record', c:'#C9962C'}, '')}`

Both `k` and `n` strings unchanged.

These two tables were the contrast priority flagged in the brief: `.mcard .mk` and `.play` render `var(--c)` as *text* on white cards, so the old bright accents (`#2BD9B0` teal and `#F5D06B` gold especially) were failing as labels. All five values are now the palette's text-safe accents.

---

## Step 3 — `radarSVG()` (lines 969–995)

| Element | Before | After |
| --- | --- | --- |
| `sw` gradient stop 1 | `stop-color="#2BD9B0" stop-opacity="0"` | `stop-color="#0FA98A" stop-opacity="0"` |
| `sw` gradient stop 2 | `stop-color="#2BD9B0" stop-opacity=".55"` | `stop-color="#0FA98A" stop-opacity=".55"` |
| Dial face (r=92) | `fill="#0B131B" stroke="#22303F"` | `fill="#F5F8FB" stroke="#DCE6EF"` |
| Ring/crosshair group | `stroke="#22303F"` | `stroke="#DCE6EF"` |
| Blip group (3 circles) | `fill="#2BD9B0"` | `fill="#0FA98A"` |
| Centre dot | `fill="#2BD9B0"` | `fill="#0FA98A"` |
| Pulsing ring | `stroke="#2BD9B0"` | `stroke="#0FA98A"` |

That is four `#2BD9B0` → `#0FA98A` occurrences in the body (blip group, centre dot, pulsing ring — the blip group is one `fill` attribute covering three circles) plus the two gradient stops, matching the brief's count. Stroke widths, radii, `opacity` values and both `<animate>` blocks are untouched.

After:

```974:990:aml-compliance-academy.html
        <stop offset="0" stop-color="#0FA98A" stop-opacity="0"/>
        <stop offset="1" stop-color="#0FA98A" stop-opacity=".55"/>
      </linearGradient>
    </defs>
    <circle cx="100" cy="100" r="92" fill="#F5F8FB" stroke="#DCE6EF" stroke-width="1.4"/>
    <g fill="none" stroke="#DCE6EF" stroke-width="1">
      <circle cx="100" cy="100" r="70"/><circle cx="100" cy="100" r="47"/><circle cx="100" cy="100" r="24"/>
      <path d="M100 8v184M8 100h184"/>
      <path d="M35 35l130 130M165 35L35 165" opacity=".5"/>
    </g>
    <path class="rsweep" d="M100 100 L192 100 A92 92 0 0 0 165 35 Z" fill="url(#sw)"/>
    <g class="rblip" fill="#0FA98A">
      <circle cx="142" cy="66" r="3.4"/><circle cx="70" cy="132" r="2.6" opacity=".7"/>
      <circle cx="122" cy="140" r="2.2" opacity=".5"/>
    </g>
    <circle cx="100" cy="100" r="4" fill="#0FA98A"/>
    <circle cx="100" cy="100" r="4" fill="none" stroke="#0FA98A" stroke-width="1.4">
```

---

## Step 4 — `thermoSVG()` (lines 998–1018)

| Element | Before | After |
| --- | --- | --- |
| `col` ternary — non-cash | `'#4C8DF6'` | `'#3B7DE8'` |
| `col` ternary — ≥ CTR_CASH | `'#FF5F52'` | `'#E2493C'` |
| `col` ternary — ≥ WALKIN_VERIFY | `'#F2B138'` | `'#E39A0C'` |
| `col` ternary — below both | `'#2BD9B0'` | `'#0FA98A'` |
| Track rect | `fill="#1E2B3A"` | `fill="#DCE6EF"` |
| Label group | `fill="#55677A"` | `fill="#6B7F92"` |
| Verify marker line | `stroke="#F2B138"` | `stroke="#E39A0C"` |
| CTR marker line | `stroke="#FF5F52"` | `stroke="#E2493C"` |
| Position dot outline | `stroke="#070B11"` | `stroke="#FFFFFF"` |

The ternary's *structure* and both threshold comparisons (`RULES.CTR_CASH`, `RULES.WALKIN_VERIFY`) are unchanged — only the four returned hex strings. The `500K · verify` and `2M · CTR` label text, the `cash`/`transfer` label, and all coordinate expressions are unchanged.

The position-dot outline is the one non-mechanical substitution in this step: it is a separator stroke whose job is to lift the dot off the surface behind it, so on a light panel it inverts to `#FFFFFF` rather than mapping through the colour table. This matches the brief's explicit instruction.

After:

```1004:1015:aml-compliance-academy.html
  const col = !isCash ? '#3B7DE8' : amount >= RULES.CTR_CASH ? '#E2493C' : amount >= RULES.WALKIN_VERIFY ? '#E39A0C' : '#0FA98A';
  return `
  <svg viewBox="0 0 400 52" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="22" width="400" height="8" rx="4" fill="#DCE6EF"/>
    <rect x="0" y="22" width="${(x*4).toFixed(1)}" height="8" rx="4" fill="${col}"/>
    <g font-family="IBM Plex Mono, monospace" font-size="8" fill="#6B7F92">
      <line x1="..." y1="14" x2="..." y2="38" stroke="#E39A0C" stroke-width="1" stroke-dasharray="2 2"/>
      <text x="..." y="12">500K · verify</text>
      <line x1="..." y1="14" x2="..." y2="38" stroke="#E2493C" stroke-width="1" stroke-dasharray="2 2"/>
      <text x="..." y="12">2M · CTR</text>
    </g>
    <circle cx="..." cy="26" r="6" fill="${col}" stroke="#FFFFFF" stroke-width="2"/>
```

(Coordinate template expressions elided as `...` for readability; they are unchanged in the file.)

---

## Step 5 — `gaugeSVG()` (lines 1021–1051) — the critical fix

| Element | Before | After |
| --- | --- | --- |
| Base arc | `arc(-180,-0.01,r,'#1E2B3A',13)` | `arc(-180,-0.01,r,'#DCE6EF',13)` |
| Cash band — below verify | `'#2BD9B0'` | `'#0FA98A'` |
| Cash band — verify→CTR | `'#F2B138'` | `'#E39A0C'` |
| Cash band — above CTR | `'#FF5F52'` | `'#E2493C'` |
| Non-cash arc | `'#4C8DF6'` | `'#3B7DE8'` |
| Tick label group | `fill="#55677A"` | `fill="#6B7F92"` |
| **Needle** | `fill="#E9EFF5"` | `fill="#10202F"` |
| Hub | `fill="#111A24" stroke="#2E4155"` | `fill="#10202F" stroke="#FFFFFF"` |
| **Amount readout** | `fill="#E9EFF5"` | `fill="#10202F"` |
| Sub-label | `fill="#7A8DA0"` | `fill="#6B7F92"` |

This resolves the defect the brief singled out: the transaction amount — the single most important number on the Threshold Trainer screen — was printing in `#E9EFF5` (near-white) on what Task 3 had made a white panel, i.e. effectively invisible. It is now `#10202F` ink. The needle had the same failure and is fixed the same way. The hub's stroke inverts to white for the same separator reason as the thermo dot.

Untouched in this function: `max = 3000000`, the `frac`/`ang` maths, `r`/`cx`/`cy`, the `rad`/`px`/`py`/`arc` helpers, `aVerify`/`aCtr` derived from `RULES.*`, the `0` / `500K` / `2M` / `3M+` tick text, `PKR(amount)`, the `CASH`/`NON-CASH TRANSFER` label, all font sizes and all geometry.

After:

```1035:1049:aml-compliance-academy.html
    ${arc(-180,-0.01,r,'#DCE6EF',13)}
    ${cash ? arc(-180,aVerify,r,'#0FA98A',13) + arc(aVerify,aCtr,r,'#E39A0C',13) + arc(aCtr,-0.01,r,'#E2493C',13)
           : arc(-180,-0.01,r,'#3B7DE8',13)}
    <g font-family="IBM Plex Mono, monospace" font-size="8.5" fill="#6B7F92">
      <text x="18" y="164">0</text>
      <text x="..." y="...">500K</text>
      <text x="..." y="...">2M</text>
      <text x="282" y="164">3M+</text>
    </g>
    <g transform="rotate(${ang.toFixed(2)} ${cx} ${cy})">
      <path d="M${cx} ${cy} L${cx+r-16} ${cy-4} L${cx+r-16} ${cy+4} Z" fill="#10202F"/>
    </g>
    <circle cx="${cx}" cy="${cy}" r="9" fill="#10202F" stroke="#FFFFFF" stroke-width="2"/>
    <text x="${cx}" y="${cy-30}" text-anchor="middle" ... font-size="23" font-weight="600" fill="#10202F">${PKR(amount)}</text>
    <text x="${cx}" y="${cy-13}" text-anchor="middle" ... font-size="10.5" fill="#6B7F92">${cash?'CASH':'NON-CASH TRANSFER'}</text>
```

---

## Step 6 — Audit of the four remaining generators (report only, nothing changed)

I inspected all four and changed none of them. Findings below, ordered by severity.

### 1. `artBankVault()` — line 819 — **severe, worst remaining element on the page**

Every fill in this 300×260 hero is dark: the masonry gradient `gA` is `#2E4256 → #18242F`, the pediment inner is `#101A24`, the three step bars are `#22323F` / `#1B2934` / `#16222C`, the vault door is `#101A24` / `#16232F` / `#0C141C`, and the two alert chips are `#1B2B22` and `#2E2415`. Column strokes are `#3C5468` / `#243444`.

On the new `#F4F9FD` page this renders as a near-black building occupying the landing screen's hero slot (called at line 1352 inside `.hero-art`). Separately, the `gGlow` radial — `#2BD9B0` at `.38` fading to `0` — is a dark-theme glow idiom: on white it does not read as light emission at all, it reads as a muddy green-grey haze ring behind the building.

Task 7 removes this element from the page, which resolves it. **Flagging because until Task 7 lands, the landing screen is the most visually broken screen in the app** — if the task order shifts, this should be pulled forward.

### 2. `sealSVG()` — line 1054 — **high, genuine legibility failure, and an internal colour conflict**

All seal ink is the old bright gold `#F5D06B`: 28 rays at `opacity=".55"`, the r=36 ring, the r=29 inner ring at `opacity=".6"`, the star, and the `SENTINEL` wordmark at `font-size="8"` with `letter-spacing="1.4"`.

It sits on `.cert`, which is `linear-gradient(150deg,#FFFDF6,#FFF8E8)` — cream (line 410). `#F5D06B` on `#FFFDF6` is very low contrast before opacity is applied; the rays at 55% and the inner ring at 60% will be close to invisible, and an 8px letter-spaced wordmark in that gold on cream fails legibility outright. Of the four generators this is the only one with a hard *text* legibility failure.

There is also a live inconsistency worth passing to Task 12: `.cert`'s border and its `.ct` label already use `var(--gold)` = `#C9962C` after Task 3, and as of this task the certificate's `missionHead` chip is `#C9962C` too — but the seal in the middle of that same card is still `#F5D06B`. Two different golds now sit side by side on one card. Moving the seal to `#C9962C` would fix both the contrast and the mismatch. (Minor third variant: the print-only override at line 2081 uses `border-color:#B9963C`.)

### 3. `badgeArt()` — line 1071 — **moderate, two of six colours wash out**

The `map` holds six old accents: `onboarding:#4C8DF6`, `radar:#F2B138`, `console:#2BD9B0`, `thresholds:#A57BFF`, `vault:#F5D06B`, `clean:#FF5F52`. They are applied as a 1.7px `stroke` plus a `fill-opacity=".13"` wash, on `.badge` chips on a white card (line 1382).

`#2BD9B0` (console) and `#F5D06B` (vault) are the two failures — both are high-luminance and at a 1.7px stroke on white they will look faded rather than drawn; the `.13` fill wash beneath them effectively disappears. `#F2B138` (radar) is borderline. Unearned badges are safe because `.badge` applies `opacity:.24; filter:grayscale(1)` (line 422), so the weakness only shows on *earned* badges at full opacity — i.e. exactly when the user has earned the reward.

Task 12 can apply the Task 3b mapping table verbatim; all six values are in it.

One consequence of this task's scope worth recording: `badgeArt()`'s keys mirror the `MISSIONS` ids, and its colours were the same values as the `MISSIONS` `c:` fields. Because Step 2 recoloured `MISSIONS` but Step 6 forbids touching `badgeArt()`, the same module is now drawn in two different colours in two places — e.g. Module 02's header chip is `#E39A0C` while its `radar` badge is still `#F2B138`. This is an expected transient that Task 12 closes; noting it so it is not mistaken for a missed replacement.

### 4. `avatar()` — line 888 — **low as drawn, but the brief's caller assumption is wrong**

Visually I agree with the brief. The medallion is self-contained: an `av${seed}` gradient disc `#1D2B3A → #111A24` with a `#2E4155` ring, and everything inside it (skins `#E3B183`…, hairs `#241C14`…, shirts `#2C4A6B`…, the `#E9EFF5` tie, `#8FA3B8` glasses, `#F6F9FB` eye whites) is tuned against that dark disc and stays internally consistent. On white it reads as a deliberate dark portrait frame, not a bug. No change warranted on appearance grounds.

**However — `avatar()` has two callers, not one.** The brief says "`avatar()` loses its last caller in Task 10", but:

- line 1482 — `<div class="av">${avatar(P.seed, mood())}</div>` in the onboarding dialogue persona (styled by `.persona .av`, 150px, with a `drop-shadow(0 12px 24px rgba(16,32,47,.22))`)
- line 1724 — `<div style="width:88px">${avatar(cust.seed,'neutral')}</div>` in the Review Console customer panel, inline-styled, no `.persona` wrapper

If Task 10 only replaces the persona call at 1482, `avatar()` stays live on the Review Console screen and its dark literals stay on the page. The console instance also has no frame styling around it, so an unsoftened dark disc will be the heaviest object on an otherwise white case panel. **Task 10's scope should be confirmed to cover both call sites, or the console avatar handled explicitly.** This is the one audit finding that could silently invalidate a later task's assumption.

---

## Step 7 — Verification

### Command 1 — remaining old accent hexes

```powershell
rg -n "#4C8DF6|#F2B138|#A57BFF|#2BD9B0|#FF5F52|#F5D06B" aml-compliance-academy.html
```

Verbatim output:

```
454:          <stop offset="0" stop-color="#2BD9B0"/><stop offset="1" stop-color="#4C8DF6"/>
827:        <stop offset="0" stop-color="#2BD9B0"/><stop offset="1" stop-color="#4C8DF6"/>
830:        <stop offset="0" stop-color="#2BD9B0" stop-opacity=".38"/>
831:        <stop offset="1" stop-color="#2BD9B0" stop-opacity="0"/>
866:    <g fill="#2BD9B0" opacity=".75">
874:        <rect x="-19" y="-13" width="38" height="26" rx="7" fill="#1B2B22" stroke="#2BD9B0" stroke-width="1.3"/>
875:        <path d="M-6 0l4.4 4.6L8-4.6" stroke="#2BD9B0" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
879:        <rect x="-19" y="-13" width="38" height="26" rx="7" fill="#2E2415" stroke="#F2B138" stroke-width="1.3"/>
880:        <path d="M0-6.5v7" stroke="#F2B138" stroke-width="2.4" stroke-linecap="round"/>
881:        <circle cx="0" cy="5" r="1.6" fill="#F2B138"/>
955:    pts.push(`<circle cx="${x.toFixed(1)}" cy="25" r="1.9" fill="#F5D06B"/>`);
960:      <stop offset="0" stop-color="#2BD9B0"/><stop offset="1" stop-color="#4C8DF6"/>
1058:    rays.push(`<line x1="${(52+38*Math.cos(a)).toFixed(1)}" y1="${(52+38*Math.sin(a)).toFixed(1)}" x2="${(52+45*Math.cos(a)).toFixed(1)}" y2="${(52+45*Math.sin(a)).toFixed(1)}" stroke="#F5D06B" stroke-width="2" opacity=".55"/>`);
1063:    <circle cx="52" cy="52" r="36" fill="rgba(245,208,107,.09)" stroke="#F5D06B" stroke-width="2"/>
1064:    <circle cx="52" cy="52" r="29" fill="none" stroke="#F5D06B" stroke-width="1" opacity=".6"/>
1065:    <path d="M52 32l3.6 7.6 8.3 1.1-6.1 5.8 1.5 8.3L52 50.9l-7.3 3.9 1.5-8.3-6.1-5.8 8.3-1.1z" fill="#F5D06B"/>
1066:    <text x="52" y="70" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="8" letter-spacing="1.4" fill="#F5D06B">SENTINEL</text>
1073:    onboarding:['#4C8DF6','M12 3l7 3v6c0 4.4-2.9 7.6-7 8.8C7.9 19.6 5 16.4 5 12V6z','M9.4 12.2l1.9 1.9 3.6-3.8'],
1074:    radar:['#F2B138','M12 3a9 9 0 1 0 9 9','M12 12l6-6M12 12h9'],
1075:    console:['#2BD9B0','M4 5h16v14H4z','M8 10h8M8 14h5'],
1076:    thresholds:['#A57BFF','M4 18h16','M7 18V9M12 18V5M17 18v-7'],
1077:    vault:['#F5D06B','M4 5h16v14H4z','M12 9v6M9 12h6'],
1078:    clean:['#FF5F52','M12 3l9 16H3z','M12 10v4M12 17h.01']
1118:    ctx.fillStyle = '#2BD9B0';
1125:      ctx.globalAlpha = g.a; ctx.font = g.s+'px IBM Plex Mono, monospace'; ctx.fillStyle = '#4C8DF6';
1139:  const cols = ['#2BD9B0','#4C8DF6','#F2B138','#A57BFF','#F5D06B'];
```

**The pass condition is met.** The brief's failure condition was "any match inside `CATS`, `MISSIONS`, `radarSVG`, `thermoSVG`, `gaugeSVG` or `screenCertificate`". There are none — no match falls in lines 501–507, 969–995, 998–1018, 1021–1051, 1181–1197, or 2073–2095. All five recolour steps are complete.

**But the output contains four sites the brief did not predict.** The brief expected matches "only inside `avatar()`, `artBankVault()`, `sealSVG()`, `badgeArt()`, and the `.stamp` CSS tints". Reconciling actual against expected:

- **Accounted for by the brief:** 827–881 `artBankVault()`, 1058–1066 `sealSVG()`, 1073–1078 `badgeArt()`.
- **`avatar()` produced no match** — its dark literals are different hexes (`#1D2B3A`, `#111A24`, `#2E4155`, `#E9EFF5`), none of which are in this grep's six. Expected-but-absent, not a problem.
- **`.stamp` CSS produced no match** — lines 353–354 express their tints as `rgba(43,217,176,.09)` and `rgba(255,95,82,.09)`, i.e. decimal rgba rather than hex, so a hex grep structurally cannot find them. The brief's stated expectation could never have matched here. Noting so the next agent does not read this as a regression. (Those two rgba values are the old teal and old coral; their `color`/`border-color` are already `var(--teal)`/`var(--coral)`, so the 9%-alpha backgrounds are now slightly off-hue from their own borders — cosmetic, and CSS is out of bounds for this task.)
- **Not owned by any task in the brief — four unowned sites:**
  - **line 454 — the topbar brand mark.** `#2BD9B0 → #4C8DF6` gradient with `fill="rgba(43,217,176,.08)"`. This is inline SVG in the HTML `<body>`, not a JS generator, so it falls outside Task 3b's file list. It is permanently visible in the topbar on every screen.
  - **lines 955 / 960 — `rankBadge()`.** `#F5D06B` star dots at `r="1.9"`, a `#2BD9B0 → #4C8DF6` shield gradient, and `fill="rgba(43,217,176,.1)"`. Called at line 1272 into the topbar rank chip, so also always visible. The pale gold r=1.9 dots on a light chip will be near-invisible. This is a JS SVG generator with dark literals that the brief's Step 6 list omits entirely.
  - **lines 1118 / 1125 — the `#fx` ambience canvas.** `ctx.fillStyle='#2BD9B0'` for drifting dots and `'#4C8DF6'` for currency glyphs. Low severity: these draw at `globalAlpha` of roughly `.1–.5` and `.02–.07`, and were designed to glow against a dark page — on `#F4F9FD` they will read as faintly invisible rather than wrong.
  - **line 1139 — `confetti()`.** All five old accents. Only visible during a burst; low severity, but should eventually track the new palette.

These four are reported, not fixed — they are outside this task's declared file list, and Step 6's instruction to leave later tasks' code alone implies the same restraint for code no task has claimed. **Recommend they be assigned explicitly**, since `rankBadge()` and the brand mark are on screen at all times and no downstream task currently covers them.

### Command 2 — remaining near-white fills

```powershell
rg -n "#E9EFF5" aml-compliance-academy.html
```

Verbatim output:

```
924:      <path d="M60 92l-9 9 9 21 9-21z" fill="#E9EFF5" opacity=".92"/>
```

**Exactly as expected: one match, inside `avatar()`, at line 924** (the tie on the avatar's shirt, drawn against `avatar()`'s own dark disc, correct as-is). The two `#E9EFF5` fills in `gaugeSVG()` — the needle and the amount readout — are gone, confirming the critical fix landed.

---

## Step 8 — Commit

Skipped as instructed: this project has no git. Nothing was done in its place, and the pristine reference copy at `_backup\aml-compliance-academy.ORIGINAL.html` was read for comparison only and not modified. Note that backup still carries the pre-Task-3 dark stylesheet.

---

## Constraint compliance

- Palette values used verbatim from Global Constraints / the Task 3b table; nothing invented or adjusted.
- `CATS` — only `color:` touched. `MISSIONS` — only `c:` touched. All names, ids, descriptions, icons, thresholds and `meta` byte-identical.
- No user-visible text, regulatory string, or scoring/progression logic altered.
- CSS block not touched.
- `avatar()`, `artBankVault()`, `sealSVG()`, `badgeArt()` inspected and left unmodified.
- Located every edit by function name and surrounding text rather than by the brief's approximate line numbers. In this file the numbering happened to still line up closely, but the anchoring was textual.

## Concerns for the next task

1. **`avatar()` has two callers (lines 1482 and 1724), not one.** Task 10's "loses its last caller" premise looks incomplete; if only the persona call is removed, the console avatar keeps dark literals on the page.
2. **Four sites with old accents are unowned by any task** — brand mark (454), `rankBadge()` (955/960), `#fx` canvas (1118/1125), `confetti()` (1139). `rankBadge()` and the brand mark are visible on every screen.
3. **`sealSVG()` is a real legibility failure, not just a stylistic leftover** — `#F5D06B` ink on the cream `.cert`, worst on the 8px `SENTINEL` wordmark, and it now clashes with the `#C9962C` gold used by the same card's border and label. Task 12 should treat it as contrast work.
4. **`badgeArt()` and `MISSIONS` now disagree per module** (e.g. `#E39A0C` header vs `#F2B138` radar badge) — expected until Task 12, flagged so it is not read as a missed replacement.
5. **The brief's Step 7 `.stamp` expectation cannot match**, because those tints are `rgba(...)` not hex.
6. **Not verified in a browser** — no test framework and no browser available, so correctness rests on the two ripgrep checks plus a read-back of each edited region. The colour choices are mechanical applications of the mapping table; actual rendered contrast on each screen is unconfirmed.
