---
name: skill-funding-helper
description: Use when a GitHub-hosted skill, agent skill, Claude Code skill, Codex skill, or OpenClaw skill needs sponsor links, donation links, paid support copy, GitHub FUNDING.yml, README support blocks, launch copy, or funding configuration validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project.

Use this skill when the user wants to add funding, donations, sponsorship, or paid support to a repository that contains `SKILL.md` files.

## What to do

1. Inspect the repository layout and find every `SKILL.md`.
2. Ask for missing maintainer handles only when they cannot be inferred.
3. Generate or update `funding.config.json`.
4. Generate `.github/FUNDING.yml`.
5. Insert or update the README support block between stable markers.
6. Generate launch copy when the user is preparing a public release.
7. Validate that no secrets are written into public funding files.

## Boundaries

Do not collect payment credentials.

Do not ask for private keys, payment API tokens, bank details, or platform passwords.

Do not claim the project is officially sponsored unless the user provides that exact wording.

Prefer public platform links such as GitHub Sponsors, Ko-fi, Patreon, Open Collective, Buy Me a Coffee, Polar, thanks.dev, Tidelift, Liberapay, IssueHunt, or a custom support page.

## Default commands

Use the bundled script when available.

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name "My Useful Skill" --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit
python3 scripts/skill_funding.py validate --repo-root .
```

## README copy style

Keep funding copy plain and transparent.

Good copy says what support pays for, where the money goes, and what paid support includes.

Avoid pressure tactics. A good open source support link should feel like a clean door, not a pop-up.

