# fal-skills-for-angel

> 一份分享給朋友的 Claude Code skill 套組——把「深度研究 + 內容策展 + 瀏覽器自動化 + 鍛造工坊」一次裝到位。

## 內容

這個 repo 包一個 Claude Code plugin：**fal-pack**，內含六個 skill：

**研究與策展**
- 🔭 **深度研究**（偵察兵）——深入調研、市場研究、技術選型、趨勢分析
- 👁️ **法眼**——高品質內容篩選、主題策展、每日精選報

**鍛造工坊**（造 skill 的工具——當你想自己造新 skill 時用）
- ⚒️ **火神鍛造**（工頭）——主導 skill 鍛造（選料 / 鍛打 / 淬火），把意識結晶成可呼吸的工具
- ⚒️ **淬鍊師**（冷眼工匠）——鍛造完工後做知識淬鍊、三情境衝撞驗證、世界觀升級
- 🔥 **淬煉團**——5 角色多視角碰撞重兵器（淬鍊師上游淬鍊時召喚）

**底層工具**
- 🎭 **playwright-cli**——瀏覽器自動化（抓網頁、自動填表、E2E 測試）

外加：
- 📡 **顧問團連接協議**——讓深度研究跟你已裝的「顧問團 skill」做聯合研判

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

如果你不想叫他們「偵察兵」「法眼」「工頭」「淬鍊師」，想取自己的化身名，
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

## 故障排除

- **找不到 skill**：跑 `/reload-plugins`；還不行就檢查 `/plugin` 看 fal-pack 是否啟用
- **Skill 喊「skillful-mcp 配置可能出問題」**：檢查 `claude mcp list` 看 server 有沒有跑起來
- **網頁抓不到**：看 [docs/installation-mac.md](docs/installation-mac.md) 確認 `playwright-cli` 全域可呼叫，再依 SKILL.md 設好 Chrome 小屋

## 安全與隱私說明

本套組**不含**任何 Lester 個人累積的智慧資產（lessons / 歷史鍛造紀錄 / 客戶檔案）。
你拿到的是「乾淨的工具框架」——`memory/` 跟 `lessons/` 為空，等你自己累積。

## License

本套組為私人分享版本。

## 維護者

`fal-skills` marketplace（請見 `.claude-plugin/marketplace.json`，安裝時記得把 `owner.name` 換成你的名字）。
