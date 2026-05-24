# Skill Patterns And Review Rubric

Use this reference when a skill is nontrivial, needs a quality review, or the user wants coaching on how to write better skills.

## Strong Skill Traits

- The frontmatter description is specific enough to trigger reliably from real user phrasing.
- The body begins with action: what Codex should do, what order to do it in, and what to validate.
- The skill assumes Codex is capable and avoids teaching generic facts.
- Optional detail lives in `references/` and is loaded only when relevant.
- Scripts handle repetitive, brittle, or validation-heavy work.
- Assets are directly reused in user-facing outputs.
- The final workflow tells Codex how to know it is done.

## Description Formula

Write the description as:

```text
Do X for Y. Use when the user asks for A, B, C, or D. Also use for files/tools/products named E, F, and G.
```

Good descriptions include concrete triggers:

- User intents: create, edit, review, migrate, translate, audit, publish.
- Artifacts: `.docx`, `.pptx`, PDFs, screenshots, repo files, API specs.
- Tools and domains: OpenAI API, GitHub Actions, BigQuery, payroll, brand system.
- Natural user phrasing, including non-English phrasing when likely.

Avoid descriptions that only say "helps with X" or "provides guidance for X". Codex only sees the description before deciding whether to load the body.

## Resource Decision Table

Use `SKILL.md` for:

- Core workflow and decision tree.
- Commands that are always relevant.
- Short examples that prevent ambiguity.
- Links to optional references.

Use `references/` for:

- Long examples.
- Schemas, API notes, policies, style rules, rubrics.
- Variant-specific guidance, such as AWS vs. GCP or React vs. Vue.

Use `scripts/` for:

- Repeatable file transformations.
- Validation or linting.
- Fragile command sequences.
- Data extraction that would otherwise be rewritten each time.

Use `assets/` for:

- Templates, starter projects, fonts, images, icons, sample workbooks, or decks.

## Common Failure Modes

- Hidden trigger logic: "when to use" guidance appears only in the body, so the skill never loads.
- Overbroad trigger: the description captures generic coding, writing, or research tasks.
- Tutorial bloat: the body explains concepts Codex already knows instead of giving workflow constraints.
- Reference hoarding: large files are included but never linked from `SKILL.md`.
- Script theater: scripts exist but are untested, unused, or simpler than a direct command.
- Metadata drift: `agents/openai.yaml` no longer matches the skill name or purpose.
- Unclear completion: Codex is not told how to validate or stop.

## Review Rubric

Score each item 0-2.

- Trigger accuracy: Realistic prompts invoke it; unrelated prompts do not.
- Procedural clarity: The next action is obvious after reading the body.
- Context discipline: The body is compact and references are optional.
- Resource usefulness: Every bundled file has a clear job.
- Validation strength: The skill includes commands, checks, or examples that catch mistakes.
- Maintainability: Names, paths, metadata, and examples stay easy to update.

Suggested verdict:

- 10-12: Strong. Ship it.
- 7-9: Useful, but tighten the weakest one or two areas.
- 4-6: Works only with a cooperative prompt. Revise before relying on it.
- 0-3: Reframe the skill from examples and start again.

## Example Skeleton

```markdown
---
name: useful-action-name
description: Do the specialized workflow. Use when the user asks for concrete trigger A, artifact B, tool C, or phrase D.
---

# Useful Action Name

## Workflow

1. Inspect the artifact or repo first.
2. Choose the narrowest applicable path.
3. Use bundled scripts for deterministic steps.
4. Validate with the listed command.
5. Report changed files and remaining risks.

## Resources

- Read `references/provider-a.md` only when the user chooses Provider A.
- Run `scripts/check_output.py <path>` before finishing.
```
