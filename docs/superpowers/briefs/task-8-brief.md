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


