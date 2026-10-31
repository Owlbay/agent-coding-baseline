#!/usr/bin/env python3
"""根据 skills.json 和 skills.lock.json 生成 docs/UPSTREAMS.md。

用法: scripts/render-upstreams.py [--check]
  --check  只比较现有文件，不一致时退出码为 1。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills.json"
LOCK_PATH = ROOT / "skills.lock.json"
OUT = ROOT / "docs" / "UPSTREAMS.md"

SCOPES = {
    "user": "用户级，安装到 `~/.claude/skills/<name>/`",
    "project": "项目级，安装到目标项目的 `.claude/`",
}


def load():
    manifest = json.loads(MANIFEST_PATH.read_text())
    lock = json.loads(LOCK_PATH.read_text())["upstreams"]
    return manifest, lock


def repo_name(url: str) -> str:
    path = url.removeprefix("https://github.com/").strip("/")
    return path or url


def render(manifest, lock) -> str:
    titles = {cat["id"]: cat["title"] for cat in manifest["categories"]}
    lines = [
        "# 上游清单",
        "",
        "本文件由 `scripts/render-upstreams.py` 根据 `skills.json` 和 `skills.lock.json` 生成。不要手改。改清单或锁定提交后运行 `python3 scripts/render-upstreams.py`。`scripts/check.sh` 会核对本文件与这两份 JSON 一致。",
        "",
        "## 已同步的上游",
        "",
        "这些上游由 `scripts/sync-upstream.py` 写入 `vendor/<category>/<upstream-id>/`。作者、许可证、分类和未收录路径以 `skills.json` 为准，锁定提交以 `skills.lock.json` 为准。",
        "",
    ]
    for up in manifest["upstreams"]:
        uid = up["id"]
        locked = lock[uid]
        commit = locked["commit"]
        lines.append(f"### {repo_name(up['repository'])}")
        lines.append("")
        lines.append(f"- 清单 id：`{uid}`")
        lines.append(f"- 仓库：{up['repository']}")
        if up.get("homepage"):
            lines.append(f"- 主页：{up['homepage']}")
        lines.append(f"- 作者：{up['author']}")
        lines.append(f"- 许可证：{up['license']}（文件 `{up.get('licenseFile', 'LICENSE')}`）")
        if up.get("$licenseNote"):
            lines.append(f"- 许可证说明：{up['$licenseNote']}")
        lines.append(f"- 安装范围：{SCOPES[up['scope']]}")
        lines.append(
            f"- 锁定提交：[`{commit[:7]}`]({up['repository']}/commit/{commit})（`{commit}`）"
        )
        lines.append(f"- 上游提交时间：{locked['committedAt']}")
        lines.append(f"- 同步时间：{locked['syncedAt']}")
        lines.append("")
        lines.append("| Skill | 分类 |")
        lines.append("| --- | --- |")
        for skill in up["skills"]:
            cat = skill["category"]
            lines.append(f"| `{skill['name']}` | {titles[cat]}（`{cat}`） |")
        lines.append("")
        lines.append("#### 未收录")
        lines.append("")
        excluded = up.get("excluded") or []
        if not excluded:
            lines.append("无。")
        else:
            lines.append("| 路径 | 原因 |")
            lines.append("| --- | --- |")
            for item in excluded:
                lines.append(f"| `{item['path']}` | {item['reason']} |")
        lines.append("")
    lines.append("## 参考整理")
    lines.append("")
    lines.append("这些资料不进 `vendor/`，不锁定提交，不由 `scripts/sync-upstream.py` 安装。")
    lines.append("")
    for ref in manifest.get("references", []):
        lines.append(f"### {ref['name']}")
        lines.append("")
        lines.append(f"- 仓库：{ref['repository']}")
        lines.append(f"- 作者：{ref['author']}")
        lines.append(f"- 许可证：{ref['license']}")
        lines.append(f"- 本仓库文档：`{ref['doc']}`")
        lines.append(f"- 说明：{ref['summary']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    check_only = "--check" in sys.argv[1:]
    if any(arg not in ("--check",) for arg in sys.argv[1:]):
        sys.exit("用法: scripts/render-upstreams.py [--check]")
    text = render(*load())
    if check_only:
        current = OUT.read_text() if OUT.exists() else ""
        if current != text:
            sys.exit("docs/UPSTREAMS.md 与 skills.json / skills.lock.json 不一致，请运行 python3 scripts/render-upstreams.py")
        print("docs/UPSTREAMS.md 与清单一致")
        return
    OUT.write_text(text)
    print(f"已写入 {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
