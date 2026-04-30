#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dogfood-validator.py — 火神鍛造自驗腳本

借鑑 impeccable E19 build-time dogfood validator 精髓：把火神自家飛輪規則
寫成自動檢查，違規分級警示。治「規則已存在 ≠ 規則被遵守」家族。

三個 check（v1：F-016）：
  A check_landmines_repeat — 踩雷錄活躍症狀/閘門失效 累計或復發次數 ≥3 警示
  C check_lessons_sync — 淬鍊師 lessons INDEX 跟情境檔同步性
  D check_pf_zombie — pending_followups Active 區 >30 天未動殭屍預防

Exit code（仿 impeccable）：
  0 — 全綠
  1 — WARNING
  2 — BLOCKER

用法：
  python tools/dogfood-validator.py
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Iterator, NamedTuple

# Windows console UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


# ─── 常數 ───────────────────────────────────────────────────────────

SEV_INFO = "🟢 INFO"
SEV_WARNING = "🟡 WARNING"
SEV_BLOCKER = "🔴 BLOCKER"

SKILL_ROOT = Path.home() / ".claude" / "skills" / "火神鍛造"
LESSONS_ROOT = Path.home() / ".claude" / "skills" / "淬鍊師" / "lessons"

LANDMINE_FILE = SKILL_ROOT / "references" / "踩雷錄.md"
PF_FILE = SKILL_ROOT / "clients" / "pending_followups.md"
INDEX_FILE = LESSONS_ROOT / "INDEX.md"

PF_ZOMBIE_DAYS = 30  # SKILL.md 既定（pending_followups.md 維護注意）
SAME_KIND_THRESHOLD = 3  # SKILL.md 既定（同類記憶 ≥3 = 升級閘門）

# 狀態欄含這些字面 = 已採結構性對策（降 INFO 不算 WARNING）
RESOLVED_KEYWORDS = (
    "已升級",
    "三振",
    "Hook 層",
    "升 Hook",
    "觀察期",
    "運作中",
    "結構重設計",
    "退役",
)


def _is_resolved(status: str) -> bool:
    return any(kw in status for kw in RESOLVED_KEYWORDS)


LESSON_CATEGORY_FILES = [
    "long_form_delivery.md",
    "structure_design.md",
    "verification.md",
    "subcontract.md",
    "skill_rework.md",
    "infrastructure.md",
]


class Finding(NamedTuple):
    severity: str
    check: str
    message: str


# ─── Helper：markdown 表格列解析 ────────────────────────────────────

def _parse_table_rows(section_text: str) -> Iterator[list[str]]:
    """從 markdown 段落抓資料列（跳過 header + separator）。

    yield 每列的 cells（string list，已 strip）。
    """
    header_seen = False
    for line in section_text.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not header_seen:
            header_seen = True
            continue
        # separator 列（| --- | --- |）
        if all(re.match(r"^[-:]+$", c) for c in cells if c):
            continue
        yield cells


# ─── Helper：YAML frontmatter 簡易解析 ────────────────────────────

def _iter_frontmatters(text: str) -> Iterator[dict]:
    """抓 markdown 內所有 ---\\nid: ...\\n--- 區塊。

    不嘗試完整 YAML——只支援本專案 lessons schema（key:value + 列表項）。
    """
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].strip() == "---":
            # 找下一個 ---
            j = i + 1
            while j < len(lines) and lines[j].strip() != "---":
                j += 1
            if j >= len(lines):
                # 沒找到 closing，當作裝飾分隔線跳過
                i += 1
                continue
            body_lines = lines[i + 1:j]
            # 必須含 id: 才算真 frontmatter（過濾裝飾分隔線）
            if any(re.match(r"^id:\s*\S", ln.strip()) for ln in body_lines):
                fm = _parse_yaml_simple(body_lines)
                if fm.get("id"):
                    yield fm
                i = j + 1  # 跳過 closing ---
            else:
                # 這個 --- 是裝飾分隔線，繼續往前找
                i += 1
        else:
            i += 1


def _parse_yaml_simple(lines: list[str]) -> dict:
    """極簡 YAML parser——夠 lessons schema 用就好。"""
    result: dict = {}
    related: list[str] = []
    triggers: list[str] = []
    evidence: list[str] = []
    current_list: str | None = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue

        # key: value
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            # 移除行尾註解（# 後）但避免吃到「value: #abc」這種
            if "#" in value and not value.startswith("#"):
                value = re.sub(r"\s+#.*$", "", value).strip()
            if not value:
                current_list = key
                continue
            # inline list: [M01, M02]
            if value.startswith("[") and value.endswith("]"):
                items = [s.strip() for s in value[1:-1].split(",") if s.strip()]
                if key == "related":
                    related.extend(items)
                else:
                    result[key] = items
            else:
                result[key] = value
            current_list = None
            continue

        # 列表項：  - xxx
        m = re.match(r"^\s+-\s+(.+)$", line)
        if m and current_list:
            item = m.group(1).strip()
            if current_list == "related":
                related.append(item)
            elif current_list == "triggers":
                triggers.append(item)
            elif current_list == "evidence":
                evidence.append(item)

    if related:
        result["_related"] = related
    if triggers:
        result["_triggers"] = triggers
    if evidence:
        result["_evidence"] = evidence
    return result


# ─── A：踩雷錄同類記憶 ≥3 ─────────────────────────────────────────

def check_landmines_repeat() -> Iterator[Finding]:
    if not LANDMINE_FILE.exists():
        yield Finding(SEV_BLOCKER, "A", f"踩雷錄不存在：{LANDMINE_FILE}")
        return

    content = LANDMINE_FILE.read_text(encoding="utf-8")

    # 「## 活躍症狀追蹤」段
    m_symptom = re.search(
        r"##\s*活躍症狀追蹤\s*\n(.+?)(?=\n##|\Z)",
        content,
        re.DOTALL,
    )
    if m_symptom:
        for row in _parse_table_rows(m_symptom.group(1)):
            if len(row) < 3:
                continue
            symptom = row[0]
            cnt_match = re.match(r"\s*(\d+)", row[2])
            if not cnt_match:
                continue
            count = int(cnt_match.group(1))
            if count < SAME_KIND_THRESHOLD:
                continue
            status = row[-1] if len(row) >= 4 else ""
            if _is_resolved(status):
                yield Finding(
                    SEV_INFO,
                    "A 活躍症狀",
                    f"「{symptom}」累計 {count} 次（已採結構性對策）",
                )
            else:
                yield Finding(
                    SEV_WARNING,
                    "A 活躍症狀",
                    f"「{symptom}」累計 {count} 次（≥{SAME_KIND_THRESHOLD}），"
                    "考慮升級為結構性閘門",
                )

    # 「## 🔴 閘門失效追蹤」段
    m_gate = re.search(
        r"##\s*🔴?\s*閘門失效追蹤\s*\n(.+?)(?=\n##|\Z)",
        content,
        re.DOTALL,
    )
    if m_gate:
        for row in _parse_table_rows(m_gate.group(1)):
            if len(row) < 3:
                continue
            gate_name = row[0]
            cnt_match = re.match(r"\s*(\d+)", row[2])
            if not cnt_match:
                continue
            count = int(cnt_match.group(1))
            if count < SAME_KIND_THRESHOLD:
                continue
            status = row[-1] if len(row) >= 4 else ""
            if _is_resolved(status):
                yield Finding(
                    SEV_INFO,
                    "A 閘門失效",
                    f"「{gate_name}」復發 {count} 次（已採結構性對策）",
                )
            else:
                yield Finding(
                    SEV_WARNING,
                    "A 閘門失效",
                    f"「{gate_name}」復發 {count} 次（≥{SAME_KIND_THRESHOLD}），"
                    "檢查是否需結構性審查（退役/降級/重新問 WHO）",
                )


# ─── C：淬鍊師 lessons INDEX 同步 ──────────────────────────────────

def check_lessons_sync() -> Iterator[Finding]:
    if not INDEX_FILE.exists():
        yield Finding(SEV_BLOCKER, "C", f"INDEX.md 不存在：{INDEX_FILE}")
        return
    if not LESSONS_ROOT.exists():
        yield Finding(SEV_BLOCKER, "C", f"lessons/ 目錄不存在：{LESSONS_ROOT}")
        return

    index_content = INDEX_FILE.read_text(encoding="utf-8")

    # 1. INDEX 「最後生成：YYYY-MM-DD」
    m_gen = re.search(r"最後生成：(\d{4}-\d{2}-\d{2})", index_content)
    index_gen_date: date | None = None
    if m_gen:
        try:
            index_gen_date = datetime.strptime(m_gen.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass

    # 2. INDEX 「現役條目：N ｜ 已退役：M」
    m_stat = re.search(
        r"現役條目：\*?\*?(\d+)\*?\*?\s*[｜|]\s*已退役：\*?\*?(\d+)",
        index_content,
    )
    if not m_stat:
        yield Finding(
            SEV_WARNING,
            "C INDEX 統計",
            "INDEX.md 找不到「現役條目：N ｜ 已退役：M」格式",
        )
        index_active = -1
        index_invalid = -1
    else:
        index_active = int(m_stat.group(1))
        index_invalid = int(m_stat.group(2))

    # 3. 掃情境檔
    all_ids: set[str] = set()
    invalid_ids: set[str] = set()
    related_refs: set[str] = set()
    file_max_mtime: float = 0
    incomplete_entries: list[str] = []

    required_fields = {
        "id", "title", "one_liner", "category", "created_at",
        "invalid_at", "helpful_count", "harmful_count",
    }

    for fn in LESSON_CATEGORY_FILES:
        fp = LESSONS_ROOT / fn
        if not fp.exists():
            yield Finding(SEV_BLOCKER, "C 情境檔缺失", f"{fn} 不存在於 lessons/")
            continue
        file_max_mtime = max(file_max_mtime, fp.stat().st_mtime)
        text = fp.read_text(encoding="utf-8")

        for fm in _iter_frontmatters(text):
            entry_id = fm["id"]
            all_ids.add(entry_id)

            invalid_at = fm.get("invalid_at", "null")
            if invalid_at and invalid_at not in ("null", "~", ""):
                invalid_ids.add(entry_id)

            # 必填欄位檢查（觸發詞至少 2 個）
            missing = required_fields - set(fm.keys())
            if missing:
                incomplete_entries.append(
                    f"{entry_id} ({fn}) 缺欄位：{sorted(missing)}"
                )
            triggers_list = fm.get("_triggers", [])
            if not triggers_list or len(triggers_list) < 2:
                incomplete_entries.append(
                    f"{entry_id} ({fn}) triggers <2（schema 規範必填 ≥2）"
                )

            related_refs.update(fm.get("_related", []))

    # 補：掃 ARCHIVE.md 補退役條目 ID（避免 related 引用退役 ID 被誤判斷鏈）
    archive_file = LESSONS_ROOT / "ARCHIVE.md"
    if archive_file.exists():
        arch_text = archive_file.read_text(encoding="utf-8")
        for fm in _iter_frontmatters(arch_text):
            arch_id = fm.get("id")
            if arch_id:
                all_ids.add(arch_id)
                invalid_ids.add(arch_id)  # ARCHIVE 一律當退役

    file_active = len(all_ids - invalid_ids)
    file_invalid = len(invalid_ids)

    # 4. INDEX vs 情境檔統計
    if index_active >= 0 and index_active != file_active:
        yield Finding(
            SEV_WARNING,
            "C INDEX 統計脫鉤",
            f"INDEX 寫現役 {index_active} 條，情境檔實際 {file_active} 條 → "
            "跑 generate_lessons_index.py",
        )
    # 退役數允許 INDEX > 情境檔（已退役表可能不在情境檔內）
    # 但反過來（情境檔退役 > INDEX）就脫鉤了
    if index_invalid >= 0 and file_invalid > index_invalid:
        yield Finding(
            SEV_WARNING,
            "C INDEX 退役數脫鉤",
            f"情境檔退役 {file_invalid} 條 > INDEX 寫的 {index_invalid} 條 → "
            "跑 generate_lessons_index.py",
        )

    # 5. INDEX 過期
    if index_gen_date and file_max_mtime > 0:
        file_date = date.fromtimestamp(file_max_mtime)
        if file_date > index_gen_date:
            yield Finding(
                SEV_WARNING,
                "C INDEX 過期",
                f"情境檔最新修改 {file_date}，INDEX 最後生成 {index_gen_date} → "
                "跑 generate_lessons_index.py",
            )

    # 6. related[] 斷鏈
    missing_refs = related_refs - all_ids
    if missing_refs:
        yield Finding(
            SEV_WARNING,
            "C related 斷鏈",
            f"{len(missing_refs)} 個 related 指向不存在的 ID：{sorted(missing_refs)}",
        )

    # 7. frontmatter 必填欄位完整性
    if incomplete_entries:
        for msg in incomplete_entries:
            yield Finding(SEV_WARNING, "C 條目欄位", msg)


# ─── D：PF 殭屍預防 ────────────────────────────────────────────────

def check_pf_zombie() -> Iterator[Finding]:
    if not PF_FILE.exists():
        yield Finding(SEV_BLOCKER, "D", f"pending_followups.md 不存在：{PF_FILE}")
        return

    content = PF_FILE.read_text(encoding="utf-8")

    # 「## Active」區段（後面跟「（進行中）」或直接跟內容）
    m_active = re.search(
        r"##\s*Active.*?\n(.+?)(?=\n##|\Z)",
        content,
        re.DOTALL,
    )
    if not m_active:
        yield Finding(SEV_INFO, "D", "Active 區未找到（檔案可能格式變動）")
        return

    today = date.today()
    rows = list(_parse_table_rows(m_active.group(1)))
    if not rows:
        yield Finding(SEV_INFO, "D", "Active 區無 PF（全綠）")
        return

    for row in rows:
        if len(row) < 5:
            continue
        pf_id = row[0]
        opened = row[4]
        try:
            opened_date = datetime.strptime(opened, "%Y-%m-%d").date()
        except ValueError:
            yield Finding(
                SEV_WARNING,
                "D 日期格式",
                f"{pf_id} 開單日「{opened}」非 YYYY-MM-DD 格式",
            )
            continue
        days = (today - opened_date).days
        if days >= PF_ZOMBIE_DAYS:
            yield Finding(
                SEV_WARNING,
                "D PF 殭屍",
                f"{pf_id} 已掛 {days} 天（≥{PF_ZOMBIE_DAYS}），"
                "主動評估是否 Cancelled",
            )
        else:
            yield Finding(
                SEV_INFO,
                "D PF 健康",
                f"{pf_id} 已掛 {days} 天（<{PF_ZOMBIE_DAYS}）",
            )


# ─── 主程序 ────────────────────────────────────────────────────────

CHECKS = [
    ("A", "踩雷錄同類記憶 ≥3 警示", check_landmines_repeat),
    ("C", "淬鍊師 lessons 索引同步", check_lessons_sync),
    ("D", "PF 殭屍預防 (>30 天)", check_pf_zombie),
]


def main() -> int:
    print("⚒️ 火神鍛造 dogfood validator")
    print(f"   日期：{date.today()}")
    print()

    all_findings: list[Finding] = []
    for code, label, fn in CHECKS:
        print(f"【{code}】{label}")
        findings = list(fn())
        all_findings.extend(findings)
        # 過濾 INFO 級僅在無 WARNING/BLOCKER 時顯示
        warns_blockers = [f for f in findings if f.severity != SEV_INFO]
        infos = [f for f in findings if f.severity == SEV_INFO]
        if warns_blockers:
            for f in warns_blockers:
                print(f"   {f.severity} [{f.check}] {f.message}")
            # INFO 也順便列（給上下文）
            for f in infos:
                print(f"   {f.severity} [{f.check}] {f.message}")
        elif infos:
            for f in infos:
                print(f"   {f.severity} [{f.check}] {f.message}")
        else:
            print("   🟢 全綠")
        print()

    # 總結 + exit code
    has_blocker = any(f.severity == SEV_BLOCKER for f in all_findings)
    has_warning = any(f.severity == SEV_WARNING for f in all_findings)

    print("─" * 50)
    if has_blocker:
        print("🔴 BLOCKER——有東西必須處理")
        return 2
    elif has_warning:
        print("🟡 WARNING——有事項建議處理")
        return 1
    else:
        print("🟢 全綠")
        return 0


if __name__ == "__main__":
    sys.exit(main())
