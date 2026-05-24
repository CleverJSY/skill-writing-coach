#!/usr/bin/env python3
"""Lightweight structural audit for Codex skill folders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$|^[a-z0-9]$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["SKILL.md must start with YAML frontmatter delimited by ---"]

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, ["SKILL.md frontmatter is missing the closing --- delimiter"]

    raw = text[4:end].strip()
    body = text[end + len("\n---") :].lstrip("\n")
    data: dict[str, str] = {}

    for line_no, line in enumerate(raw.splitlines(), start=2):
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"Frontmatter line {line_no} is not key: value")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value

    return data, body, errors


def audit(path: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    skill_dir = path.resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"Missing {skill_md}"], warnings, notes

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body, parse_errors = parse_frontmatter(text)
    errors.extend(parse_errors)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    allowed_keys = {"name", "description"}
    extra_keys = sorted(set(frontmatter) - allowed_keys)
    if extra_keys:
        warnings.append(f"Frontmatter has nonstandard keys: {', '.join(extra_keys)}")

    if not name:
        errors.append("Frontmatter is missing name")
    elif not NAME_RE.match(name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens only")
    elif name != skill_dir.name:
        warnings.append(f"Skill name '{name}' does not match folder name '{skill_dir.name}'")

    if not description:
        errors.append("Frontmatter is missing description")
    else:
        if len(description) < 80:
            warnings.append("Description is short; include concrete triggers and contexts")
        if not re.search(r"\b(use when|when|trigger|asks?|requests?)\b", description, re.I):
            warnings.append("Description should state when Codex should use the skill")
        if "[" in description and "TODO" in description.upper():
            errors.append("Description still contains placeholder text")

    if "TODO" in text.upper() or "[TODO" in text.upper():
        errors.append("SKILL.md still contains TODO placeholders")

    body_lines = [line for line in body.splitlines() if line.strip()]
    if len(body_lines) < 12:
        warnings.append("Body is very short; make sure it gives operational steps")
    if len(body.splitlines()) > 500:
        warnings.append("Body is long; consider moving optional detail into references/")

    for resource in ("references", "scripts", "assets"):
        resource_dir = skill_dir / resource
        if resource_dir.exists():
            files = [p for p in resource_dir.rglob("*") if p.is_file()]
            if not files:
                warnings.append(f"{resource}/ exists but is empty")
            elif resource not in body:
                warnings.append(f"{resource}/ has files but is not mentioned in SKILL.md")

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if agents_yaml.exists():
        yaml_text = agents_yaml.read_text(encoding="utf-8")
        if "default_prompt:" in yaml_text and f"${name}" not in yaml_text:
            warnings.append("agents/openai.yaml default_prompt should mention the skill as $skill-name")
        if "short_description:" not in yaml_text:
            warnings.append("agents/openai.yaml is missing short_description")
    else:
        notes.append("agents/openai.yaml is absent; this is acceptable if UI metadata is not needed")

    stray_docs = sorted(
        p.name
        for p in skill_dir.iterdir()
        if p.is_file() and p.name.lower() in {"readme.md", "changelog.md", "installation_guide.md", "quick_reference.md"}
    )
    if stray_docs:
        warnings.append(f"Consider removing auxiliary docs from skill root: {', '.join(stray_docs)}")

    return errors, warnings, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Codex skill folder.")
    parser.add_argument("skill_folder", type=Path)
    args = parser.parse_args()

    errors, warnings, notes = audit(args.skill_folder)

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    for message in notes:
        print(f"NOTE: {message}")

    if not errors and not warnings:
        print("OK: skill structure looks solid")
    elif not errors:
        print("OK: no blocking errors")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
