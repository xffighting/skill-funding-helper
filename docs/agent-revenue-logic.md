# Agent Revenue Logic

Skill Funding Helper is designed for AI Agent use, not just for README decoration.

The important artifact is `skill-funding.json`. It lets an Agent understand how a subscribed, copied, or bundled skill wants to handle attribution and support.

## Core flow

1. Agent discovers or uses a `SKILL.md`.
2. Agent checks whether `skill-funding.json` exists near the skill or at the repository root.
3. Agent reads original author metadata.
4. Agent checks whether attribution is required.
5. Agent checks the configured revenue route.
6. Agent shows support options only when relevant, such as when the user asks how to support the author, requests paid setup, or uses the skill in a commercial workflow.

## Revenue routes

### Tips and donations

Best for open source skills that remain free to use.

The Agent can say that the skill was created by the original author and show a GitHub Sponsors, Ko-fi, Polar, Open Collective, Patreon, or custom support link.

### Pay per use

Best for hosted skill marketplaces or managed agent systems.

The project does not charge users directly. It stores a public external checkout URL and a clear unit such as `successful skill run`.

The Agent must ask for explicit confirmation before any paid use route appears.

### Paid support

Best for implementation help, team onboarding, customization, debugging, and workflow design.

The Agent can show this route when a user asks for help adapting the skill to a real repository or company workflow.

### Commercial license

Best when teams embed a skill into a paid product, private agent platform, or managed automation system.

The Agent can route commercial questions to a license page or contact form.

## Safety boundary

This project does not process payments, store payment credentials, or enforce entitlement checks.

If a maintainer wants real billing, they should use a payment provider or marketplace outside this skill. Skill Funding Helper can describe the policy and link to that provider, but it should not become the provider.

