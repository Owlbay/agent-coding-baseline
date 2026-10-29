#!/usr/bin/env python3
"""按 skills.json 拉取上游默认分支，把文件同步到 vendor/<category>/<id>/，并更新 skills.lock.json。

用法: scripts/sync-upstream.py [--check]
  --check  只报告上游是否有新提交，不改文件；有更新时退出码为 1。
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "skills.json"
LOCK = ROOT / "skills.lock.json"
VENDOR = ROOT / "vendor"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def skills_of(up):
    items = up.get("skills", [])
    if not items or not all(isinstance(s, dict) and s.get("name") and s.get("category") for s in items):
        sys.exit(f"{up['id']}: 每个 skill 都要有 name 和 category")
    return items


def skill_keys(up):
    return {f"skills/{s['name']}" for s in skills_of(up)}


def categories_of(up):
    return sorted({s["category"] for s in skills_of(up)})


def copy_entry(src: Path, dest: Path, label: str):
    if not src.exists():
        sys.exit(f"上游缺少 {label}")
    if dest.exists():
        shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git", ".DS_Store"))
    else:
        shutil.copy2(src, dest)


def layout_ok(up) -> bool:
    uid = up["id"]
    if (VENDOR / uid).exists():
        return False
    lic = up.get("licenseFile", "LICENSE")
    assets = [key for key in up.get("paths", {}) if key not in skill_keys(up)]
    for cat in categories_of(up):
        root = VENDOR / cat / uid
        if not (root / lic).is_file() and not (root / lic).is_dir():
            return False
        for key in assets:
            if not (root / key).exists():
                return False
        expected = sorted(s["name"] for s in skills_of(up) if s["category"] == cat)
        skills_dir = root / "skills"
        if not skills_dir.is_dir():
            return False
        found = sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
        if found != expected:
            return False
        for name in expected:
            if not (skills_dir / name / "SKILL.md").is_file():
                return False
    return True


def place(up, src: Path):
    uid = up["id"]
    cats = set(categories_of(up))
    legacy = VENDOR / uid
    if legacy.exists():
        shutil.rmtree(legacy)
    if VENDOR.exists():
        for cat_dir in list(VENDOR.iterdir()):
            if not cat_dir.is_dir():
                continue
            placed = cat_dir / uid
            if placed.exists() and cat_dir.name not in cats:
                shutil.rmtree(placed)
            if cat_dir.exists() and not any(cat_dir.iterdir()):
                cat_dir.rmdir()
    keys = skill_keys(up)
    paths = up.get("paths", {})
    for cat in sorted(cats):
        root = VENDOR / cat / uid
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        for target, source in paths.items():
            if target in keys:
                continue
            copy_entry(src / source, root / target, f"{uid}: {source}")
        lic = up.get("licenseFile", "LICENSE")
        if not (root / lic).exists():
            sys.exit(f"{uid}: 分类 {cat} 缺少 {lic}，请把它写进 paths")
        for skill in skills_of(up):
            if skill["category"] != cat:
                continue
            key = f"skills/{skill['name']}"
            if key not in paths:
                sys.exit(f"{uid}: paths 缺少 {key}")
            dest = root / "skills" / skill["name"]
            copy_entry(src / paths[key], dest, f"{uid}: {paths[key]}")
            if not (dest / "SKILL.md").is_file():
                sys.exit(f"{uid}: 上游已没有 skill {skill['name']}，请更新 skills.json")


def validate(manifest):
    known = []
    for cat in manifest.get("categories", []):
        cid = cat.get("id", "")
        if not SLUG.match(cid):
            sys.exit(f"分类 id 不是 kebab-case: {cid}")
        known.append(cid)
    if len(known) != len(set(known)):
        sys.exit("分类 id 重复")
    known_set = set(known)
    seen = {}
    for up in manifest["upstreams"]:
        if up.get("scope") not in ("user", "project"):
            sys.exit(f"{up['id']}: scope 只能是 user 或 project")
        names = []
        for skill in skills_of(up):
            if skill["category"] not in known_set:
                sys.exit(f"{up['id']}: 未知分类 {skill['category']}")
            name = skill["name"]
            names.append(name)
            if name in seen:
                sys.exit(f"skill 名称冲突: {name}（{seen[name]} 与 {up['id']}）")
            seen[name] = up["id"]
            if f"skills/{name}" not in up.get("paths", {}):
                sys.exit(f"{up['id']}: paths 缺少 skills/{name}")
        if len(names) != len(set(names)):
            sys.exit(f"{up['id']}: skills 列表有重复名称")
        for key in up.get("paths", {}):
            if key.startswith("skills/") and key[len("skills/"):] not in names:
                sys.exit(f"{up['id']}: paths 有未列入 skills 的 {key}")


def main():
    check_only = "--check" in sys.argv[1:]
    manifest = json.loads(MANIFEST.read_text())
    validate(manifest)
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {"upstreams": {}}
    changed = []
    rewritten = False

    with tempfile.TemporaryDirectory() as tmp:
        for up in manifest["upstreams"]:
            uid, repo = up["id"], up["repository"]
            head = git("ls-remote", repo, "HEAD").split()[0]
            prev = lock["upstreams"].get(uid, {}).get("commit")
            if head == prev:
                if check_only or layout_ok(up):
                    print(f"{uid}: 已是最新 {head[:7]}")
                    continue
                print(f"{uid}: 提交未变，按清单重新同步 {head[:7]}")
            else:
                print(f"{uid}: {prev[:7] if prev else '无'} -> {head[:7]}")
                changed.append(uid)
                if check_only:
                    continue

            src = Path(tmp) / uid
            git("clone", "--quiet", "--depth", "1", repo, str(src))
            got = git("rev-parse", "HEAD", cwd=src)
            if got != head:
                sys.exit(f"{uid}: 浅克隆得到 {got[:7]}，与 ls-remote 的 {head[:7]} 不一致")
            place(up, src)
            lock["upstreams"][uid] = {
                "repository": repo,
                "commit": head,
                "committedAt": git("log", "-1", "--format=%cI", cwd=src),
                "syncedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            rewritten = True

    if rewritten:
        LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
    if changed:
        print("有更新: " + ", ".join(changed))
    elif rewritten:
        print("提交未变，已按清单重新同步")
    else:
        print("全部最新")
    sys.exit(1 if check_only and changed else 0)


if __name__ == "__main__":
    main()
