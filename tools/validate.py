#!/usr/bin/env python3
"""Check package wiring and local links. This does not grade communication."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]


def validate() -> list[str]:
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    require(manifest.get("name") == "express", "Unexpected plugin identity")
    require(not (ROOT / "plugin.json").exists(), "Root plugin.json shadows Codex hook loading in the verified host version")
    for path in (manifest["skills"], manifest["hooks"]):
        require(path.startswith("./") and ".." not in Path(path).parts, "Plugin path must be package-relative")
        require((ROOT / path).exists(), f"Missing plugin component: {path}")

    skill = ROOT / "skills/express/SKILL.md"
    raw = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", raw, re.DOTALL)
    require(match is not None, "Skill must contain YAML frontmatter and a body")
    if match:
        meta = yaml.safe_load(match.group(1))
        require(meta.get("name") == skill.parent.name, "Skill name must match its directory")
        require(isinstance(meta.get("description"), str) and bool(meta["description"].strip()), "Skill description missing")
        require(len(meta.get("description", "")) <= 1024, "Skill description exceeds host metadata limit")
    interface = yaml.safe_load((skill.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
    require("$express" in interface["interface"]["default_prompt"], "Default prompt must invoke $express")
    require(interface["policy"]["allow_implicit_invocation"] is True, "Expected normal skill discovery")

    hooks = json.loads((ROOT / manifest["hooks"]).read_text(encoding="utf-8"))["hooks"]
    require(set(hooks) == {"SessionStart"}, "Only SessionStart is part of this package")
    group = hooks["SessionStart"][0]
    require("matcher" not in group, "SessionStart must cover all sources")
    require(group["hooks"][0]["additionalContextLimit"] == 0, "Core context must not be intentionally truncated")
    require((ROOT / "hooks/session_start.py").is_file(), "SessionStart script missing")

    market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    require(market["plugins"][0]["name"] == manifest["name"], "Marketplace plugin identity mismatch")
    require(market["plugins"][0]["source"]["path"] == "./", "Marketplace must resolve the package root")

    ignored = {".git", ".venv", ".work", "artifacts", "__pycache__"}
    markdown_files = [p for p in ROOT.rglob("*.md") if not (set(p.relative_to(ROOT).parts) & ignored)]
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"/(?:Users|home)/[^\s/]+/", text), f"Private absolute path in {path.relative_to(ROOT)}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            linked = (path.parent / unquote(parsed.path)).resolve()
            require(linked.is_relative_to(ROOT), f"Link escapes package in {path.relative_to(ROOT)}")
            require(linked.exists(), f"Broken local link in {path.relative_to(ROOT)}: {parsed.path}")
    return errors


if __name__ == "__main__":
    try:
        errors = validate()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"Package validation failed: {type(error).__name__}", file=sys.stderr)
        raise SystemExit(1)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print("Package wiring and local Markdown links passed. Writing quality requires behavioral review.")
