---
name: skill-funding-helper
description: Use when an AI Agent or GitHub-hosted skill needs attribution, original-author revenue routing, sponsor links, donation links, pay-per-use policy, paid support copy, commercial license copy, GitHub FUNDING.yml, README support blocks, launch copy, agent manifests, or funding validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project that AI Agents can understand and route correctly.

Find `SKILL.md` files, identify the original author, generate funding config, create `skill-funding.json`, create `.github/FUNDING.yml`, update README support copy, and validate that public funding files do not contain secrets.

Default command path:

```bash
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

Keep the boundary clear. This skill configures attribution, links, support policy, and copy. It does not process payments or silently meter paid usage.
