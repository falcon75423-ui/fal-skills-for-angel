# lessons/ Schema

> 所有 lessons/*.md 教訓條目的 frontmatter 欄位定義。**INDEX.md 由腳本從此 schema 生成，禁止手編**。

---

## Frontmatter 欄位

每條教訓獨立一個 `---` YAML 區塊，後接教訓本體內容。

```yaml
---
id: M08                                    # 必填。延用既有 M## / S-INFRA-## / S-INFO-## 等編號
title: 讀者視角是品質的終極裁判              # 必填。一句話標題
one_liner: 規格通過 ≠ 讀者滿意，長文交付後必須切換讀者視角做體檢   # 必填。索引層一句話（≤ 50 字）
category: long_form_delivery               # 必填。主歸屬情境（見下方情境列表）
triggers:                                  # 必填。觸發脈絡（搜尋者會想到的詞，≥ 2 個）
  - 長文交付
  - 2000字以上
  - 品質自我驗證
related: [M24, M27, M29]                   # 選填。相關條目 ID list（載入時遞迴 2 層上限）
created_at: 2026-04-14                     # 必填。條目首次建立日期（沿用原教訓出處日期）
invalid_at: null                           # 必填。退役時戳（null = 現役）
invalid_reason: null                       # 選填。退役理由一句話（invalid_at 非空時必填）
superseded_by: null                        # 選填。被哪條新教訓取代（升級退役時填）
helpful_count: 7                           # 必填。引用 helpful 次數（沿用原計數）
harmful_count: 0                           # 必填。引用 harmful 次數
evidence:                                  # 必填。觸發實例（至少 1 條，最多 10 條）
  - YYYY-MM-DD 案件名 / 階段（範例）
  - YYYY-MM-DD 另一筆觸發紀錄
---

# 讀者視角是品質的終極裁判

（教訓本體內容：詳細說明、何時適用、反例、配套等）

## 何時觸發
...

## 配套
...

## 反例
...
```

---

## 情境（category）列表

六個情境檔，對應鍛造時會自然冒出的動作詞：

| category | 檔名 | 收什麼教訓 |
|----------|------|-----------|
| `long_form_delivery` | `long_form_delivery.md` | 長文交付（≥ 2000 字）的結構、風格、讀者視角、比例拿捏 |
| `structure_design` | `structure_design.md` | Skill 結構、架構、變動地圖、單一真相源、雙層掃描 |
| `verification` | `verification.md` | 驗證紀律、體檢清單、字面 vs 根本目的、診斷工具盲點 |
| `subcontract` | `subcontract.md` | 跨 Skill 協作、分包是對話、視角切換、聯合研判 |
| `skill_rework` | `skill_rework.md` | Skill 修繕、翻修、假設審計、生命週期、預設驗證、規格漂移 |
| `infrastructure` | `infrastructure.md` | 基建層設計、索引設計、schema 規範、工具鏈、腳本自動化 |

**歸類原則**：
- 每條教訓只歸**一個主 category**（primary file）
- 跨情境的關聯用 `related: []` 欄位，不複製條目
- 無法歸類 = 該教訓還不夠具體，留在 `ARCHIVE.md` 待再出現

---

## 退役機制（Bi-temporal）

退役 ≠ 刪除。條目永遠保留，退役時加 `invalid_at` 時戳 + `invalid_reason`。

**退役三種原因**：
1. **升級**：教訓升級為 SKILL.md 世界觀 / 鍛打閘門 → `superseded_by: SKILL.md#XXX`
2. **過時**：背景改變、教訓不再適用 → `invalid_reason: "背景改變：..."`
3. **合併**：被另一條教訓吸收 → `superseded_by: M##`

退役後的條目：
- 不出現在 INDEX.md 主表（由腳本過濾 invalid_at != null）
- 仍可被 related 引用（考古用）
- 移到該情境檔底部「已退役」section（人工整理，腳本不動）

---

## 載入機制

**顯式路由**（P1-1 起步版）：SKILL.md 進場偵察區塊明列「若本次任務涉及 X，讀 lessons/X.md」。

**遞迴 related 載入**：載入情境檔 A 時，檔內條目 `related[]` 指向的條目 ID **跨檔載入（2 層遞迴上限）**。

**觸發詞反向索引**：INDEX.md 腳本生成「觸發詞 → 條目 ID」反向表，供人類搜尋（模型載入仍以 category 為主）。

---

## 寫入新條目的 CLI（新增摩擦控制）

新增一條教訓只需兩步：
1. 打開對應情境檔（例 `lessons/verification.md`）
2. 複製 `_schema.md` 的 template 區塊貼到檔尾，填欄位

**禁止**：直接改 INDEX.md（會被下次 `tools/generate_lessons_index.py` 覆蓋）

---

## 為什麼這樣設計

- **索引投影**（原則 1）：INDEX.md 由腳本生成，人不手編，雙向脫鉤不可能發生
- **新增摩擦控制**（原則 4）：寫入新條目 = 貼 template + 填欄位 ≤ 1 分鐘
- **顯式路由**（原則 5）：先靠 SKILL.md 明列觸發情境，LLM 自動選檔延後觀察
- **bi-temporal**（Graphiti 精髓）：退役不刪，考古能力永遠在
