# fal-skills-for-angel

> 一份分享給朋友的 Claude Code skill 套組——把「深度研究 + 內容策展 + 鍛造工坊 + 文件工程 + 視覺設計 + 瀏覽器自動化」一次裝到位。

## 內容

這個 repo 包一個 Claude Code plugin：**fal-pack**，內含九個 skill：

**研究與策展**
- 🔭 **深度研究**（偵察兵）——深入調研、市場研究、技術選型、趨勢分析
- 👁️ **法眼**——高品質內容篩選、主題策展、每日精選報

**鍛造工坊**（造 skill 的工具——當你想自己造新 skill 時用）
- ⚒️ **火神鍛造**（工頭）——主導 skill 鍛造（選料 / 鍛打 / 淬火），把意識結晶成可呼吸的工具
- ⚒️ **淬鍊師**（冷眼工匠）——鍛造完工後做知識淬鍊、三情境衝撞驗證、世界觀升級
- 🔥 **淬煉團**——5 角色多視角碰撞重兵器（淬鍊師上游淬鍊時召喚）

**文件工程** ⚠️ Windows-only（Mac 可用 50-60% 純 Python 功能）
- 📊 **表格地下司令**（表哥）——Excel 精密工程：格式鎖定、模板公版化、三層驗證、CJK 字寬感知
- 📄 **文本參謀長**（表弟）——頂級出版商級 Word 文件工程：三引擎精密產出、四重校對零容忍

**前端設計**
- 🔪 **剃刀**（impeccable）——對 AI slop 過敏的前端設計總監，視覺蒸餾器。剃除冗餘，做出不像 AI 做的介面

**底層工具**
- 🎭 **playwright-cli**——瀏覽器自動化（抓網頁、自動填表、E2E 測試）

外加：
- 📡 **顧問團連接協議**——讓深度研究跟你已裝的「顧問團 skill」做聯合研判

> ⚠️ **平台說明**：表哥/表弟依賴 `pywin32` + Excel/Word COM，Mac 上 `pip install pywin32` 會失敗、COM 相關功能（修改既有檔/PDF/Track Changes/品檢二讀）不可用。Mac 用戶仍可用兩 skill 的純 Python 部分（openpyxl 生成新檔、python-docx 編輯）約 50-60% 功能。impeccable / 其他 skill 跨平台 OK。

## 安裝路徑（給 Mac 使用者）

完整流程約 30-45 分鐘。三大階段：

### 1. 環境準備

裝 Homebrew、Node.js（≥ 18）、Python uv、`playwright-cli`。

詳細命令見 [docs/installation-mac.md](docs/installation-mac.md)。

### 2. 安裝 skillful-mcp + 設定 API keys

`skillful-mcp` 是搜尋武器庫的中介層（封裝 Exa / Tavily / NotebookLM 等）。
要先裝 server 本體，再設定各家服務的 API key。

詳細命令見 [docs/mcp-setup.md](docs/mcp-setup.md)。

### 3. 透過 plugin marketplace 安裝 fal-pack

```bash
# 在你的 Claude Code 對話框輸入：
/plugin marketplace add <你拿到的 GitHub URL>
/plugin install fal-pack@fal-skills
```

安裝完跑 `/reload-plugins` 載入。

### 4. 把連接協議補進你已有的顧問團

如果你已經裝了「顧問團 skill」，請依 [docs/顧問團連接協議.md](docs/顧問團連接協議.md) 的指引，
把「聯合研判」段落補進你的 `~/.claude/skills/顧問團/SKILL.md`。

### 5.（可選）改成你自己的化身名

如果你不想叫他們「偵察兵」「法眼」「工頭」「淬鍊師」「表哥」「表弟」「剃刀」，想取自己的化身名，
請看 [docs/個人化客製.md](docs/個人化客製.md)。

## 觸發詞

裝好之後可以直接這樣呼叫：

| 場景 | 召喚詞 |
|------|--------|
| 想做深度研究 | 「召喚偵察兵」「偵察 [主題]」「深度研究 [主題]」 |
| 想要每日精選 | 「召喚法眼」「今天有什麼好文章」「召喚法眼 [主題]」 |
| 偵察兵 + 顧問團聯合 | 「聯合研判 [主題]」「聯合研判 [主題] 跑 N 輪」 |
| 想造一個新 skill | 「召喚工頭」「召喚火神」「幫我建一個 skill」「翻修 X」 |
| 鍛造完做知識淬鍊 | 「召喚淬鍊師」「淬煉這個 X」「淬煉這次經驗」 |
| 高張力議題碰撞 | 「召喚淬煉團」「淬煉團來看 X」 |
| 做 Excel 表格 | 「召喚表哥」「幫我做 Excel」「做一個表格」（Windows-only） |
| 做 Word 文件 | 「召喚表弟」「幫我做 Word」「做一份文件」「排版」（Windows-only） |
| 前端設計 / UI 改造 | 「召喚剃刀」「polish UI」「critique 設計」「craft 這個 feature」 |

## 故障排除

- **找不到 skill**：跑 `/reload-plugins`；還不行就檢查 `/plugin` 看 fal-pack 是否啟用
- **Skill 喊「skillful-mcp 配置可能出問題」**：檢查 `claude mcp list` 看 server 有沒有跑起來
- **網頁抓不到**：看 [docs/installation-mac.md](docs/installation-mac.md) 確認 `playwright-cli` 全域可呼叫，再依 SKILL.md 設好 Chrome 小屋
- **表哥/表弟 ImportError: No module named 'win32com'**：Mac 環境下無法用 COM 部分；純 Python 功能（openpyxl 生成 xlsx、python-docx 編輯 docx）仍可使用

## 安全與隱私說明

本套組**不含**任何個人累積的智慧資產（lessons / 歷史鍛造紀錄 / 客戶檔案）。
你拿到的是「乾淨的工具框架」——`memory/` 跟 `lessons/` 為空，等你自己累積。

火神鍛造的 `clients/` 只含 SOP 骨架（`_templates/工作簿.md` + 空白 `_index.md` + `pending_followups.md`），
你照模板建立自己的客戶資料夾即可。

## License

本套組為私人分享版本。

## 維護者

`fal-skills` marketplace（請見 `.claude-plugin/marketplace.json`，安裝時記得把 `owner.name` 換成你的名字）。
