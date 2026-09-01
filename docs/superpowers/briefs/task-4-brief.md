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


