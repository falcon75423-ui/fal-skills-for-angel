#!/usr/bin/env python3
"""
lessons/INDEX.md 生成腳本

掃描 lessons/*.md（排除 INDEX.md、_schema.md、ARCHIVE.md），
抽取每條教訓的 YAML frontmatter，產出 INDEX.md。

純標準庫實作，不依賴 PyYAML。frontmatter 欄位格式需對齊 lessons/_schema.md。

用法：
    python tools/generate_lessons_index.py

產出：
    lessons/INDEX.md（覆蓋）
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime


SKILL_ROOT = Path(__file__).parent.parent
LESSONS_DIR = SKILL_ROOT / "lessons"
INDEX_PATH = LESSONS_DIR / "INDEX.md"

EXCLUDED_FILES = {"INDEX.md", "_schema.md"}

CATEGORY_ORDER = [
    "long_form_delivery",
    "structure_design",
    "verification",
    "subcontract",
    "skill_rework",
    "infrastructure",
]

CATEGORY_CN = {
    "long_form_delivery": "長文交付",
    "structure_design": "結構設計",
    "verification": "驗證品質",
    "subcontract": "跨 Skill 協作",
    "skill_rework": "Skill 修繕",
    "infrastructure": "基建層",
}


@dataclass
class Lesson:
    id: str
    title: str
    one_liner: str
    category: str
    triggers: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    created_at: str = ""
    invalid_at: str | None = None
    invalid_reason: str | None = None
    superseded_by: str | None = None
    helpful_count: int = 0
    harmful_count: int = 0
    evidence: list[str] = field(default_factory=list)
    source_file: str = ""

    @property
    def is_retired(self) -> bool:
        return self.invalid_at is not None and self.invalid_at != "null"


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.MULTILINE | re.DOTALL)


def parse_frontmatter_block(block: str) -> dict:
    """解析一個 YAML frontmatter 區塊（我們自己控制格式，純標準庫夠用）"""
    result: dict = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        m = re.match(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue

        key, value = m.group(1), m.group(2).strip()

        if value == "":
            # Block list: key:\n  - item1\n  - item2
            items: list[str] = []
            j = i + 1
            while j < len(lines):
                sub = lines[j]
                if not sub.strip():
                    j += 1
                    continue
                sub_m = re.match(r"^\s*-\s*(.+)$", sub)
                if sub_m:
                    items.append(sub_m.group(1).strip())
                    j += 1
                else:
                    break
            result[key] = items
            i = j
            continue

        if value == "null":
            result[key] = None
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            result[key] = [x.strip() for x in inner.split(",")] if inner else []
        elif value.isdigit():
            result[key] = int(value)
        else:
            # 去除引號（若有）
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            result[key] = value
        i += 1
    return result


def parse_lessons_file(path: Path) -> list[Lesson]:
    """一個檔案可含多條教訓（多個 --- frontmatter 區塊）"""
    text = path.read_text(encoding="utf-8")
    lessons: list[Lesson] = []
    for m in FRONTMATTER_RE.finditer(text):
        data = parse_frontmatter_block(m.group(1))
        if "id" not in data or "title" not in data:
            continue
        lesson = Lesson(
            id=data.get("id", ""),
            title=data.get("title", ""),
            one_liner=data.get("one_liner", ""),
            category=data.get("category", ""),
            triggers=data.get("triggers", []) or [],
            related=data.get("related", []) or [],
            created_at=data.get("created_at", "") or "",
            invalid_at=data.get("invalid_at"),
            invalid_reason=data.get("invalid_reason"),
            superseded_by=data.get("superseded_by"),
            helpful_count=data.get("helpful_count", 0) or 0,
            harmful_count=data.get("harmful_count", 0) or 0,
            evidence=data.get("evidence", []) or [],
            source_file=path.name,
        )
        lessons.append(lesson)
    return lessons


def collect_all_lessons() -> list[Lesson]:
    all_lessons: list[Lesson] = []
    for path in sorted(LESSONS_DIR.glob("*.md")):
        if path.name in EXCLUDED_FILES:
            continue
        all_lessons.extend(parse_lessons_file(path))
    return all_lessons


def build_index(lessons: list[Lesson]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append("# 教訓索引（INDEX）")
    lines.append("")
    lines.append(f"> 🤖 本檔由 `tools/generate_lessons_index.py` 自動生成，**禁止手編**。")
    lines.append(f"> 最後生成：{now}")
    lines.append("")

    active = [l for l in lessons if not l.is_retired]
    retired = [l for l in lessons if l.is_retired]

    # 統計
    lines.append(f"現役條目：**{len(active)}** ｜ 已退役：**{len(retired)}** ｜ 總計：**{len(lessons)}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 現役條目：按 category 分組
    lines.append("## 現役條目（按情境）")
    lines.append("")
    by_cat: dict[str, list[Lesson]] = {}
    for l in active:
        by_cat.setdefault(l.category, []).append(l)

    for cat in CATEGORY_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        cn = CATEGORY_CN.get(cat, cat)
        lines.append(f"### {cn}（`{cat}.md`）")
        lines.append("")
        lines.append("| ID | 一句話 | 觸發詞 | helpful | 檔案 |")
        lines.append("|----|--------|--------|---------|------|")
        for l in sorted(items, key=lambda x: x.id):
            triggers = " / ".join(l.triggers[:3]) if l.triggers else "—"
            lines.append(f"| {l.id} | {l.one_liner} | {triggers} | {l.helpful_count} | `{l.source_file}` |")
        lines.append("")

    # 未分類情境（有 active 但不在 CATEGORY_ORDER 裡的）
    unknown_cats = sorted(set(by_cat.keys()) - set(CATEGORY_ORDER))
    for cat in unknown_cats:
        lines.append(f"### ⚠️ 未知情境：{cat}")
        lines.append("")
        lines.append("這些 category 不在 CATEGORY_ORDER 白名單裡，請確認 _schema.md 或修正條目。")
        for l in by_cat[cat]:
            lines.append(f"- {l.id}（`{l.source_file}`）")
        lines.append("")

    # 觸發詞反向索引
    lines.append("---")
    lines.append("")
    lines.append("## 觸發詞反向索引")
    lines.append("")
    lines.append("> 搜尋者動作詞 → 相關條目。進場偵察時用來快速定位。")
    lines.append("")
    trigger_map: dict[str, list[str]] = {}
    for l in active:
        for t in l.triggers:
            trigger_map.setdefault(t, []).append(l.id)
    for t in sorted(trigger_map.keys()):
        ids = ", ".join(sorted(trigger_map[t]))
        lines.append(f"- **{t}** → {ids}")
    lines.append("")

    # 已退役
    if retired:
        lines.append("---")
        lines.append("")
        lines.append("## 已退役條目（考古用）")
        lines.append("")
        lines.append("| ID | 原標題 | 退役時戳 | 退役原因 | 被誰取代 |")
        lines.append("|----|--------|---------|---------|---------|")
        for l in sorted(retired, key=lambda x: (x.invalid_at or "", x.id)):
            reason = l.invalid_reason or "—"
            sup = l.superseded_by or "—"
            lines.append(f"| {l.id} | {l.title} | {l.invalid_at} | {reason} | {sup} |")
        lines.append("")

    # 驗證段：一致性檢查
    lines.append("---")
    lines.append("")
    lines.append("## 一致性檢查")
    lines.append("")
    issues = validate(lessons)
    if not issues:
        lines.append("✅ 通過：所有 related 指向有效、無重複 ID、無缺必填欄位")
    else:
        lines.append("⚠️ 發現問題：")
        for i in issues:
            lines.append(f"- {i}")
    lines.append("")

    return "\n".join(lines)


def validate(lessons: list[Lesson]) -> list[str]:
    issues: list[str] = []
    ids = {l.id for l in lessons}

    # 重複 ID
    seen: set[str] = set()
    for l in lessons:
        if l.id in seen:
            issues.append(f"重複 ID：{l.id}（{l.source_file}）")
        seen.add(l.id)

    # related 指向無效
    for l in lessons:
        for r in l.related:
            if r not in ids:
                issues.append(f"{l.id} related 指向不存在的條目：{r}")

    # 必填欄位缺失
    for l in lessons:
        missing: list[str] = []
        if not l.title:
            missing.append("title")
        if not l.one_liner:
            missing.append("one_liner")
        if not l.category:
            missing.append("category")
        if not l.triggers:
            missing.append("triggers")
        if not l.created_at:
            missing.append("created_at")
        if missing:
            issues.append(f"{l.id} 缺必填欄位：{', '.join(missing)}")

    # 退役條目必須有 invalid_reason
    for l in lessons:
        if l.is_retired and not (l.invalid_reason or l.superseded_by):
            issues.append(f"{l.id} 已退役但缺 invalid_reason 或 superseded_by")

    return issues


def main() -> int:
    if not LESSONS_DIR.exists():
        print(f"❌ lessons/ 目錄不存在：{LESSONS_DIR}", file=sys.stderr)
        return 1

    lessons = collect_all_lessons()
    if not lessons:
        print(f"⚠️ 無教訓條目可索引（lessons/ 下無 *.md 含 frontmatter）")

    INDEX_PATH.write_text(build_index(lessons), encoding="utf-8")

    active = [l for l in lessons if not l.is_retired]
    retired = [l for l in lessons if l.is_retired]
    issues = validate(lessons)

    print(f"✅ 生成完成：{INDEX_PATH}")
    print(f"   現役 {len(active)} 條 ｜ 退役 {len(retired)} 條")
    if issues:
        print(f"   ⚠️ 一致性問題 {len(issues)} 件（見 INDEX.md 尾段）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
