---
name: skill-funding-helper
description: Use when an AI Agent or GitHub-hosted skill needs attribution, original-author revenue routing, sponsor links, donation links, pay-per-use policy, paid support copy, commercial license copy, GitHub FUNDING.yml, README support blocks, launch copy, agent manifests, or funding validation.
---

# Skill Funding Helper

You help maintainers turn a skill repository into a supportable open source project that AI Agents can understand and route correctly.

Use this skill when the user wants to add funding, donations, sponsorship, pay-per-use policy, attribution, commercial licensing, or paid support to a repository that contains `SKILL.md` files.

The core idea is simple: the agent should know who created the skill, how to attribute them, and which public support options are appropriate when the skill creates value.

## What to do

1. Inspect the repository layout and find every `SKILL.md`.
2. Identify the original author, GitHub account, source repository, and preferred support model.
3. Generate or update `funding.config.json`.
4. Generate `skill-funding.json`, a machine-readable manifest for AI Agents.
5. Generate `.github/FUNDING.yml` for GitHub Sponsor Button support.
6. Insert or update the README support block between stable markers.
7. Generate launch copy and an Agent use card when the user is preparing a public release.
8. Validate that no secrets are written into public funding files.

## Revenue models

Prefer transparent public links. The skill can describe these models, but should not process payment itself.

- Tips and donations: optional support after the skill helps.
- Pay per use: a configured external checkout link, shown only after the user confirms paid use.
- Paid support: implementation, customization, debugging, onboarding, or team setup.
- Commercial license: for teams embedding the skill into paid products or managed agent systems.

When pay per use is enabled, always ask for explicit user confirmation before routing to checkout. Do not silently charge, meter, or imply that payment has happened.

## Agent behavior

When an AI Agent uses a subscribed or copied skill in a meaningful result, it should read `skill-funding.json` if present.

If attribution is required, include the original author in the final output or support section.

If the user asks how to support the skill, show the configured support route.

If the user asks for enterprise use, paid setup, or embedding into a paid workflow, show paid support or commercial license options.

## Boundaries

Do not collect payment credentials.

Do not ask for private keys, payment API tokens, bank details, or platform passwords.

Do not claim the project is officially sponsored unless the user provides that exact wording.

Do not implement real metering or entitlement checks unless the user already has a separate payment provider and explicitly asks for integration guidance.

Prefer public platform links such as GitHub Sponsors, Ko-fi, Patreon, Open Collective, Buy Me a Coffee, Polar, thanks.dev, Tidelift, Liberapay, IssueHunt, or a custom support page.

## Default commands

Use the bundled script when available.

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name "My Useful Skill" --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

## README copy style

Keep funding copy plain and transparent.

Good copy says what support pays for, where the money goes, and what paid support includes.

Avoid pressure tactics. A good open source support link should feel like a clean door, not a pop-up.
