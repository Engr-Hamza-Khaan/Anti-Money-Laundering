# AML/CFT & KYC — Content Notes for PoC Build
**Source:** State Bank of Pakistan, AML/CFT Regulations for Banks & DFIs (updated to Dec 2019, still current framework as of Aug 2026 — verify against latest BPRD circulars before final content lock)
**Purpose:** Raw regulatory content, pre-structured for the three delivery components — dialogue simulation, red-flag/case content, and transaction-review simulator.

---

## 1. Core concepts (feeds: document explorer / glossary, dialogue simulation prompts)

| Term | Definition (paraphrased) |
|---|---|
| KYC/CDD | Identifying the customer, verifying identity via reliable documents/sources, understanding the purpose of the relationship, and monitoring the account on an ongoing basis for consistency with the customer's known profile. |
| Beneficial Owner | The real natural person who ultimately owns or controls the customer or on whose behalf a transaction happens — not necessarily the named account holder. |
| EDD (Enhanced Due Diligence) | Extra scrutiny applied above standard CDD for higher-risk customers/products/geographies — extra info on occupation, source of funds/wealth, senior management sign-off, more frequent monitoring. |
| PEP (Politically Exposed Person) | Someone in a prominent public role (head of state, senior politician, judge, military official, senior state-owned enterprise exec) or their close associates/family — does not include junior officials. |
| STR (Suspicious Transaction Report) | Filed regardless of amount, whenever a transaction is suspected of being linked to money laundering or terrorism financing. |
| CTR (Currency Transaction Report) | Filed for cash transactions of PKR 2 million and above. |

---

## 2. Key thresholds & triggers (feeds: transaction-review simulator logic)

These are the concrete numeric rules your dev can encode as decision logic for the simulator:

- **CTR trigger**: cash transactions ≥ **PKR 2,000,000** — must be reported regardless of suspicion.
- **Walk-in/occasional customer identity verification required for**: cash transactions of **PKR 500,000 or above**, single or apparently-linked.
- **STR trigger**: no minimum amount — filed whenever suspicion exists, including attempted (not completed) transactions.
- **PEP handling**: requires senior management approval to open/continue relationship + source-of-wealth documentation + enhanced ongoing monitoring.
- **NGO/NPO/Charity accounts**: automatic EDD + senior management approval, regardless of transaction size.
- **Record retention**: 10 years from transaction date; 10 years after relationship ends for identification records.

**Simulator logic hook**: any transaction the employee reviews can be tagged against these thresholds so the "correct" flag/clear decision is deterministic and gradeable — useful for the scoring layer.

---

## 3. Red-flag indicator library (feeds: card-based case scenarios, dialogue simulation branch triggers, transaction-review simulator's "suspicious" transaction generator)

Organized into categories your dev team can use as tags/filters when generating scenario variants:

**A. Transactions inconsistent with customer profile**
- Frequent transfers between the customer's own multiple accounts, or unusually high liquidity for their stated profile
- Funds withdrawn almost immediately after deposit, with no plausible business reason
- Deposits/withdrawals structured to fall just under reporting thresholds (e.g., repeated PKR 490,000 cash deposits)
- Large cash activity in an account whose stated business would normally use cheques/instruments instead

**B. Large cash activity**
- Exchanging many small-denomination notes for large ones
- Large cash withdrawal from a previously dormant account, or one that just received an unexpected large credit
- Multiple people using separate tellers simultaneously for large transactions (structuring)

**C. Cross-border / wire transfer concerns**
- Wire transfers to/from jurisdictions of concern with no clear business reason
- Large incoming/outgoing wires with no logical business purpose
- Wire transfers deliberately kept small to avoid reporting thresholds
- Missing originator/beneficiary information on incoming transfers

**D. Unidentified or unclear parties**
- Third-party collateral/guarantees from someone with no discernible relationship to the customer
- Payment orders with inaccurate info about who placed them
- Trustee/nominee accounts inconsistent with the customer's stated business

**E. Suspicious account behavior**
- Customer reluctant to provide information, or provides info that's expensive/difficult to verify
- Dormant account suddenly receiving deposits followed by rapid withdrawals until drained
- Shared address across unrelated legal entities with the same signatories, no clear reason
- Stated occupation doesn't match transaction volume (e.g., a student with frequent large wires)

**Use for scenario variety**: each category above can seed a distinct branch in the dialogue simulation or a distinct card in the case-scenario deck — gives you natural content diversity without repeating the same "red flag" every time.

---

## 4. CDD process flow (feeds: dialogue simulation — this is literally the conversation structure)

This is the actual sequence a bank employee follows during onboarding, which maps directly onto a branching dialogue:

1. **Identify** — obtain full name, ID document number, address, DOB, nationality, nature of business, purpose of account, source of earnings, expected monthly turnover
2. **Verify** — check the ID against a reliable source (NADRA/biometric for Pakistani nationals); biometric verification is mandatory before establishing new relationships except for defined exceptions
3. **Understand beneficial ownership** — if the customer isn't a natural person, identify who actually owns/controls it (20%+ shareholding threshold, 10%+ under EDD)
4. **Assess risk / decide CDD level** — Simplified, standard CDD, or Enhanced, based on customer/product/geography risk
5. **Monitor on an ongoing basis** — flag transactions inconsistent with the customer's known profile

**Dialogue branch point**: after step 4, the employee's risk assessment choice determines whether the simulation proceeds down a standard onboarding path or an EDD path (more questions, senior management approval step) — this is your core adaptive branch for this modality.

---

## 5. Reporting obligations (feeds: consequence/outcome content — what happens after a "flag" decision)

- STRs are filed with FMU (Financial Monitoring Unit), regardless of transaction size, including attempted transactions
- Employees are strictly prohibited from disclosing to the customer that an STR has been or is being filed ("tipping off") — this itself is a disciplinable/reportable offense
- The basis for deciding to file or not file an STR must be documented, even if no STR is ultimately filed
- Reporting suspicious transactions cannot be delegated to outsourced staff

**Use in scenario consequences**: this is good material for a "wrong choice" branch — e.g., an employee who tells the customer "we've flagged your account" should trigger a clear violation consequence in the simulation, since tipping off is explicitly prohibited.

---

## 6. Suggested mapping to the 3 delivery modalities

| Modality | What from this doc it uses |
|---|---|
| Interactive dialogue simulation | Section 4 (CDD process flow) as the conversation skeleton; Section 3 red flags as things the "customer" says/does that the employee must catch |
| Card-based case scenarios | Section 3 red-flag categories, each as a standalone case; Section 2 thresholds for scoring correct/incorrect flag decisions |
| Simulated transaction-review interface | Section 2 thresholds as the deterministic logic layer; Section 3 red flags as generated transaction patterns to detect |

---

*Note: this reflects the regulation booklet as last compiled by SBP (through Dec 2019 amendments). Before finalizing content for the UBL pitch, verify against SBP's current circulars page for any amendments since — the source document itself carries this same disclaimer.*
