---
name: skill-funding-helper
description: Use when a GitHub-hosted skill, agent skill, Claude Code skill, Codex skill, or OpenClaw skill needs sponsor links, donation links, paid support copy, GitHub FUNDING.yml, README support blocks, launch copy, or funding configuration validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project.

Find `SKILL.md` files, generate funding config, create `.github/FUNDING.yml`, update README support copy, and validate that public funding files do not contain secrets.

Default command path:

```bash
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit
python3 scripts/skill_funding.py validate --repo-root .
```

Keep the boundary clear. This skill configures links and copy. It does not process payments.

