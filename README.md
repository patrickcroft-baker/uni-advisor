# Uni Advisor — Claude Code Skill

A Claude Code skill that acts as a personal university advisor. Helps you research courses, compare universities, explore European options, build a UCAS shortlist, and work on your personal statement.

Built for UK Year 12/13 students applying via UCAS, with full coverage of European university options. Everything is embedded in a single file — no separate downloads needed.

---

## Install

One command:

```bash
mkdir -p ~/.claude/skills/uni-advisor && curl -o ~/.claude/skills/uni-advisor/SKILL.md https://raw.githubusercontent.com/PatrickCroft-Baker/uni-advisor/main/uni-advisor/SKILL.md
```

Then open Claude Code and type:

```
/uni-advisor
```

That's it. On first use it will ask where to save your progress, then run through a short profile interview. After that it picks up where you left off every session.

---

## What it does

- **Profiles you** — one-time interview covering your subjects, interests, goals, and constraints
- **Researches courses** — maps your A-levels to available degrees with specific entry requirements and rankings
- **Compares universities** — subject rankings (not overall), NSS scores, graduate outcomes
- **European options** — country-by-country breakdown including Germany (free tuition), TU Delft, ETH Zurich
- **Shortlist strategy** — builds your UCAS 5 choices with an honest reach/target/safe split
- **Personal statement coaching** — guides you through the new 2026 three-question format
- **Tracks your progress** — updates a profile file every session so it always knows where you left off

---

## Requirements

- [Claude Code](https://claude.ai/code) installed
- A folder on your computer to store your progress (Obsidian vault or any plain folder works)
