#!/usr/bin/env bash
# 基准仓库自检：脚本语法、JSON 合法性、vendor/ 与清单一致；本机运行时额外报告 user/ 配置漂移。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
status=0

for f in scripts/*.sh; do
  bash -n "$f" || status=1
done
for f in scripts/*.py; do
  python3 -m py_compile "$f" || status=1
done
find scripts -name '__pycache__' -type d -exec rm -rf {} +

while IFS= read -r f; do
  python3 -m json.tool "$f" >/dev/null || { echo "JSON 无效: $f"; status=1; }
done < <(find . -name '*.json' -not -path './.git/*')

python3 - <<'PY' || status=1
import json, re, sys
from pathlib import Path

manifest = json.load(open("skills.json"))
lock = json.load(open("skills.lock.json"))["upstreams"]
bad = []
slug = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
known = []
for cat in manifest.get("categories", []):
    cid = cat.get("id", "")
    if not slug.match(cid):
        bad.append(f"分类 id 不是 kebab-case: {cid!r}")
    known.append(cid)
if len(known) != len(set(known)):
    bad.append("分类 id 重复")
known_set = set(known)

seen = {}
ids = []
for up in manifest["upstreams"]:
    uid = up["id"]
    ids.append(uid)
    if uid not in lock:
        bad.append(f"{uid}: skills.lock.json 缺少记录")
    if up.get("scope") not in ("user", "project"):
        bad.append(f"{uid}: scope 只能是 user 或 project")
    skills = up.get("skills", [])
    names = []
    cats = set()
    for item in skills:
        if not isinstance(item, dict) or not item.get("name") or not item.get("category"):
            bad.append(f"{uid}: skills 项需要 name 和 category")
            continue
        name, cat = item["name"], item["category"]
        names.append(name)
        cats.add(cat)
        if cat not in known_set:
            bad.append(f"{uid}: {name} 的分类 {cat} 不在 categories 里")
        if name in seen:
            bad.append(f"skill 名称冲突: {name}（{seen[name]} 与 {uid}）")
        else:
            seen[name] = uid
        if not Path(f"vendor/{cat}/{uid}/skills/{name}/SKILL.md").is_file():
            bad.append(f"{uid}: vendor 中缺少 {cat}/{name}/SKILL.md")
        if f"skills/{name}" not in up.get("paths", {}):
            bad.append(f"{uid}: paths 缺少 skills/{name}")
    if len(names) != len(set(names)):
        bad.append(f"{uid}: skills 列表有重复名称")
    lic = up.get("licenseFile", "LICENSE")
    for cat in cats:
        root = Path(f"vendor/{cat}/{uid}")
        if not (root / lic).exists():
            bad.append(f"{uid}: vendor/{cat}/{uid} 缺少 {lic}")
        skills_dir = root / "skills"
        found = sorted(p.name for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
        expected = sorted(item["name"] for item in skills if isinstance(item, dict) and item.get("category") == cat)
        if found != expected:
            bad.append(f"{uid}: vendor/{cat}/{uid}/skills 与清单不一致")
    for key in up.get("paths", {}):
        if key.startswith("skills/"):
            if key[len("skills/"):] not in names:
                bad.append(f"{uid}: paths 有未列入 skills 的 {key}")
            continue
        for cat in cats:
            if not (Path(f"vendor/{cat}/{uid}") / key).exists():
                bad.append(f"{uid}: vendor/{cat}/{uid} 缺少 {key}")
    if (Path("vendor") / uid).exists():
        bad.append(f"{uid}: 仍留在 vendor/{uid}/，应放到分类目录下")

vendor = Path("vendor")
if vendor.is_dir():
    for cat_dir in sorted(p for p in vendor.iterdir() if p.is_dir()):
        if cat_dir.name not in known_set:
            bad.append(f"vendor/{cat_dir.name} 不在分类清单里")
            continue
        for up_dir in sorted(p for p in cat_dir.iterdir() if p.is_dir()):
            if up_dir.name not in ids:
                bad.append(f"vendor/{cat_dir.name}/{up_dir.name} 不是已登记上游")

for b in bad:
    print(b)
sys.exit(1 if bad else 0)
PY

if [ -z "${CI:-}" ] && [ -d "$HOME/.claude" ]; then
  drift=$(scripts/sync-user.sh)
  if [ -n "$drift" ]; then
    echo "user/ 与本机配置不一致（scripts/sync-user.sh 查看，--pull 或 --apply 处理）:"
    echo "$drift" | grep -E '^(==|新增)' || true
  fi
fi

[ $status -eq 0 ] && echo "检查通过"
exit $status
