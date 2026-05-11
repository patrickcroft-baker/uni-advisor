# Uni Advisor — Claude Code Skill

A Claude Code skill that acts as a personal university advisor. Helps you research courses, compare universities, explore European options, build a UCAS shortlist, and work on your personal statement.

Built for UK Year 12/13 students applying via UCAS, with full coverage of European university options.

---

## What it does

- **Profiles you** — runs a one-time interview to understand your subjects, interests, goals, and constraints
- **Researches courses** — maps your A-levels to available degrees with entry requirements and rankings
- **Compares universities** — subject rankings (not overall), NSS scores, graduate outcomes
- **European options** — country-by-country guide including Germany (free tuition), TU Delft, ETH Zurich
- **Shortlist strategy** — builds your UCAS 5 choices with an honest reach/target/safe split
- **Personal statement coaching** — guides you through the new 2026 three-question format
- **Tracks your progress** — updates a profile file every session so it always knows where you left off

---

## Install

### 1. Copy the skill

```bash
mkdir -p ~/.claude/skills/uni-advisor
cp uni-advisor/SKILL.md ~/.claude/skills/uni-advisor/SKILL.md
```

### 2. Set up your vault (optional but recommended)

The skill tracks your profile, shortlist, and progress in a markdown vault. If you already use Obsidian or a similar markdown folder, point it there. If not, create a simple folder:

```bash
mkdir -p ~/my-vault/wiki/sources
mkdir -p ~/my-vault/wiki/projects
```

Copy the knowledge base into your vault:

```bash
cp uni-advisor/uni-advisor-research.md ~/my-vault/wiki/sources/uni-advisor-research.md
```

### 3. Use it

Open Claude Code and type:

```
/uni-advisor
```

On first use it will ask for your vault path, then run through a short profile interview. After that it picks up where you left off every session.

---

## What's included

| File | Purpose |
|------|---------|
| `uni-advisor/SKILL.md` | The skill itself — install to `~/.claude/skills/uni-advisor/` |
| `uni-advisor/uni-advisor-research.md` | Knowledge base — UCAS process, European fees, rankings guide, personal statement format. Place in your vault at `wiki/sources/` |

---

## Knowledge base covers

- Full UCAS process and deadlines
- New 2026 personal statement format (3 questions, not the old essay)
- European universities country by country — Germany (free), Netherlands, Switzerland, Sweden, Denmark, France
- How to use university rankings properly (subject vs overall)
- A-level profile mapping to courses
- Common application mistakes
- Super-curricular recommendations

---

## Requirements

- [Claude Code](https://claude.ai/code) CLI installed
- A markdown vault folder (Obsidian or just a plain folder works)
