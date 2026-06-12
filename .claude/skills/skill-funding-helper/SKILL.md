---
name: skill-funding-helper
description: Use when a GitHub-hosted skill, agent skill, Claude Code skill, Codex skill, or OpenClaw skill needs sponsor links, donation links, paid support copy, GitHub FUNDING.yml, README support blocks, launch copy, or funding configuration validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project.

Use this skill when the user wants to add funding, donations, sponsorship, or paid support to a repository that contains `SKILL.md` files.

Follow the repository script first when it exists.

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name "My Useful Skill" --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit
python3 scripts/skill_funding.py validate --repo-root .
```

Never request payment credentials or private platform tokens. Only generate public repository files and public support copy.

