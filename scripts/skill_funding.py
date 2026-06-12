#!/usr/bin/env python3
"""Generate funding files and launch copy for skill repositories."""

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


def sponsor_block(config: Dict[str, Any]) -> str:
    project_name = config.get("project_name", "this skill")
    github = as_list(config.get("github"))
    custom = as_list(config.get("custom"))
    paid = config.get("paid_support") or {}

    github_sponsors = ", ".join(
        f"https://github.com/sponsors/{name}" for name in github
    ) or "Not configured yet"
    custom_links = ", ".join(custom) or "Not configured yet"
    if paid.get("enabled") and paid.get("url"):
        paid_support = f"{paid.get('label', 'Paid support')} - {paid['url']}"
    else:
        paid_support = "Not configured yet"

    return f"""{START}
## Support {project_name}

If this skill saves you time, consider supporting ongoing maintenance.

- GitHub Sponsors: {github_sponsors}
- Paid support: {paid_support}
- Other links: {custom_links}

This project does not collect payments directly. All support links point to the maintainer's chosen platforms.
{END}
"""


def update_readme(readme: Path, block: str) -> None:
    existing = readme.read_text(encoding="utf-8") if readme.exists() else "# Project\n"
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(existing):
        updated = pattern.sub(block.strip(), existing)
    else:
        updated = existing.rstrip() + "\n\n" + block
    readme.write_text(updated.rstrip() + "\n", encoding="utf-8")


def init_config(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    config = {
        "project_name": args.project_name,
        "maintainer": args.github,
        "github": [args.github],
        "ko_fi": "",
        "patreon": "",
        "open_collective": "",
        "polar": args.github,
        "custom": [f"https://github.com/sponsors/{args.github}"],
        "paid_support": {
            "enabled": True,
            "label": "Paid setup support",
            "url": f"https://github.com/sponsors/{args.github}",
            "description": "For teams that want help adapting this skill to their own workflow.",
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

    if args.publish_kit:
        write_publish_kit(root, config)

    print("Applied funding config")


def write_publish_kit(root: Path, config: Dict[str, Any]) -> None:
    docs = root / "docs" / "publish-kit"
    docs.mkdir(parents=True, exist_ok=True)
    name = config.get("project_name", "Skill Funding Helper")
    github = as_list(config.get("github"))
    sponsor = f"https://github.com/sponsors/{github[0]}" if github else "your sponsor link"
    paid = config.get("paid_support") or {}
    paid_url = paid.get("url") or sponsor

    (docs / "github-release.md").write_text(
        f"""# {name} launch

This release adds a repeatable funding setup for skill repositories.

Highlights:

- Generate `.github/FUNDING.yml`
- Insert an idempotent README support block
- Validate skill metadata
- Generate public launch copy

Support link: {sponsor}
Paid setup: {paid_url}
""",
        encoding="utf-8",
    )

    (docs / "social-copy.md").write_text(
        f"""I published {name}, a tiny helper for turning GitHub skill repos into supportable open source projects.

It generates FUNDING.yml, README sponsor blocks, validation checks, and launch copy.

Best part: it does not touch payments or secrets. It only writes public repo files.
""",
        encoding="utf-8",
    )


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
        count = len(list(root.glob("**/SKILL.md")))
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
        if "name:" not in text.split("---", 2)[1]:
            errors.append(f"{path}: missing name in frontmatter")
        if "description:" not in text.split("---", 2)[1]:
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
        if text.count(START) > 1 or text.count(END) > 1:
            errors.append("README sponsor block markers appear more than once")
    else:
        warnings.append("README.md is not present")

    return ValidationResult(errors=errors, warnings=warnings)


def is_ignored_path(path: Path) -> bool:
    ignored = {"node_modules", ".git", "__pycache__"}
    return any(part in ignored for part in path.parts)


def social(args: argparse.Namespace) -> None:
    root = Path(args.repo_root)
    config = load_json(Path(args.config))
    write_publish_kit(root, config)
    print("Generated docs/publish-kit")


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

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
