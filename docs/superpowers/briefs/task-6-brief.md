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


