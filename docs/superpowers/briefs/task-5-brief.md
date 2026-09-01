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


