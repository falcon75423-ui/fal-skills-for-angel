# 貼給 Claude（階段 2B）：裝 notebooklm-mcp

> Angel：把整段複製貼進 Claude Code IDE 對話框，按 Enter 送出。
>
> 中間有一步要妳用 Google 帳號登入（瀏覽器會自動跳出來），Claude 會在那一步暫停告訴妳怎麼做。

---

嗨 Claude，我是 Lester。請幫 Angel 裝 **notebooklm-mcp**——Python 寫的 NotebookLM 接口工具，讓 Claude 能呼叫 NotebookLM 建 notebook、加 source、跑 deep research、產出 audio/video/podcast/infographic/slides。

整個過程約 5-10 分鐘。**這個工具第一次用要 Angel 用她的 Google 帳號登入**——你跑到那一步時暫停，跟她說怎麼操作。

## 前提檢查：uv 已裝好

```bash
which uv
```

- 印出路徑 → 繼續步驟 1
- 沒結果 → 跑 `brew install uv`，然後重試

## 步驟 1：用 uv 安裝

```bash
uv tool install notebooklm-mcp-cli
```

這會花 1-2 分鐘下載 Python 依賴。看到「Installed N executables: notebooklm-mcp, nlm」就成功。

## 步驟 2：確認兩個 binary 路徑

```bash
which notebooklm-mcp
which nlm
```

預期兩個都印出路徑（通常是 `/Users/<angel>/.local/bin/notebooklm-mcp` 跟 `.../nlm`）。

如果其中一個 `which` 沒結果 → 跑：

```bash
uv tool update-shell
source ~/.zshrc
```

然後重試 `which`。

## 步驟 3：Google OAuth 登入（要 Angel 親手做）

跟 Angel 說：

> 「下一步要妳用 Google 帳號登入 NotebookLM。我會跑一條命令，它會自動打開瀏覽器，妳照畫面登入就好。**用妳平常用 NotebookLM 的同一個 Google 帳號**。登入完成、瀏覽器顯示成功訊息後，回來告訴我『登好了』。」

然後跑：

```bash
nlm login
```

等 Angel 說「登好了」，繼續步驟 4。

> 如果瀏覽器沒自動跳，命令會印出一個網址，請她手動複製貼到瀏覽器。

## 步驟 4：驗證登入 + 整體體檢

```bash
nlm login --check
nlm doctor
```

`nlm doctor` 會印一份體檢報告，所有項目顯示綠色勾或「OK」就成功。

如果看到 `not authenticated` → 重跑 `nlm login`。

## 步驟 5：完成

跟 Angel 說：

> 「✅ notebooklm-mcp 裝好了，**階段 2 全部完成**。我們繼續階段 3，去申請 Exa 跟 Tavily 的 API key。
>
> 注意：notebooklm 怎麼接到 skillful-mcp 上面（改 mcp.json 那段），會在階段 3 下載 mcp.json template 後一起做，不用現在動手。」

## 卡住怎麼辦

- `uv tool install` 失敗 → 確認 `uv --version` 有結果；沒有就重裝 uv（`brew reinstall uv`）
- `nlm login` 卡住或瀏覽器沒跳出來 → 看 terminal 印的網址，叫 Angel 手動貼到瀏覽器
- `nlm doctor` 顯示一堆紅字 → 截圖請 Angel 傳給 Lester

任何一步卡超過 5 分鐘，請 Angel 把對話最後 10 句截圖傳給 Lester。
