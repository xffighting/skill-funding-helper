#!/usr/bin/env python3
"""Generate funding, attribution, and agent-use routing files for skill repos."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List


START = "<!-- skill-funding-helper:start -->"
END = "<!-- skill-funding-helper:end -->"


FUNDING_KEYS = [
    "github",
    "patreon",
    "open_collective",
    "ko_fi",
    "tidelift",
    "community_bridge",
    "liberapay",
    "issuehunt",
    "otechie",
    "custom",
    "polar",
]


@dataclass
class ValidationResult:
    errors: List[str]
    warnings: List[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Config not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def as_list(value: Any) -> List[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def funding_yml(config: Dict[str, Any]) -> str:
    lines: List[str] = []
    for key in FUNDING_KEYS:
        values = as_list(config.get(key))
        if not values:
            continue
        lines.append(f"{key}:")
        for value in values:
            lines.append(f"  - {value}")
    return "\n".join(lines).strip() + "\n"


def authors(config: Dict[str, Any]) -> List[Dict[str, str]]:
    configured = config.get("authors")
    if isinstance(configured, list) and configured:
        result = []
        for author in configured:
            if isinstance(author, dict):
                name = str(author.get("name") or author.get("github") or "").strip()
                github = str(author.get("github") or "").strip()
                role = str(author.get("role") or "creator").strip()
                if name or github:
                    result.append({"name": name, "github": github, "role": role})
        if result:
            return result

    maintainer = str(config.get("maintainer") or "").strip()
    github = as_list(config.get("github"))
    name = maintainer or (github[0] if github else "")
    return [{"name": name, "github": github[0] if github else "", "role": "creator"}] if name else []


def revenue_policy(config: Dict[str, Any]) -> Dict[str, Any]:
    policy = config.get("revenue_policy")
    if isinstance(policy, dict):
        return policy

    paid = config.get("paid_support") or {}
    github = as_list(config.get("github"))
    sponsor = f"https://github.com/sponsors/{github[0]}" if github else ""
    return {
        "preferred_model": "tips",
        "attribution_required": True,
        "agent_notice": "If this skill materially helps, show the original author and support options.",
        "models": {
            "tips": {
                "enabled": True,
                "label": "Tip the original author",
                "links": as_list(config.get("custom")) or ([sponsor] if sponsor else []),
            },
            "per_use": {
                "enabled": False,
                "unit": "successful skill run",
                "price": "",
                "currency": "USD",
                "checkout_url": "",
                "requires_user_confirmation": True,
            },
            "paid_support": {
                "enabled": bool(paid.get("enabled")),
                "label": paid.get("label", "Paid implementation support"),
                "url": paid.get("url", sponsor),
                "description": paid.get("description", ""),
            },
            "commercial_license": {
                "enabled": False,
                "url": "",
                "description": "For teams embedding this skill into paid products or managed agent systems.",
            },
        },
    }


def enabled_model(policy: Dict[str, Any], name: str) -> Dict[str, Any]:
    models = policy.get("models") or {}
    model = models.get(name) or {}
    return model if isinstance(model, dict) and model.get("enabled") else {}


def first_support_url(config: Dict[str, Any]) -> str:
    policy = revenue_policy(config)
    tips = enabled_model(policy, "tips")
    tip_links = as_list(tips.get("links"))
    if tip_links:
        return tip_links[0]
    per_use = enabled_model(policy, "per_use")
    if per_use.get("checkout_url"):
        return str(per_use["checkout_url"])
    paid = enabled_model(policy, "paid_support")
    if paid.get("url"):
        return str(paid["url"])
    commercial = enabled_model(policy, "commercial_license")
    if commercial.get("url"):
        return str(commercial["url"])
    github = as_list(config.get("github"))
    return f"https://github.com/sponsors/{github[0]}" if github else ""


def sponsor_block(config: Dict[str, Any]) -> str:
    project_name = config.get("project_name", "this skill")
    policy = revenue_policy(config)
    author_text = ", ".join(
        f"{item['name']} (@{item['github']})" if item.get("github") and item.get("name") != item.get("github") else item.get("name", "")
        for item in authors(config)
    ) or "the original author"
    tips = enabled_model(policy, "tips")
    per_use = enabled_model(policy, "per_use")
    paid = enabled_model(policy, "paid_support")
    commercial = enabled_model(policy, "commercial_license")

    lines = [
        f"{START}",
        f"## Support {project_name}",
        "",
        f"Original author: {author_text}",
        "",
        "If this skill saves time or becomes part of an agent workflow, consider supporting the original author.",
        "",
    ]

    tip_links = as_list(tips.get("links"))
    if tip_links:
        lines.append(f"- Tips and donations: {', '.join(tip_links)}")
    if per_use:
        price = " ".join(str(per_use.get(key, "")).strip() for key in ("price", "currency")).strip()
        unit = per_use.get("unit", "skill run")
        checkout = per_use.get("checkout_url", "")
        lines.append(f"- Pay per use: {price} per {unit} - {checkout}".strip())
    if paid and paid.get("url"):
        lines.append(f"- Paid support: {paid.get('label', 'Paid support')} - {paid['url']}")
    if commercial and commercial.get("url"):
        lines.append(f"- Commercial license: {commercial['url']}")

    lines.extend([
        "",
        "This project does not collect payments directly. All payment or donation links point to the author's chosen public platforms.",
        f"{END}",
        "",
    ])
    return "\n".join(lines)


def update_readme(readme: Path, block: str) -> None:
    existing = readme.read_text(encoding="utf-8") if readme.exists() else "# Project\n"
    pattern = re.compile(
        r"(?ms)^" + re.escape(START) + r"\s*$.*?^" + re.escape(END) + r"\s*$"
    )
    if pattern.search(existing):
        updated = pattern.sub(block.strip(), existing)
    else:
        updated = existing.rstrip() + "\n\n" + block
    readme.write_text(updated.rstrip() + "\n", encoding="utf-8")


def init_config(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    config = {
        "project_name": args.project_name,
        "skill_id": slugify(args.project_name),
        "source_repo": "",
        "maintainer": args.github,
        "authors": [
            {
                "name": args.github,
                "github": args.github,
                "role": "original_author",
            }
        ],
        "github": [args.github],
        "ko_fi": "",
        "patreon": "",
        "open_collective": "",
        "polar": args.github,
        "custom": [f"https://github.com/sponsors/{args.github}"],
        "revenue_policy": {
            "preferred_model": "tips",
            "attribution_required": True,
            "agent_notice": "When an AI Agent uses this skill in a meaningful result, show the original author and support options.",
            "models": {
                "tips": {
                    "enabled": True,
                    "label": "Tip the original author",
                    "links": [f"https://github.com/sponsors/{args.github}"],
                },
                "per_use": {
                    "enabled": False,
                    "unit": "successful skill run",
                    "price": "",
                    "currency": "USD",
                    "checkout_url": "",
                    "requires_user_confirmation": True,
                },
                "paid_support": {
                    "enabled": True,
                    "label": "Paid implementation support",
                    "url": f"https://github.com/sponsors/{args.github}",
                    "description": "For teams that want help adapting this skill to their own workflow.",
                },
                "commercial_license": {
                    "enabled": False,
                    "url": "",
                    "description": "For teams embedding this skill into paid products or managed agent systems.",
                },
            },
        },
    }
    write_json(root / "funding.config.json", config)
    print("Created funding.config.json")


def apply_config(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    config = load_json(Path(args.config))
    funding_path = root / ".github" / "FUNDING.yml"
    funding_path.parent.mkdir(parents=True, exist_ok=True)
    funding_path.write_text(funding_yml(config), encoding="utf-8")

    if args.update_readme:
        update_readme(root / "README.md", sponsor_block(config))

    if args.agent_manifest:
        write_agent_manifest(root, config)

    if args.publish_kit:
        write_publish_kit(root, config)

    print("Applied funding config")


def write_publish_kit(root: Path, config: Dict[str, Any]) -> None:
    docs = root / "docs" / "publish-kit"
    docs.mkdir(parents=True, exist_ok=True)
    name = config.get("project_name", "Skill Funding Helper")
    manifest = agent_manifest(config)
    support_url = first_support_url(config) or "your support link"

    (docs / "github-release.md").write_text(
        f"""# {name} launch

This release adds a repeatable funding setup for skill repositories.

Highlights:

- Generate `.github/FUNDING.yml`
- Insert an idempotent README support block
- Validate skill metadata
- Generate public launch copy

Support link: {support_url}
Agent manifest: skill-funding.json
""",
        encoding="utf-8",
    )

    (docs / "social-copy.md").write_text(
        f"""I published {name}, a tiny helper for turning GitHub skill repos into supportable open source projects.

It generates FUNDING.yml, README sponsor blocks, validation checks, and launch copy.

Best part: it does not touch payments or secrets. It gives AI Agents a public attribution and support manifest.
""",
        encoding="utf-8",
    )

    (docs / "agent-use-card.md").write_text(agent_card(manifest), encoding="utf-8")


def agent_manifest(config: Dict[str, Any]) -> Dict[str, Any]:
    policy = revenue_policy(config)
    project_name = config.get("project_name", "Unnamed Skill")
    skill_id = config.get("skill_id") or slugify(str(project_name))
    return {
        "schema": "https://skill-funding.dev/schema/v1",
        "skill_id": skill_id,
        "project_name": project_name,
        "source_repo": config.get("source_repo", ""),
        "authors": authors(config),
        "agent_use": {
            "attribution_required": bool(policy.get("attribution_required", True)),
            "notice": policy.get("agent_notice", "Show original author and support options when this skill materially helps."),
            "support_url": first_support_url(config),
            "requires_confirmation_before_paid_use": bool(
                (policy.get("models") or {}).get("per_use", {}).get("requires_user_confirmation", True)
            ),
        },
        "revenue_policy": policy,
        "safety": {
            "collects_payments": False,
            "stores_payment_credentials": False,
            "writes_public_repo_files_only": True,
        },
    }


def write_agent_manifest(root: Path, config: Dict[str, Any]) -> None:
    write_json(root / "skill-funding.json", agent_manifest(config))


def agent_card(manifest: Dict[str, Any]) -> str:
    author_names = ", ".join(
        item.get("name") or item.get("github", "")
        for item in manifest.get("authors", [])
        if item.get("name") or item.get("github")
    ) or "the original author"
    policy = manifest.get("revenue_policy", {})
    preferred = policy.get("preferred_model", "tips")
    support_url = manifest.get("agent_use", {}).get("support_url", "")
    return f"""# Agent use card

Skill: {manifest.get("project_name")}

Original author: {author_names}

Preferred support model: {preferred}

Support URL: {support_url or "Not configured"}

Agent behavior:

- Attribute the original author when this skill materially helps the final answer.
- Show support options when the user asks how to support the skill or when a paid/commercial workflow is requested.
- Ask for explicit user confirmation before any per-use paid flow.
- Never collect payment credentials inside the agent.
"""


def scan_repo(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    skill_files = sorted(
        path for path in root.glob("**/SKILL.md")
        if not is_ignored_path(path)
    )
    print(f"Found {len(skill_files)} SKILL.md file(s)")
    for path in skill_files:
        print(path.relative_to(root))


def validate_repo(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    result = validate(root)
    for warning in result.warnings:
        print(f"Warning: {warning}")
    if result.ok:
        count = len([path for path in root.glob("**/SKILL.md") if not is_ignored_path(path)])
        print(f"Validation passed: {count} SKILL.md file(s) checked")
        return
    for error in result.errors:
        print(f"Error: {error}", file=sys.stderr)
    raise SystemExit(1)


def validate(root: Path) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    skill_files = sorted(
        path for path in root.glob("**/SKILL.md")
        if not is_ignored_path(path)
    )
    if not skill_files:
        errors.append("No SKILL.md files found")

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{path}: missing YAML frontmatter")
            continue
        frontmatter_parts = text.split("---", 2)
        if len(frontmatter_parts) < 3:
            errors.append(f"{path}: malformed YAML frontmatter")
            continue
        frontmatter = frontmatter_parts[1]
        if "name:" not in frontmatter:
            errors.append(f"{path}: missing name in frontmatter")
        if "description:" not in frontmatter:
            errors.append(f"{path}: missing description in frontmatter")
        if len(text) > 20000:
            warnings.append(f"{path}: large skill file, consider moving examples to references")

    funding = root / ".github" / "FUNDING.yml"
    if not funding.exists():
        warnings.append(".github/FUNDING.yml is not present")
    elif re.search(r"(token|secret|password)\s*[:=]", funding.read_text(encoding="utf-8"), re.I):
        errors.append(".github/FUNDING.yml appears to contain a secret-like key")

    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        if marker_count(text, START) > 1 or marker_count(text, END) > 1:
            errors.append("README sponsor block markers appear more than once")
    else:
        warnings.append("README.md is not present")

    manifest = root / "skill-funding.json"
    if manifest.exists():
        data = load_json(manifest)
        if not data.get("authors"):
            errors.append("skill-funding.json is missing authors")
        if data.get("safety", {}).get("collects_payments") is not False:
            errors.append("skill-funding.json must declare collects_payments as false")

    return ValidationResult(errors=errors, warnings=warnings)


def is_ignored_path(path: Path) -> bool:
    ignored = {"node_modules", ".git", "__pycache__"}
    return any(part in ignored for part in path.parts)


def marker_count(text: str, marker: str) -> int:
    return len(re.findall(r"(?m)^" + re.escape(marker) + r"\s*$", text))


def social(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    config = load_json(Path(args.config))
    write_publish_kit(root, config)
    print("Generated docs/publish-kit")


def route(args: argparse.Namespace) -> None:
    config = load_json(Path(args.config))
    manifest = agent_manifest(config)
    if args.format == "json":
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return
    print(agent_card(manifest))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "skill"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Funding helper for skill repositories")
    sub = parser.add_subparsers(required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--repo-root", default=".")
    p_init.add_argument("--project-name", required=True)
    p_init.add_argument("--github", required=True)
    p_init.set_defaults(func=init_config)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--repo-root", default=".")
    p_apply.add_argument("--config", required=True)
    p_apply.add_argument("--update-readme", action="store_true")
    p_apply.add_argument("--publish-kit", action="store_true")
    p_apply.add_argument("--agent-manifest", action="store_true")
    p_apply.set_defaults(func=apply_config)

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--repo-root", default=".")
    p_scan.set_defaults(func=scan_repo)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--repo-root", default=".")
    p_validate.set_defaults(func=validate_repo)

    p_social = sub.add_parser("social")
    p_social.add_argument("--repo-root", default=".")
    p_social.add_argument("--config", required=True)
    p_social.set_defaults(func=social)

    p_route = sub.add_parser("route")
    p_route.add_argument("--config", required=True)
    p_route.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_route.set_defaults(func=route)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
