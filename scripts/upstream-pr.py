#!/usr/bin/env python3
"""有上游变化时开或更新同一个 PR。没有变化则什么都不做。

用法:
  scripts/upstream-pr.py --before skills.lock.json [--report new-skills.json] [--dry-run]
  scripts/upstream-pr.py --before FILE --report FILE --push
  scripts/upstream-pr.py --self-test

--push 才会提交、强制推送 upstream-sync 并用 gh 开或更新 PR。本地默认只打印。
新 skill 只写进 PR 正文，不改 skills.json。
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills.json"
LOCK_PATH = ROOT / "skills.lock.json"
BRANCH = "upstream-sync"
BASE = "main"
FILE_LIMIT = 100


def run(*args, check=True):
    result = subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.stderr.write(result.stdout)
        raise SystemExit(f"命令失败（{result.returncode}）: {' '.join(args)}")
    return result


def load_sync():
    path = ROOT / "scripts" / "sync-upstream.py"
    spec = importlib.util.spec_from_file_location("sync_upstream", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def changed_files():
    text = run("git", "status", "--porcelain").stdout
    files = []
    for line in text.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return files


def short(sha):
    return sha[:7] if sha else "无"


def is_license_file(path, manifest):
    parts = Path(path).parts
    if len(parts) != 4 or parts[0] != "vendor":
        return False
    uid, filename = parts[2], parts[3]
    for up in manifest["upstreams"]:
        if up["id"] != uid:
            continue
        names = {up.get("licenseFile", "LICENSE"), "LICENSE", "NOTICE.md"}
        return filename in names
    return False


def render_title(manifest, before, after):
    bits = []
    old_map = before["upstreams"]
    new_map = after["upstreams"]
    for up in manifest["upstreams"]:
        uid = up["id"]
        old = old_map.get(uid, {}).get("commit")
        new = new_map.get(uid, {}).get("commit")
        if old != new:
            bits.append(f"{uid} {short(old)} → {short(new)}")
    if not bits:
        return "chore(skills): 重新同步上游文件"
    return "chore(skills): 同步上游（" + "，".join(bits) + "）"


def render_body(manifest, before, after, files, discovered):
    old_map = before["upstreams"]
    new_map = after["upstreams"]
    lines = [
        "每周的 Upstream update workflow 打开此 PR，不会自动合并。",
        "",
        "## 提交",
        "",
        "| 上游 | 旧提交 | 新提交 | 对比 |",
        "| --- | --- | --- | --- |",
    ]
    for up in manifest["upstreams"]:
        uid = up["id"]
        repo = up["repository"]
        old = old_map.get(uid, {}).get("commit")
        new = new_map.get(uid, {}).get("commit")
        old_cell = f"[`{short(old)}`]({repo}/commit/{old})" if old else "无"
        new_cell = f"[`{short(new)}`]({repo}/commit/{new})" if new else "无"
        if old and new and old != new:
            compare = f"[对比]({repo}/compare/{old}...{new})"
        elif old == new:
            compare = "提交未变"
        else:
            compare = "无旧提交"
        lines.append(f"| `{uid}` | {old_cell} | {new_cell} | {compare} |")
    lines.extend(["", "## 变更文件", ""])
    shown = files[:FILE_LIMIT]
    if shown:
        lines.extend(f"- `{path}`" for path in shown)
        if len(files) > FILE_LIMIT:
            lines.append(f"- 其余 {len(files) - FILE_LIMIT} 个文件略")
    else:
        lines.append("无。")
    licenses = [path for path in files if is_license_file(path, manifest)]
    lines.extend(["", "## 许可证", ""])
    if licenses:
        lines.append("这次改到了许可证或 NOTICE。请核对是否仍可接受：")
        lines.append("")
        lines.extend(f"- `{path}`" for path in licenses)
    else:
        lines.append("这次没有改到许可证文件。")
    lines.extend(["", "## 新 skill", ""])
    fresh = [(uid, item) for uid, items in discovered.items() for item in items]
    if fresh:
        lines.append("在已同步的 skill 目录里出现了尚未收录的 skill。本次没有自动加入 `skills.json`，需要的话另改清单并指定分类：")
        lines.append("")
        for uid, item in fresh:
            lines.append(f"- `{uid}`：`{item['name']}`（`{item['path']}`）")
    else:
        lines.append("在已同步的 skill 目录里，没有清单和未收录名单之外的新 skill。")
    lines.append("")
    return "\n".join(lines)


def commit_and_open(title, body):
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "checkout", "-B", BRANCH)
    run("git", "add", "--", "vendor", "skills.lock.json", "docs/UPSTREAMS.md")
    staged = run("git", "diff", "--cached", "--name-only").stdout.strip()
    if not staged:
        print("没有可提交的变更，不开 PR")
        return
    run("git", "commit", "-m", title)
    run("git", "push", "--force", "origin", f"HEAD:{BRANCH}")
    listed = run(
        "gh", "pr", "list",
        "--head", BRANCH,
        "--base", BASE,
        "--state", "open",
        "--json", "number",
    )
    prs = json.loads(listed.stdout or "[]")
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(body)
        body_file = handle.name
    if prs:
        number = str(prs[0]["number"])
        run("gh", "pr", "edit", number, "--title", title, "--body-file", body_file)
        print(f"已更新 PR #{number}")
    else:
        created = run(
            "gh", "pr", "create",
            "--base", BASE,
            "--head", BRANCH,
            "--title", title,
            "--body-file", body_file,
        )
        print(created.stdout.strip())


def self_test():
    manifest = {
        "upstreams": [
            {
                "id": "example",
                "repository": "https://github.com/acme/skills",
                "licenseFile": "LICENSE",
                "paths": {"skills/kept": "skills/kept"},
                "skills": [{"name": "kept", "category": "motion"}],
                "excluded": [{"path": "skills/old", "reason": "已知不收录"}],
            }
        ]
    }
    before = {"upstreams": {"example": {"commit": "a" * 40}}}
    after = {"upstreams": {"example": {"commit": "b" * 40}}}
    files = [
        "vendor/motion/example/LICENSE",
        "vendor/motion/example/skills/kept/SKILL.md",
        "docs/UPSTREAMS.md",
    ]
    discovered = {"example": [{"name": "fresh", "path": "skills/fresh"}]}
    title = render_title(manifest, before, after)
    body = render_body(manifest, before, after, files, discovered)
    assert "example" in title and "→" in title
    assert f"https://github.com/acme/skills/compare/{'a' * 40}...{'b' * 40}" in body
    assert "vendor/motion/example/LICENSE" in body
    assert "请核对是否仍可接受" in body
    assert "skills/fresh" in body
    assert "没有自动加入" in body
    same = render_body(
        manifest,
        before,
        before,
        ["skills.lock.json"],
        {},
    )
    assert "提交未变" in same
    assert "这次没有改到许可证文件" in same
    assert "没有清单和未收录名单之外的新 skill" in same
    assert render_title(manifest, before, before) == "chore(skills): 重新同步上游文件"

    sync = load_sync()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in ("skills/kept/SKILL.md", "skills/old/SKILL.md", "skills/fresh/SKILL.md"):
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("---\nname: x\n---\n")
        decoy = root / ".claude" / "skills" / "decoy" / "SKILL.md"
        decoy.parent.mkdir(parents=True, exist_ok=True)
        decoy.write_text("---\nname: decoy\n---\n")
        (root / "performance-cheatsheet.md").write_text("not a skill")
        found = sync.unlisted_skills(root, manifest["upstreams"][0])
    assert found == [{"name": "fresh", "path": "skills/fresh"}], found
    print("upstream-pr self-test 通过")


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        self_test()
        return
    if "--before" not in argv:
        sys.exit(__doc__)
    before_path = Path(argv[argv.index("--before") + 1])
    report_path = None
    if "--report" in argv:
        report_path = Path(argv[argv.index("--report") + 1])
    push = "--push" in argv
    manifest = json.loads(MANIFEST_PATH.read_text())
    before = json.loads(before_path.read_text())
    after = json.loads(LOCK_PATH.read_text())
    files = changed_files()
    if report_path and report_path.exists():
        discovered = json.loads(report_path.read_text())
    else:
        discovered = {}
    if not files:
        print("没有变化，不开 PR")
        return
    title = render_title(manifest, before, after)
    body = render_body(manifest, before, after, files, discovered)
    if not push:
        print(title)
        print(body)
        print("未推送。workflow 里加 --push 才会开或更新 PR。")
        return
    commit_and_open(title, body)


if __name__ == "__main__":
    main()
