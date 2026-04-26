# 法眼 巡兵器來源名單 — Skill / MCP 開源工具

> 最後更新：2026-04-01
> 偵察輪次：1 輪（初始建立）
> 用途：巡兵器掃描時使用，追蹤近一週動量最強的 skill / MCP server / agent 工具

---

## 品味校準：什麼樣的 Skill 值得上版面

- 不是星星最多的（那是歷史排行榜），是**此刻正在起飛的**
- 週增量 > 絕對星數（動量優先）
- 解決真實痛點，不是 demo 玩具
- README 品質是門檻——爛 README 直接跳過
- Fork 換皮、awesome-list 搬運不算

---

## Tier 1 — 必掃

| 平台 | 類型 | 核心價值 | 搜尋方式 |
|------|------|---------|---------|
| **GitHub Trending** | 開源 repo | 全球開發者動量最直接的信號 | WebSearch "github trending weekly" + 篩 skill/MCP/agent 相關 |
| **SkillsMP** (skillsmp.com) | Skill 市集 | 700K+ skills，有品質篩選（最低 2 星）、職業分類 | Exa / WebSearch 搜最新上架或熱門 |
| **Smithery** (smithery.ai) | MCP registry | 8,000+ MCP servers，最大的 MCP 生態索引 | Exa / WebSearch 搜新增或熱門 |
| **ClaudeMarketplaces** (claudemarketplaces.com) | 社群目錄 | 150+ Claude Code skills，有社群投票+評分+安裝數 | WebFetch 直接掃 |

---

## Tier 2 — 定期看

| 平台 | 類型 | 核心價值 |
|------|------|---------|
| **SkillStore** (skillstore.io) | Skill 市集 | Prompt engineering 導向，開發/自動化/內容創作 |
| **mcp.so** | MCP 目錄 | 6,000+ MCP servers |
| **Glama** (glama.ai/mcp) | MCP 目錄 | 20,000+ MCP servers，覆蓋最廣 |
| **SkillsLLM** (skillsllm.com) | Skill 市集 | AI skills marketplace |
| **MCP Directory** (mcpdirectory.app) | MCP 目錄 | Skills + packages，有 blog 推薦 |
| **awesome-claude-code** (GitHub) | 清單 | 28.5K stars，社群中央索引 |
| **awesome-claude-plugins** (GitHub) | 追蹤器 | 自動化追蹤 plugin adoption metrics |
| **Product Hunt** (AI category) | 產品發現 | AI 工具新品，非純開源但有信號 |

---

## Tier 3 — 偶爾看看

| 平台 | 核心價值 |
|------|---------|
| **LobeHub Skills** (lobehub.com/skills) | Agent skills 整合平台 |
| **MCP Bundles** (mcpbundles.com) | 500+ providers 聚合 |
| **Reddit** (r/ClaudeAI, r/LocalLLaMA) | 社群討論新工具、使用心得 |
| **Hacker News** ("Show HN") | 開發者自己做的工具，品質參差但偶有驚豔 |

---

## 搜尋關鍵字範例（動態調整）

- `Claude Code skill`、`MCP server`、`AI agent tool`
- `SKILL.md`、`claude plugin`、`coding assistant extension`
- `agentic workflow tool`、`AI automation`
- 當週特定熱點（如新模型發布帶動的工具生態）

---

## 排除標準

- Fork 換皮（改個 README 就上架）→ 跳過
- 星星灌水明顯（星星數和 commit 歷史不成比例）→ 跳過
- README 品質低（沒有清楚的安裝說明和功能描述）→ 跳過
- Awesome-list 搬運（只是連結集合沒有自己的東西）→ 跳過
- 已失活 repo（超過 3 個月沒更新）→ 跳過，除非功能仍有獨特價值
