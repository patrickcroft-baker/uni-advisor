# Uni Advisor

A personal university advisor powered by Claude. Helps you research courses, compare universities, explore European options, build a UCAS shortlist, and work on your personal statement.

Built for UK Year 12/13 students applying via UCAS, with full coverage of European university options. Profiles you first — no hardcoded course assumptions.

> **Scope:** Built around the UK application system (UCAS, A-levels, UK universities + European alternatives). Works best for UK students. If you're outside the UK you'll find gaps in the process guidance.

---

## Two ways to use it

### Option 1 — Claude.ai Project (any plan, including free)

1. Go to [claude.ai](https://claude.ai) → **Projects** → **New project**
2. Click **Edit project instructions**
3. Copy and paste the contents of [`claude-ai-project-instructions.md`](./claude-ai-project-instructions.md)
4. Save

Every conversation inside that project will have the advisor ready to go. State is tracked via a copy-paste Profile Summary block between sessions.

---

### Option 2 — Claude Code skill (requires Claude Code)

**Step 1 — Install files:**

```bash
mkdir -p ~/.claude/skills/uni-advisor
BASE="https://raw.githubusercontent.com/PatrickCroft-Baker/uni-advisor/main/uni-advisor"
curl -o ~/.claude/skills/uni-advisor/SKILL.md "$BASE/SKILL.md"
curl -o ~/.claude/skills/uni-advisor/reference-template.md "$BASE/reference-template.md"
curl -o ~/.claude/skills/uni-advisor/generate-uni-pdf.py "$BASE/generate-uni-pdf.py"
curl -o ~/.claude/skills/uni-advisor/setup.sh "$BASE/setup.sh"
```

**Step 2 — Run setup** (installs `fpdf2` and downloads fonts for PDF generation):

```bash
bash ~/.claude/skills/uni-advisor/setup.sh
```

**Step 3 — Start:**

```
/uni-advisor
```

On first use it will ask where to save your progress, then run through a short profile interview. After that it picks up where you left off every session, with full file tracking.

> **PDF reports** require Python 3 and are set up automatically by `setup.sh`. If you skip setup, all modes still work — you just won't be able to generate PDF research briefs.

---

## What it does

- **Profiles you** — one-time interview covering your subjects, interests, goals, and constraints
- **Researches courses** — based on your confirmed interests via web search, not a hardcoded list
- **Compares universities** — subject rankings (not overall), NSS scores, graduate outcomes
- **European options** — country-by-country breakdown including Germany (free tuition at most public unis), TU Delft, ETH Zurich
- **Shortlist strategy** — builds your UCAS 5 choices with an honest reach/target/safe split
- **Personal statement coaching** — guides you through the 2026 three-question format
- **Tracks your progress** — file-based (Claude Code) or copy-paste summary block (Claude.ai)
