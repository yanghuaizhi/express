# Express

Express helps Codex explain things clearly from the first reply, including complex discussions, progress updates, and work documents. It is designed for natural Chinese and also supports English and bilingual writing. Its communication principles are inspired by ASD-STE100, without applying English word limits to Chinese.

Answer the reader's question first. Explain the necessary evidence, conditions, and relationships. Preserve facts, uncertainty, and the difference between a suggestion and a decision. Choose length and format for the task, without fixed word limits or blanket bans on lists and tables.

[中文](README.md) · [Skill](skills/express/SKILL.md) · [Examples](skills/express/references/examples.md) · [Codex setup](docs/codex.md)

## Make it a session default

For everyday communication, install the plugin from a downloaded or cloned checkout:

```bash
codex plugin marketplace add .
codex plugin add express@express-marketplace
```

Then review and trust its session-start hook through Codex's native flow, such as `/hooks` in the CLI. Installation does not automatically trust it. The hook requires `python3` on PATH and loads shared communication principles on supported session-start events. Complex explanations and feedback such as “I don't understand” or “the main point is missing” call for the relevant skill guidance without a separate enablement request. Guidance already in context is reused.

You can ask questions and request clearer explanations normally; `$express` is not required for every message. Whether instructions were loaded and whether an answer is useful are separate checks. See the [setup guide](docs/codex.md) for verification, updates, and removal.

## Try the standalone skill

From a downloaded or cloned checkout, copy the skill into your personal Codex skills directory. This command refuses to replace an existing installation:

```bash
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/express" && cp -R skills/express "$HOME/.agents/skills/express"
```

Invoke it in Codex:

```text
$express Answer the main question directly, explain the necessary conditions, and preserve uncertainty.
$express Restructure this proposal for its readers without inventing facts or commitments.
$express Edit only this paragraph and preserve its meaning.
```

Codex can select the standalone skill automatically, but discovery does not guarantee invocation on every turn. Choose either the plugin or the standalone skill to avoid duplicate entries. Copying a skill does not install a hook or change existing sessions.

## Scope

Express covers direct answers, explanations, discussions, clarification, progress updates, and practical documents. It does not replace research, coding, document-format tools, or user decisions. A small edit stays small; an explanation does not automatically need an action plan.

When a user asks for a clearer answer, first identify whether the problem concerns facts, reasoning, missing relationships, missing information, or presentation. Repair the cause and affected conclusions. Do not merely substitute words, add length, or repeat apologies.

Express has no dependency on Waza Write. Shared expression principles can apply while one appropriate skill leads the task. It does not automatically draft with Express and rewrite with Write, copy Write's specialized workflows, or modify another plugin's cache. See [coexistence guidance](skills/express/references/compatibility.md).

Chinese instructions and examples are original, not word-for-word translations of English writing limits. The project borrows general clarity principles from [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) and [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish), with [documented boundaries](docs/sources.md). It does not redistribute the ASD standard or dictionary and makes no claim of ASD-STE100 compliance or endorsement.

## Verification and privacy

The optional SessionStart hook reads only the packaged `core.md`, emits context, and exits. It does not read session input, access the network, or write user files. User and project instructions take precedence over its defaults. It does not modify `AGENTS.md`.

Package checks require Python 3.9 or newer and the development dependency in `requirements-dev.txt`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

Structural checks and hook tests do not establish writing quality. Review actual answers against their inputs, including semantic fidelity and whether readers have enough information to understand, decide, or act. [Synthetic cases and review criteria](evals/README.md) support this review; they do not establish effectiveness in every real task.

When reporting a problem, share only material you are authorized to disclose. Do not include credentials, private conversations, internal records, or personal configuration. All bundled teaching cases are fictional.

Licensed under the [MIT License](LICENSE).
