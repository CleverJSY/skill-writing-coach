# Skill Writing Coach

A Codex skill for designing, writing, auditing, and improving other Codex skills.

The skill acts as a practical skill architect. It helps decide whether a workflow should become a skill, writes concise trigger descriptions, chooses when to use `references/`, `scripts/`, and `assets/`, and validates common structural issues before a skill is shipped.

## Contents

- `skill-writing-coach/SKILL.md`: the skill instructions.
- `skill-writing-coach/references/skill-patterns.md`: design patterns and review rubric.
- `skill-writing-coach/scripts/audit_skill.py`: a lightweight structural audit script.
- `skill-writing-coach/agents/openai.yaml`: optional Codex UI metadata.

## Install

Install with the Codex skill installer from this repository path:

```powershell
python scripts/install-skill-from-github.py --url https://github.com/Melancholy-A/skill-writing-coach/tree/main/skill-writing-coach
```

Or copy the `skill-writing-coach/` directory into your Codex skills directory:

```text
~/.codex/skills/skill-writing-coach
```

Restart Codex after installing so the new skill is discovered.

## Usage

Ask Codex to use the skill when creating or reviewing skills:

```text
Use $skill-writing-coach to design a Codex skill for my workflow.
```

You can also run the audit helper directly:

```powershell
python skill-writing-coach/scripts/audit_skill.py path/to/target-skill
```

## License

MIT
