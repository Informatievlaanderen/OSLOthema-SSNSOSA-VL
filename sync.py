#!/usr/bin/env python3
"""Copy the kit's skills into a project as project skills.

The kit sits in the project as a git subtree (``oslo-ld-kit/``). Claude Code only loads project
skills from ``.claude/skills/<name>/SKILL.md``, so this script copies ``skills/*`` there and
rewrites the relative links to the guide so that they still resolve. Run it from anywhere after
every ``git subtree pull`` and commit the result together with the update:

    python oslo-ld-kit/sync.py              # project = the directory that contains the kit
    python oslo-ld-kit/sync.py <project>    # or name the project explicitly

Skills copied earlier but no longer in the kit are removed. Skills of the project's own (not
listed in the manifest) are left alone.
"""

import json
import os
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
MANIFEST = ".oslo-ld-kit.json"
NOTICE = ("<!-- Copied from oslo-ld-kit by sync.py. Do not edit here: change the kit "
          "(https://github.com/milieuinfo/oslo-ld-kit) and run sync.py again. -->\n")


def rewrite(text: str, skill_dir: Path) -> str:
    """Point the kit-relative links (``../../guide/``, ``../../rules/``) at the kit in the project."""
    for part in ("guide", "rules"):
        target = os.path.relpath(KIT / part, skill_dir).replace(os.sep, "/")
        text = text.replace(f"../../{part}/", f"{target}/")
    return text


def add_notice(text: str) -> str:
    """Insert the notice after the YAML front matter, so that the front matter stays first."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            end = text.index("\n", end + 1) + 1
            return text[:end] + "\n" + NOTICE + text[end:]
    return NOTICE + text


def main() -> int:
    project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else KIT.parent
    target = project / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)

    manifest_path = target / MANIFEST
    previous = []
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8")).get("skills", [])

    skills = sorted(p.name for p in (KIT / "skills").iterdir() if (p / "SKILL.md").is_file())
    for name in skills:
        dest = target / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(KIT / "skills" / name, dest)
        skill_md = dest / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        skill_md.write_text(add_notice(rewrite(text, dest)), encoding="utf-8", newline="\n")

    for name in previous:
        if name not in skills and (target / name).is_dir():
            shutil.rmtree(target / name)
            print(f"removed {name}")

    version = json.loads((KIT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    manifest_path.write_text(json.dumps({"kit-version": version, "skills": skills}, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(f"oslo-ld-kit {version}: {len(skills)} skills copied to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
