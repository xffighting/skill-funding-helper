# Skill Funding Helper 项目介绍 / Project Introduction

![Skill Funding Helper cover](../assets/wechat-cover.png)

## 视觉概览 / Visual Overview

AI Agent 读取 Skill 仓库里的公开配置，再把署名、支持方式和安全边界展示给用户。

An AI Agent reads the public configuration inside a skill repository, then presents attribution, support routes, and safety boundaries to the user.

![Agent route](../assets/wechat-agent-route.png)

项目支持打赏、按次收费、付费支持和商业授权四种收益路径。

The project supports four revenue routes: tips, pay-per-use, paid support, and commercial licensing.

![Revenue routes](../assets/wechat-revenue-models.png)

所有生成内容都应该是公开文件，不包含支付密钥、银行信息或静默计费逻辑。

All generated content should remain public repository data, with no payment secrets, banking information, or silent metering logic.

![Safety boundaries](../assets/wechat-safety-boundary.png)

## 中文

### 一句话介绍

Skill Funding Helper 是一个面向 GitHub Skill 仓库和 AI Agent 工作流的开源工具，帮助原作者把署名、打赏、按次收费、付费支持和商业授权路径整理成机器可读、用户可见、边界清楚的公开文件。

### 为什么需要它

越来越多的 Skill 不只是提示词，而是一套可复用的工作方法。它们可能包含审查流程、写作判断、项目发布步骤、客户跟进模板、代码排查经验，或者团队内部 SOP。

当这些 Skill 被复制、订阅、安装，甚至被 AI Agent 自动调用时，原作者很容易从使用链路里消失。

Skill Funding Helper 解决的就是这件事。

它让一个 Skill 仓库可以公开说明：

- 原作者是谁
- Agent 使用 Skill 时是否需要署名
- 用户如何打赏或赞助原作者
- 哪些场景适合按次收费
- 哪些服务属于付费支持
- 商业使用应该走什么授权路径
- Agent 在涉及付款时必须遵守哪些安全边界

### 它会生成什么

- `skill-funding.json`：给 AI Agent 读取的收益与署名 manifest
- `.github/FUNDING.yml`：GitHub Sponsor Button 配置
- README 支持区块：给普通访问者看的支持入口
- `funding.config.json`：本地配置模板
- `docs/publish-kit`：GitHub Release、社交平台、公众号发布文案
- Agent use card：说明 Agent 如何展示署名和支持路径
- 校验工具：检查 Skill 元信息和资金配置是否完整

### AI Agent 使用逻辑

AI Agent 在使用某个订阅或复制来的 Skill 时，可以先读取 `skill-funding.json`。

它会看到原作者、署名要求、公开支持链接、付费支持入口和商业授权说明。

如果用户问“怎么支持这个 Skill 的作者”，Agent 可以展示 manifest 里配置的公开链接。

如果启用了按次付费，Agent 必须先向用户确认，再展示或引导对应付款路径。

如果用户想把 Skill 用在商业产品里，Agent 应该提示用户查看商业授权说明，而不是默认允许无限制使用。

### 支持的收益路径

- 打赏和捐赠：适合轻量支持，比如 GitHub Sponsors、Ko-fi、Buy Me a Coffee、Open Collective
- 按次收费：适合一次性高价值结果，比如报告生成、项目审查、发布包制作
- 付费支持：适合部署、定制、培训、接入和调试
- 商业授权：适合团队把 Skill 嵌入商业产品、托管 Agent 系统或客户交付流程

### 安全边界

Skill Funding Helper 不处理支付，不保存 token，不写入付款密钥，不做静默计费，也不替用户自动完成付费流程。

它只生成可以公开放进 GitHub 仓库的文件。所有支付、赞助、授权和服务链接都应该指向作者自己选择的公开平台。

### 快速开始

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name 'My Useful Skill' --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

### 适合谁使用

- 正在发布 GitHub Skill 的作者
- 正在构建 AI Agent 能力仓库的个人或团队
- 希望给开源 Skill 增加赞助入口的维护者
- 希望把 Skill 接入商业服务但需要边界说明的团队
- 想让 Agent 尊重原作者署名和支持路径的开发者

## English

### One-line Introduction

Skill Funding Helper is an open source toolkit for GitHub-hosted skills and AI Agent workflows. It helps original authors publish attribution, tips, pay-per-use, paid support, and commercial licensing routes as public files that both humans and agents can understand.

### Why It Exists

Many skills are no longer simple prompts. They are reusable operating knowledge: review workflows, writing judgment, release processes, customer follow-up templates, debugging routines, or internal SOPs.

When these skills are copied, subscribed to, installed, or called by AI Agents, the original author can easily disappear from the usage path.

Skill Funding Helper makes that path explicit.

It lets a skill repository state:

- Who the original author is
- Whether attribution is required when an Agent uses the skill
- How users can tip or sponsor the author
- Which scenarios are suitable for pay-per-use
- What belongs to paid support
- How commercial licensing should be handled
- Which safety rules apply when money is involved

### What It Generates

- `skill-funding.json`: an AI Agent-readable revenue and attribution manifest
- `.github/FUNDING.yml`: GitHub Sponsor Button configuration
- README support block: a visible support section for repository visitors
- `funding.config.json`: a local starter configuration
- `docs/publish-kit`: launch copy for GitHub Releases, social posts, and WeChat
- Agent use card: guidance for attribution and support routing
- Validator: checks skill metadata and funding config hygiene

### AI Agent Flow

Before using a subscribed or copied skill, an AI Agent can read `skill-funding.json`.

The manifest tells the Agent who created the skill, when attribution should be shown, where public support links live, and how paid support or commercial licensing should be presented.

If a user asks how to support the skill author, the Agent can show the configured public support route.

If pay-per-use is enabled, the Agent must ask for explicit user confirmation before showing or initiating any paid checkout flow.

If the user wants to embed the skill into a commercial product, the Agent should point them to the commercial licensing policy instead of assuming unrestricted use.

### Revenue Routes

- Tips and donations: lightweight support through platforms such as GitHub Sponsors, Ko-fi, Buy Me a Coffee, or Open Collective
- Pay per use: one-time paid actions such as report generation, project review, or launch kit creation
- Paid support: implementation, customization, onboarding, training, and debugging
- Commercial licensing: for teams embedding a skill into paid products, managed Agent systems, or client delivery workflows

### Safety Boundaries

Skill Funding Helper does not process payments, store tokens, write payment secrets, meter usage silently, or complete paid flows on behalf of users.

It only generates public repository files. All payment, sponsorship, licensing, and support links should point to public platforms chosen by the original author.

### Quick Start

```bash
python3 scripts/skill_funding.py init --repo-root . --project-name 'My Useful Skill' --github your-github-user
python3 scripts/skill_funding.py apply --repo-root . --config funding.config.json --update-readme --publish-kit --agent-manifest
python3 scripts/skill_funding.py route --config funding.config.json --format markdown
python3 scripts/skill_funding.py validate --repo-root .
```

### Who It Is For

- Authors publishing GitHub-hosted skills
- Individuals or teams building AI Agent skill libraries
- Maintainers who want clear sponsorship routes for open source skills
- Teams that need commercial boundaries before embedding skills into paid workflows
- Developers who want Agents to respect original-author attribution and support paths
