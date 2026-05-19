# Reference File Template — uni-advisor-research.md

This file defines what `[VAULT]/uni-advisor-research.md` must contain when built or rebuilt.

## Frontmatter (required)

```yaml
---
type: analysis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sections:
  UCAS_Process_and_Deadlines:
    last_verified: YYYY-MM-DD
    cycle: 2026-27
    next_regenerate: 2026-07-01
  European_Fee_Schedules:
    last_verified: YYYY-MM-DD
    next_regenerate: YYYY-09-01
  Subject_Rankings:
    last_verified: YYYY-MM-DD
    next_regenerate: YYYY-07-01
  Admissions_Tests:
    last_verified: YYYY-MM-DD
    next_regenerate: YYYY-07-01
  Interview_Formats:
    last_verified: YYYY-MM-DD
    next_regenerate: YYYY-07-01
  Clearing_and_Adjustment:
    last_verified: YYYY-MM-DD
    next_regenerate: YYYY-07-01
---
```

`next_regenerate` is the date after which this section should be rebuilt. Update it when you rebuild a section.

---

## Research Order (mandatory)

1. UCAS.com — source of truth for deadlines, PS format, Extra, Clearing
2. University websites — admissions tests, interview formats, fee pages
3. Ranking agencies — QS by Subject, Complete University Guide, THE by Subject
4. Graduate outcome databases — Prospects, HighFliers (optional)

---

## Section 1: UCAS Process & Deadlines

**Source:** UCAS.com official only
**Decay:** Rebuild when `next_regenerate` date passes (annually, ~July when new cycle opens)

Must include:
- Oxbridge + Medicine + Vet + Dentistry deadline (typically ~15 October)
- Main UCAS deadline (typically ~14 January)
- UCAS Extra opening (typically ~February)
- Clearing opening (typically ~July)
- A-level Results Day (typically second Thursday of August)
- Current cycle (e.g. 2026-27 entry) clearly labelled

Do NOT include: generic advice about choosing universities, overall rankings, "top 20 lists"

---

## Section 2: UCAS Personal Statement Format

**Source:** UCAS.com official changelog
**Decay:** Manual — rebuild only if UCAS changes format

Must include:
- Number of questions (currently 3 for 2026 entry onwards)
- Total character/line limit (4,000 chars OR 47 lines — whichever first)
- Minimum per question (350 chars)
- Line-break behaviour (heavy line breaks hit 47 lines before 4,000 chars)
- Format version clearly labelled (e.g. "2026 entry format")

---

## Section 3: Subject Rankings Guide

**Source:** QS by Subject, Complete University Guide by Subject
**Decay:** Annual (~July when new rankings drop)

Must include:
- Why subject ranking differs from overall ranking (explicit explanation)
- How to use each ranking agency (QS = global prestige, CUG = UK teaching quality)
- At least 3 concrete examples showing divergence (e.g. Bath Engineering vs overall, LSE Economics vs overall)

Do NOT include: overall university rankings, "top 20 universities" lists

---

## Section 4: Contextual Offers

**Source:** Individual university websites (Russell Group, targets)
**Decay:** Annual (~July)

Must include:
- Which UK universities offer contextual schemes
- Eligibility criteria (typically: school postcode, FSM, first-generation)
- Typical grade reduction per scheme (usually 1–2 grades lower)
- How to flag eligibility on UCAS application

---

## Section 5: European Options (by country)

**Source:** Institutional websites (not generic guides)
**Decay:** Annual (~September before new academic year)

CRITICAL: Always split public vs private. The same country can have 10x fee difference.

Must include per country (tailor to the user's confirmed course direction — examples below cover business/entrepreneurship/management; adjust institution list for other subjects):
- Public university fee range (verified on government/DAAD/equivalent source)
- Private institution fees — named institutions with approximate fees and "verify" flag
- English-taught programmes available (yes/no and scale)
- Post-Brexit status (UK = international student; Switzerland CHF 730/semester all students)

Country list minimum:
- Germany (WHU, TU Munich; most public unis free/low cost — verify per state)
- Netherlands (Erasmus Rotterdam, Maastricht — English programmes)
- Italy (Bocconi ~€14–15k private — verify; Bologna/Milan public €1–4k)
- Spain (IE Madrid ~€20k+ private — verify; public €1–3.5k)
- Switzerland (ETH Zurich ~CHF 730/semester)
- Sweden (KTH, Stockholm School of Economics)
- Denmark (Copenhagen Business School)

Warning callout required:
> ⚠ IE Madrid, Bocconi, ESADE are private institutions. Fees are NOT representative of their country's public sector. Always web search before quoting any specific institution's fees.

---

## Section 6: Admissions Tests

**Source:** University websites (not generic test prep sites)
**Decay:** Annual (~July when new cycle tests confirmed)

Must include (verify per cycle — these change frequently):
- Natural Sciences Cambridge → ESAT (NSAA abolished 2024)
- Physics Oxford/Cambridge → ESAT (PAT abolished 2026)
- Maths Oxford/Cambridge → TMUA (MAT abolished 2025)
- Engineering Oxford → PAT (confirm status)
- Economics/Management → TSA (confirm which universities)
- Business schools (IE Madrid, Bocconi) → GMAT/own test or none (check per institution)

Each entry must show: test name, universities requiring it, registration window, where to find practice materials

---

## Section 7: Interview Formats

**Source:** University websites, student forums (cross-reference)
**Decay:** Annual (~July)

Must include:
- Oxbridge academic format: unfamiliar problem, think out loud, reasoning over answer
- UK business school format (e.g. Durham, Warwick): competency or panel
- European business school formats:
  - IE Madrid: typically group exercise + case study + individual interview (verify)
  - Bocconi: written test + motivation interview (verify)
- How to find format-specific prep materials per institution

---

## Section 8: Clearing & Adjustment Guide

**Source:** UCAS.com official
**Decay:** Annual (~July)

Must include:
- How Clearing works (from Results Day, call universities directly with UCAS reference)
- How Adjustment works (grade exceeds firm conditions → 5-day window to trade up)
- Accurate framing: many strong universities (including Russell Group) participate in Clearing for specific courses

Do NOT include discouraging language. Clearing is a legitimate pathway.

---

## Validation Checklist (before committing rebuilt file)

- [ ] All UCAS dates verified on UCAS.com within the last 7 days
- [ ] PS format matches current UCAS specs (3 questions, 4,000 chars)
- [ ] European fees verified on 2+ institutional sites (not generic guides)
- [ ] Admissions tests cross-referenced against 3+ university pages
- [ ] Interview formats include academic (Oxbridge) and competency (business school) examples
- [ ] Section frontmatter updated: `last_verified` and `next_regenerate` for rebuilt sections

## If rebuild is incomplete

Flag in frontmatter:
```yaml
incomplete_sections:
  - name: Interview_Formats
    reason: Could not find IE Madrid 2026-27 format directly
    fallback: Recommend the user contacts IE Madrid admissions directly
```

Sections 1–4 (UCAS, PS format, Rankings, Contextual Offers) are critical — do not publish without them.
Sections 5–8 are important but can be published with flags if partially incomplete.
