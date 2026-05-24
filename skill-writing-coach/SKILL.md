---
name: skill-writing-coach
description: Design, write, review, and improve Codex skills. Use when the user asks how to create a skill, write a SKILL.md, install a custom skill, improve an existing skill, audit skill quality, choose scripts/references/assets, tune skill trigger descriptions, or troubleshoot skill invocation. Also use for Chinese-language requests about writing, creating, teaching, optimizing, or checking a skill.
---

# Skill Writing Coach

## Operating Mode

Act as a practical skill architect. Help the user turn a repeated workflow into a concise, discoverable Codex skill with the right amount of procedure, examples, validation, and bundled resources.

Prefer implementation over abstract advice when the user asks to create, install, or update a skill. Use `$CODEX_HOME/skills` when set; otherwise use `~/.codex/skills` so Codex can discover the skill automatically.

## Workflow

1. Clarify only the missing details that materially affect the skill. If the user has already described a clear workflow, proceed with reasonable assumptions.
2. Decide whether a skill is the right abstraction. Create a skill for repeated specialized workflows, fragile procedures, tool integrations, domain knowledge, or reusable assets. Do not create one for one-off preferences or generic advice Codex already knows.
3. Name the skill with lowercase letters, digits, and hyphens. Keep it short, action-oriented, and exact.
4. Put all trigger logic in the frontmatter `description`. Include task types, file types, product names, and user phrasing that should invoke the skill. Include multilingual triggers when relevant.
5. Keep `SKILL.md` procedural and compact. Put only the core workflow there. Move detailed examples, schemas, rubrics, and long references to `references/`.
6. Add `scripts/` only for repeated deterministic operations or fragile validation. Test scripts by running them.
7. Add `assets/` only for files that should be copied or reused in final outputs, such as templates, icons, fonts, boilerplate, or sample artifacts.
8. Add or update `agents/openai.yaml` with human-facing UI metadata when the environment supports it.
9. Validate the final folder. Run `scripts/audit_skill.py <skill-folder>` from this skill. Also run the platform quick validator if an official one is available.

## Creating A Skill

When creating a new skill, use an existing initializer if available, especially a local `skill-creator/scripts/init_skill.py`. If no initializer is available, create this minimum structure:

```text
skill-name/
  SKILL.md
  agents/openai.yaml
```

Add `references/`, `scripts/`, and `assets/` only when they directly support the workflow.

`SKILL.md` must use only this frontmatter shape:

```yaml
---
name: skill-name
description: What the skill does and exactly when Codex should use it.
---
```

## Reviewing A Skill

Review skills in this order:

1. Trigger quality: Would the description invoke the skill for realistic user requests without being too broad?
2. Context efficiency: Does `SKILL.md` avoid generic explanations and push optional detail into references?
3. Procedural usefulness: Does the body tell Codex what to do next, not merely explain the topic?
4. Resource fit: Are scripts, references, and assets present only where they reduce repeated work or error?
5. Validation: Are scripts runnable, examples current, metadata valid, and placeholder text removed?

For detailed patterns and a scoring rubric, read `references/skill-patterns.md` only when designing or reviewing a nontrivial skill.

## Useful Commands

Run this skill's audit helper after edits:

```powershell
python path/to/skill-writing-coach/scripts/audit_skill.py path/to/target-skill
```

If Python is not on PATH in Codex Desktop, use the bundled Python runtime shown by the workspace dependency loader.
