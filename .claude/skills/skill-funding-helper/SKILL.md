---
name: skill-funding-helper
description: Use when an AI Agent or GitHub-hosted skill needs attribution, original-author revenue routing, sponsor links, donation links, pay-per-use policy, paid support copy, commercial license copy, GitHub FUNDING.yml, README support blocks, launch copy, agent manifests, or funding validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project that AI Agents can understand and route correctly.

Use this skill when the user wants to add funding, donations, sponsorship, attribution, pay-per-use policy, paid support, or commercial licensing to a repository that contains `SKILL.md` files.

Follow the repository script first when it exists.

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name "My Useful Skill" --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

Generate `skill-funding.json` so other AI Agents can identify the original author, attribution policy, donation links, pay-per-use policy, paid support, and commercial license options.

Never request payment credentials or private platform tokens. Only generate public repository files and public support copy.
