# Task 3 Report — Light theme conversion

**File modified:** `aml-compliance-academy.html` (10 edits, all inside the `<style>` block)
**Status:** DONE_WITH_CONCERNS
**Steps completed:** 1–9 (code), 10 (static verification in lieu of browser), 11 skipped per controller instruction (no git in project)

No JavaScript, no markup, no text content, no regulatory data and no scoring logic was touched. No layout, sizing or spacing property was added or altered. Every hex/rgba value came verbatim from the brief.

---

## Step-by-step edits

### Step 1 — Replace the `:root` block

Lines 11–31 → lines 11–45.

**Before**

```css
:root{
  --bg:#070B11;
  --bg2:#0C1219;
  --panel:#111A24;
  --panel2:#17222F;
  --panel3:#1E2B3A;
  --border:#22303F;
  --border2:#2E4155;
  --text:#E9EFF5;
  --muted:#7A8DA0;
  --dim:#55677A;
  --teal:#2BD9B0;
  --blue:#4C8DF6;
  --amber:#F2B138;
  --coral:#FF5F52;
  --violet:#A57BFF;
  --gold:#F5D06B;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
  --sans:'IBM Plex Sans',system-ui,sans-serif;
  --r:12px;
}
```

**After** — exactly as specified in the brief, including the legacy alias block:

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

All 8 legacy names are preserved. Confirmed by search that the sheet still references `--panel` (many rules), `--panel2`, `--panel3`, `--border`, `--border2`, `--dim`, `--bg`; these all now resolve to light values. `--bg` and `--bg2` are no longer read by any rule after Step 2 replaced the `body` background, but they are retained as the brief specifies them.

### Step 2 — Page background and body text

**Before**

```css
body{
  background:var(--bg);
  color:var(--text);
  ...
}
```

**After**

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

### Step 3 — Top bar

**Before**

```css
  background:rgba(7,11,17,.82);
  backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);
```

**After**

```css
  background:rgba(255,255,255,.78);
  backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line); box-shadow:0 4px 20px -14px rgba(16,32,47,.35);
```

### Step 4 — Headings to ink

Added immediately after the `body` rule (line 56):

```css
h1,h2,h3,h4{color:var(--ink)}
```

Specificity checked: this rule (0,0,1) is correctly overridden where a heading was deliberately coloured — `.dossier h4{color:var(--muted)}` (0,1,1) and `.hero h1 em{color:transparent}` (0,1,2) both still win, so the dossier label stays muted and the hero gradient-text effect still works.

### Step 5 — Shadows from dark-drop to soft-lift

Three replacements:

| Rule | Before | After |
| --- | --- | --- |
| `.mcard:hover` | `box-shadow:0 16px 40px -18px rgba(0,0,0,.85)` | `box-shadow:var(--shadow-lg)` |
| `.toast` | `box-shadow:0 14px 34px -14px rgba(0,0,0,.9)` | `box-shadow:var(--shadow-lg)` |
| `.persona .av` | `filter:drop-shadow(0 12px 24px rgba(0,0,0,.5))` | `filter:drop-shadow(0 12px 24px rgba(16,32,47,.22))` |

### Step 6 — Cards get lift

Added after the `.panel` rules (lines 166–167):

```css
.panel,.mcard,.stat,.hudpill,.rankchip,.iconbtn{box-shadow:var(--shadow)}
.stat{background:var(--surface)}
```

Cascade checked: `.stat` at line 118 still declares `background:rgba(255,255,255,.03)` (0,1,0), and the new `.stat` rule at line 167 has equal specificity but comes later, so `--surface` wins — the near-transparent white is dead but harmless. `.mcard:hover` (0,2,0, line 136) still beats the new `.mcard` shadow (0,1,0), so the hover lift is preserved even though it appears earlier in the sheet.

### Step 7 — Primary button contrast

**Before** `.btn.primary{background:linear-gradient(135deg,var(--teal),#1DA98A);color:#04140F;border-color:transparent}`

**After** `.btn.primary{background:linear-gradient(135deg,var(--teal),#0B8F74);color:#FFFFFF;border-color:transparent;box-shadow:var(--shadow)}`

### Step 8 — Hero gradient

**Before**

```css
  background:linear-gradient(135deg,#101B27 0%,#0C1520 60%,#12202B 100%);
  border:1px solid var(--border);
...
  background:radial-gradient(700px 240px at 88% 22%,rgba(43,217,176,.14),transparent 65%),
             radial-gradient(500px 220px at 10% 100%,rgba(76,141,246,.12),transparent 70%);
```

**After**

```css
  background:linear-gradient(135deg,#FFFFFF 0%,#F3F8FD 60%,#EAF3FB 100%);
  border:1px solid var(--line);
...
  background:radial-gradient(700px 240px at 88% 22%,rgba(43,217,176,.20),transparent 65%),
             radial-gradient(500px 220px at 10% 100%,rgba(76,141,246,.16),transparent 70%);
```

The two `rgba()` accent glows keep the old brand RGB triplets, as the brief instructed only the alphas be raised.

### Step 9 — Certificate

**Before** `.cert{background:linear-gradient(150deg,#0F1A24,#0A121A);border:1px solid var(--gold);...`

**After** `.cert{background:linear-gradient(150deg,#FFFDF6,#FFF8E8);border:1px solid var(--gold);...`

### Step 10 — Verification (static, no browser available)

See below.

### Step 11 — Commit

**Skipped** per controller instruction: this project has no git repository. Nothing was done in its place.

---

## Static verification findings

### Method

Re-read every rule changed above (confirmed on disk). Then searched the whole file for dark colour literals: `rgba(0,0,0`, `rgba(7,11,17`, all `#0xxxxx`/`#1xxxxx` six-digit forms, all short hex forms, and every `rgba(` occurrence.

### Result inside the `<style>` block (lines 10–441): clean

The only remaining literals in the stylesheet are the intended ones — `--ink:#10202F`, `--teal:#0FA98A`, and the `#0B8F74` gradient stop from Step 7. Every `rgba()` in the sheet is now either a `rgba(16,32,47,…)` soft shadow, the white top-bar wash, or a light accent tint. No `rgba(0,0,0,…)` and no `rgba(7,11,17,…)` remain in CSS.

Two pre-existing light-tint literals in CSS use the *old* bright brand RGB values and were not in any step's scope, so I left them: `.stamp.good{background:rgba(43,217,176,.09)}` and `.stamp.bad{background:rgba(255,95,82,.09)}` (lines 353–354). Both are ~9%-alpha washes behind text whose colour and border come from `--teal`/`--coral`, so they render as a barely-there tint on white and read correctly. Flagging only because the triplets are stale, not because they are broken.

### Result outside the stylesheet: three real dark-on-light problems, all in JavaScript

These are out of scope for this task (JS is read-only here, and the brief's file list stops at line 424), so I changed nothing. They will be visible as soon as the page is opened and should be assigned to a later task or a follow-up.

1. **Threshold Trainer gauge — near-invisible readout. Highest priority.** `gaugeSVG()` at lines 1045 and 1048 paints the needle and the large central amount text with `fill="#E9EFF5"`. That was near-white on the old dark panel; the gauge now sits inside a white `.panel`, so the transaction amount — the single most important number on that screen — and the needle will be almost unreadable. Line 1049's `fill="#7A8DA0"` sub-label survives on white.
2. **Dark instrument bars on a white page.** The gauge base arc (line 1035, `#1E2B3A`), the thermometer track (line 1007, `#1E2B3A`), the thermometer marker's dark outline ring (line 1015, `stroke="#070B11"`) and the radar dial (line 978, `fill="#0B131B"` with `#22303F` grid) are all still dark-theme fills. They stay legible as "instrument" elements but look like holes punched in the light layout.
3. **Module accent colours are still the bright dark-theme set.** `MISSIONS` (lines 1182–1194) and `FLAGS` (lines 502–506) hold the pre-conversion hexes — `#2BD9B0`, `#F2B138`, `#4C8DF6`, `#A57BFF`, `#F5D06B`. These feed `--c`, which `.mcard .mk` and `.play` use as *text* colour on a white card. Gold `#F5D06B` and teal `#2BD9B0` on white are well under WCAG AA. The new `:root` has correctly darkened `--teal`/`--amber`/`--gold` etc., but these JS copies bypass the variables entirely, so the palette is now split in two.

### Lower-confidence observations — reporting rather than acting

- **Hero illustration (lines 824–888) and generated avatars (lines 916–948)** are dark-navy SVG artwork built for a dark page. They will still render, but as dark blocks on the new white hero. My understanding is the later tasks replace the hero art with a background image and the avatars with character PNGs, so I assume this resolves itself — confirming rather than pre-empting.
- **Brand logo (line 454–456)** uses `#2BD9B0`→`#4C8DF6` gradient strokes with a `rgba(43,217,176,.08)` shield fill, now on a white top bar. Legible but thin and pale. It is markup, not CSS, so out of scope.
- **Background FX canvas** (`#fx`, line 57, `opacity:.55`) draws `#2BD9B0` particles and `#4C8DF6` glyphs (lines 1118, 1125). Bright teal at 55% opacity on a near-white page will be close to invisible. Purely decorative, and the later background-image task probably supersedes this layer.
- **Dimmed/disabled states** (`.choice.faded` .32, `.catbtn.dimmed` .3, `.act:disabled` .32, `.badge` .24 + grayscale) now render as pale grey rather than dim white. Contrast is comparable to before, but the unearned-badge treatment at 24% opacity is the weakest of them and may need lifting once seen in a browser.
- **`.flagcard .wm`** watermark (line 249) has `opacity:.045` and no colour, so it now inherits dark `--text` at 4.5% on a white card. Direction is right (faint dark mark on light) but I could not judge whether it is too faint or too strong without rendering.
- **Print stylesheet** (lines 2080–2082) already forced `background:#fff;color:#111` for the certificate. Still correct, no change needed.

### Step 10's four required observations, as far as static reading can establish

1. *No white-on-white or dark-on-dark text.* **Holds within CSS.** Fails in three JS-generated spots — item 1 above is a genuine white-on-white, and item 3 is a low-contrast (not invisible) case.
2. *Cards read as raised white surfaces.* Holds — `.panel`, `.mcard`, `.stat`, `.hudpill`, `.rankchip`, `.iconbtn` all carry `--shadow` over `--surface`, with `--line` borders.
3. *Verdict colours remain distinguishable.* Holds — `.verdict.good/.bad/.meh` and `.choice.good/.bad/.meh` derive from `--teal` / `--coral` / `--amber`, which are now three well-separated darker hues rendered via `color-mix` tints over white, with matching left borders.
4. *All four modules still function.* No JS was touched and no CSS selector, class name, layout or sizing property was altered, so behaviour is unchanged by construction. Timers, answer registration and scoring were not in the edit path.

### Things I did not verify and cannot

Rendered contrast ratios, `backdrop-filter` appearance over the fixed gradient, and the certificate's gold-on-cream legibility all need an actual browser. A human pass on the four screens is still worth doing before the next task builds on this.
