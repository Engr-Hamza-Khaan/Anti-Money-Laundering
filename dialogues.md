# SENTINEL — Auto-typed dialogues

Har line jo game mein typewriter (`say()`) se aati hai. Player choices, feedback, aur system bubbles is file mein nahi hain.

MP3s: `assets/voice/` (English) · `assets/voice/ur/` (Pakistani Urdu)  
English: Elena = `en-GB-SoniaNeural` · Marcus = `en-GB-RyanNeural` · Danish = `en-IN-PrabhatNeural`  
Urdu: Elena = `ur-PK-UzmaNeural` · Marcus = `ur-PK-AsadNeural` (slower/lower) · Danish = `ur-PK-AsadNeural` (faster/brighter)

---

## Cold open

**Speaker:** Elena Vance — Head of Financial Crime Compliance  
**File:** `01-intro-elena.mp3`

> You are the last control before the money moves. Everything upstream of you is paperwork. Everything downstream is somebody else’s problem.

**Speaker:** Marcus Hale — Senior AML Analyst  
**File:** `02-intro-marcus.mp3`

> Four modules. Onboard a customer who does not want to be onboarded properly, learn the red-flag families by sight, work a live transaction queue, and drill the thresholds until they are reflex.

---

## Module 01 — Customer Onboarding

### Briefing

**Speaker:** Elena Vance  
**File:** `03-onboard-brief-elena-1.mp3`

> There is a new customer waiting at the counter. Your job is customer due diligence: identify them, verify the identity against a reliable source, establish who really owns the business, and then decide how much scrutiny this file needs.

**Speaker:** Elena Vance  
**File:** `04-onboard-brief-elena-2.mp3`

> The customer will be helpful right up to the moment you ask something inconvenient. Remember that rapport is not what the file is judged on.

### Main path — at the counter

**Speaker:** Danish Raza — Walk-in, new account application (Raza Trading Private Limited)

**1. Identify** — `05-onboard-danish-identify.mp3`

> Good morning. I want to open a current account for my company — Raza Trading Private Limited. I have the incorporation certificate here, and my own CNIC.

**2. Verify** — `06-onboard-danish-verify.mp3`

> Here is the CNIC. Look — the photo is clearly me. That’s enough, isn’t it? I’m in a bit of a rush, I have a flight this evening.

**3. Ownership** — `07-onboard-danish-ownership-1.mp3`

> The company shares? I hold 15%. My brother-in-law holds most of it — around 60% — but he’s a silent partner, he won’t be involved in the account at all. He asked me to handle all of it.

**3. Ownership (PEP)** — `08-onboard-danish-ownership-2.mp3`

> Fine, fine. His name is Adnan Sheikh. He is... he serves as an advisor and his father is the provincial minister for industries. Is that a problem? Everything is completely legitimate.

**4. Risk** — `09-onboard-danish-risk.mp3`

> So can we finish this today? I have already told my supplier the account would be ready. Expected turnover — let’s say around 5 million a month to be safe.

### EDD branch

*(Player routes the file to Enhanced Due Diligence.)*

**Speaker:** Danish Raza

**5. Risk — EDD explained** — `10-onboard-danish-edd.mp3`

> Enhanced due diligence? What does that involve? I have given you everything already.

**6. Monitor — tipping off** — `11-onboard-danish-tipping.mp3`

> Look — between us, is my account going to get reported to someone? I have heard banks report people. If anything gets filed on me I want to know about it first.

**7. Monitor — ongoing** — `12-onboard-danish-monitor.mp3`

> All right. Send it to your manager then. How will you handle the account once it opens?

### Standard CDD branch

*(Player proceeds with standard / simplified CDD. Account opens; eleven days later the file comes back.)*

**Speaker:** Danish Raza

**5. Monitor — escalation** — `13-onboard-danish-restricted.mp3`

> Why is my account restricted? I deposited 4.8 million this week and now nothing is going through. You told me everything was fine.

**6. Monitor — what next** — `14-onboard-danish-whatnext.mp3`

> So what happens now? Am I going to lose the account?

---

## Module 02 — Red-Flag Radar

*(Module is currently hidden from the home screen; briefing still exists in code.)*

**Speaker:** Marcus Hale  
**File:** `15-radar-brief-marcus-1.mp3`

> Five red-flag families, A through E, straight out of Annexure-II. If you cannot name the family an observation belongs to, you cannot reach for the right follow-up question.

**Speaker:** Marcus Hale  
**File:** `16-radar-brief-marcus-2.mp3`

> Ten observations, eighteen seconds each. Answer fast and the combo multiplier stays alive.

---

## Module 03 — Review Console

**Speaker:** Elena Vance  
**File:** `17-console-brief-elena-1.mp3`

> This is the live queue. Every case in it is a real transaction waiting on a disposition from you: clear it, flag it, or escalate it.

**Speaker:** Elena Vance  
**File:** `18-console-brief-elena-2.mp3`

> Flagging is not enough on its own. You have to name the indicator you are acting on, because an STR has to record the basis for the decision — and so does a decision not to file one.

---

## Module 04 — Threshold Trainer

**Speaker:** Elena Vance  
**File:** `19-thresholds-brief-elena-1.mp3`

> Thresholds are the part you cannot look up mid-conversation. Two million rupees in cash triggers a CTR whether or not anything looks wrong. Five hundred thousand from a walk-in triggers identity verification. An STR has no floor at all.

**Speaker:** Elena Vance  
**File:** `20-thresholds-brief-elena-2.mp3`

> Twelve drills, twenty-two seconds each. Where more than one obligation could apply, the higher duty wins.

---

## Filename index

| File | Speaker | Scene |
|---|---|---|
| `01-intro-elena.mp3` | Elena Vance | Cold open |
| `02-intro-marcus.mp3` | Marcus Hale | Cold open |
| `03-onboard-brief-elena-1.mp3` | Elena Vance | Onboarding briefing |
| `04-onboard-brief-elena-2.mp3` | Elena Vance | Onboarding briefing |
| `05-onboard-danish-identify.mp3` | Danish Raza | Identify |
| `06-onboard-danish-verify.mp3` | Danish Raza | Verify |
| `07-onboard-danish-ownership-1.mp3` | Danish Raza | Ownership |
| `08-onboard-danish-ownership-2.mp3` | Danish Raza | Ownership / PEP |
| `09-onboard-danish-risk.mp3` | Danish Raza | Risk |
| `10-onboard-danish-edd.mp3` | Danish Raza | EDD branch |
| `11-onboard-danish-tipping.mp3` | Danish Raza | EDD — tipping off |
| `12-onboard-danish-monitor.mp3` | Danish Raza | EDD — monitoring |
| `13-onboard-danish-restricted.mp3` | Danish Raza | Standard branch |
| `14-onboard-danish-whatnext.mp3` | Danish Raza | Standard branch |
| `15-radar-brief-marcus-1.mp3` | Marcus Hale | Radar briefing |
| `16-radar-brief-marcus-2.mp3` | Marcus Hale | Radar briefing |
| `17-console-brief-elena-1.mp3` | Elena Vance | Console briefing |
| `18-console-brief-elena-2.mp3` | Elena Vance | Console briefing |
| `19-thresholds-brief-elena-1.mp3` | Elena Vance | Thresholds briefing |
| `20-thresholds-brief-elena-2.mp3` | Elena Vance | Thresholds briefing |

## Speakers (cast)

| Speaker | Role | Voice |
|---|---|---|
| Elena Vance | Head of Financial Crime Compliance — mentor | `en-GB-SoniaNeural` |
| Marcus Hale | Senior AML Analyst — peer | `en-GB-RyanNeural` |
| Danish Raza | Walk-in customer, new company account | `en-IN-PrabhatNeural` |
