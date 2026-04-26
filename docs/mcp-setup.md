# MCP 工具設定

`fal-pack` 的搜尋武器庫透過 **`skillful-mcp`** 中介層調用底層工具
（NotebookLM / Tavily / Exa / Chrome DevTools / Playwright / paper-search 等）。

要讓 skill 可以正常工作，這層 MCP 必須先設好。

---

## 1. 安裝 skillful-mcp

> ⚠️ **這一步請另外跟分享者拿安裝指引**——`skillful-mcp` 不在公開 PyPI，
> 通常需要分享者直接給你 git clone URL 或私有 token。

預期流程大致長這樣（請以分享者實際提供的為準）：

```bash
# 範例（實際命令依分享者提供為準）
uv tool install --from <skillful-mcp 的 git URL> skillful-mcp

# 或者 clone 後本地裝：
# git clone <skillful-mcp git URL> ~/skillful-mcp
# cd ~/skillful-mcp
# uv tool install -e .
```

驗證 server 本體可呼叫：

```bash
which skillful-mcp
```

---

## 2. 申請各家 API key

`skillful-mcp` 內部會調用幾家服務。你需要分別到各家網站申請：

| 服務 | 用途 | 申請網址 | 是否必要 |
|------|------|----------|---------|
| **Exa** | 語意搜尋（深度研究、法眼必用）| https://dashboard.exa.ai/ | 🔴 必要 |
| **Tavily** | 廣度搜尋 + 網站爬蟲 + 日期過濾 | https://app.tavily.com/ | 🟡 建議（免費額度 1,000/月）|
| **NotebookLM** | 學術論文 + YouTube 逐字稿 | 需 `nlm` CLI 登入 Google | 🟡 建議（用法眼跟深度研究都會更強） |
| Anthropic API | 通常 Claude Code 已有 | https://console.anthropic.com/ | ✅ 已就緒 |

把拿到的 key 都暫時記下來，下一步會用到。

---

## 3. 把 skillful-mcp 加進 Claude Code

```bash
# 把 skillful-mcp 註冊成 stdio MCP server，並把 API keys 透過環境變數傳進去：
claude mcp add skillful-mcp --scope user \
  -e EXA_API_KEY=你的Exa金鑰 \
  -e TAVILY_API_KEY=你的Tavily金鑰 \
  -- skillful-mcp
```

> 命令細節以分享者提供的 skillful-mcp README 為準。

驗證 server 連得上：

```bash
claude mcp list
```

應該看到 `skillful-mcp` 列在裡面，狀態是 `connected`。

---

## 4. NotebookLM 認證（額外步驟）

NotebookLM 走 Google session cookie，不用 API key 但要登入一次：

```bash
nlm login
```

會跳出瀏覽器讓你登入 Google 帳號。Cookie 約 2-3 週有效，過期再跑一次。

> 🔴 法眼 skill 啟動時會自動探測 NotebookLM 認證，過期會主動提醒你重跑。

---

## 5. 驗證 MCP 工具可用

開啟 Claude Code，問它：

```
請呼叫 skillful-mcp 的 list_skills 看可用工具
```

如果 Claude 回覆能列出 `notebooklm` / `tavily` / `exa` / `playwright` 等子 skill，就 OK 了。

---

## 故障排除

| 症狀 | 解法 |
|------|------|
| `claude mcp list` 看不到 skillful-mcp | 重跑 `claude mcp add` 命令；確認 `which skillful-mcp` 有結果 |
| 顯示 connected 但 LLM 說「找不到工具」| 重啟 Claude Code（換新對話）|
| Exa/Tavily 報 401/403 | API key 沒設好；用 `claude mcp get skillful-mcp` 看 env vars |
| NotebookLM 失敗 | 跑 `nlm login --check` 看認證狀態；過期就重 login |

---

## 下一步

→ 回 [README.md](../README.md) 第 3 步「安裝 plugin」。
