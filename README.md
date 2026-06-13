# Skill Funding Helper

Turn a GitHub-hosted skill into an agent-readable, supportable open source product.

![Project preview](assets/effect-home.png)

Skill Funding Helper helps maintainers describe who created a skill, how AI Agents should attribute it, and how users can support the original author through tips, pay-per-use links, paid support, or commercial licensing.

It does not process payments, store tokens, or enforce entitlements. It generates public files that GitHub, readers, and AI Agents can safely inspect.

## Why this exists

Good skills are becoming reusable work products. They encode workflows, judgment, templates, and repeated operating knowledge. But many skill repositories stop at `SKILL.md`, with no original-author revenue policy, no attribution signal for AI Agents, no support path, and no launch copy.

This project gives maintainers a repeatable publishing kit and a machine-readable `skill-funding.json` manifest.

## What it generates

- `skill-funding.json` for AI Agent attribution and support routing
- `.github/FUNDING.yml` for GitHub Sponsor Button support
- A README sponsor block that can be inserted safely
- A `funding.config.json` starter file
- An Agent use card explaining how a subscribed skill should be credited and supported
- A launch kit for GitHub, X, LinkedIn, and WeChat
- A validator for skill metadata and funding config hygiene

## Revenue models

The project supports four public revenue routes:

- Tips and donations after a skill helps
- Pay per use through an external checkout link, with explicit user confirmation
- Paid support for implementation, customization, onboarding, or debugging
- Commercial licensing for teams embedding a skill into paid products or managed agent systems

Supported public link platforms include GitHub Sponsors, Patreon, Open Collective, Ko-fi, Buy Me a Coffee, Liberapay, IssueHunt, thanks.dev, Tidelift, Polar, and custom URLs.

## Quick start

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name "My Useful Skill" --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

The `route` command prints the support and attribution card an AI Agent can show or reason over.

For JSON output:

```bash
python3 scripts/skill_funding.py route --config funding.config.json --format json
```

## Repository layout

```text
skills/skill-funding-helper/SKILL.md
.claude/skills/skill-funding-helper/SKILL.md
.agents/skills/skill-funding-helper/SKILL.md
scripts/skill_funding.py
templates/README.sponsor-block.md
examples/basic/funding.config.json
skill-funding.json
docs/wechat-article.md
docs/ui-redesign-notes.md
index.html
assets/
```

The repeated skill paths make the project easier to copy into different agent ecosystems.

## Agent logic

The generated `skill-funding.json` is the core Agent contract. It answers four questions:

- Who is the original author?
- Is attribution required when this skill materially helps?
- Which support route should be shown for tips, per-use payment, paid support, or commercial use?
- What safety boundaries apply?

An AI Agent using a subscribed or copied skill can read this manifest before final output. If the user asks how to support the skill, the agent routes them to the configured public link. If pay per use is enabled, the agent must ask before showing or initiating any paid checkout flow.

## Visual redesign

The project page has been redesigned around three user decisions instead of a generic landing page.

![Flow overview](assets/product-flow.svg)

The first screen explains the value, the center of the page shows the generated files, and the lower sections show how the publishing kit travels from local config to GitHub Sponsor Button to public launch copy.

## Safe boundaries

Skill Funding Helper does not collect money, authenticate with payment providers, meter usage silently, or write secret tokens. It only writes public repository files from a local config.

That boundary is deliberate. A funding helper should make original-author support visible and maintainable, not become a payment processor.

<!-- skill-funding-helper:start -->
## Support Skill Funding Helper

Original author: 寸言 (@xffighting)

If this skill saves time or becomes part of an agent workflow, consider supporting the original author.

- Tips and donations: https://github.com/sponsors/xffighting
- Paid support: Paid setup support - https://github.com/sponsors/xffighting

This project does not collect payments directly. All payment or donation links point to the author's chosen public platforms.
<!-- skill-funding-helper:end -->
## Sponsor Block Markers

When `--update-readme` is enabled, the script writes between these markers:

`&lt;!-- skill-funding-helper:start --&gt;` and `&lt;!-- skill-funding-helper:end --&gt;`

This makes repeated runs idempotent and keeps the rest of your README untouched.

## Docs

- [公众号文章](docs/wechat-article.md)
- [Agent revenue logic](docs/agent-revenue-logic.md)
- [UI redesign notes](docs/ui-redesign-notes.md)
- [Launch checklist](docs/launch-checklist.md)
- [Quality report](docs/quality-report.md)

## License

MIT
