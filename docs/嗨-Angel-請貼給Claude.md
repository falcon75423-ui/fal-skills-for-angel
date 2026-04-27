# 嗨 Claude，請接管 Angel 的 fal-skills 安裝

> 這份檔案是寫給「Angel 的 IDE 裡那個你」看的。Angel 是電腦小白，只想跟你對話完成安裝。
> 你的工作：能你自己用 Bash 跑的 → 直接跑；必須 Angel 親手做的 → 暫停清楚告訴她做什麼，做完她說「好了」你繼續。

---

## 你要安裝的東西

GitHub repo：**https://github.com/falcon75423-ui/fal-skills-for-angel**

這是一個 Claude Code plugin（叫 `fal-pack`），內含六個 skill：
- 深度研究（偵察兵 🔭）
- 法眼（內容策展 👁️）
- 火神鍛造（工頭 ⚒️）
- 淬鍊師（冷眼工匠 ⚒️）
- 淬煉團（5 角色重兵器 🔥）
- playwright-cli（瀏覽器自動化）

---

## 進場第一件事

開場跟 Angel 說：

> 「嗨 Angel，我是 Claude，要幫妳裝 fal-skills 工具套組。整個過程約 40-60 分鐘，分成五個階段：
> 1. 裝基礎工具（10 分鐘）
> 2. 裝 skillful-mcp + notebooklm-mcp（10 分鐘）
> 3. 設定 API keys 跟 MCP 設定檔（15 分鐘）
> 4. 裝 fal-pack plugin（5 分鐘）
> 5. patch 顧問團 + 測試（10 分鐘）
>
> 大部分我自己跑，妳只要在我問妳時做幾件事：輸 Mac 密碼一次、申請 2 個 API key、複製貼上幾個東西。準備好了嗎？」

---

## 階段 1：裝基礎工具（你自己跑）

依序跑這些命令（每條跑完看 output 確認成功再跑下一條）：

### 1.1 確認是否有 Homebrew

```bash
which brew
```

**如果沒有**，告訴 Angel：
> 「我要裝 Homebrew（Mac 的軟體管家），這步需要妳的 Mac 開機密碼。我會幫妳跑命令，但會跳出 prompt 要妳貼密碼。請複製這條命令貼到 IDE 的內建終端機跑：」
>
> ```
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```
>
> 「跑完它會告訴妳要再貼兩條 echo 命令把 brew 加到 PATH，照貼即可。完成跟我說『brew 好了』。」

**如果已有 brew**，繼續下一步。

### 1.2 裝 Node.js（給 npm 用）

```bash
brew install nvm
mkdir -p ~/.nvm
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$(brew --prefix)/opt/nvm/nvm.sh" ] && \. "$(brew --prefix)/opt/nvm/nvm.sh"' >> ~/.zshrc
source ~/.zshrc
nvm install --lts
```

### 1.3 裝 uv（Python 工具管家）

```bash
brew install uv
```

### 1.4 裝 playwright-cli（瀏覽器自動化）

```bash
npm install -g @playwright/cli@latest
```

第一次跑會下載瀏覽器 1-2 GB，告訴 Angel 等 5 分鐘。

### 1.5 建 Chrome 小屋資料夾

```bash
mkdir -p "$HOME/playwright-chrome"
```

✅ 階段 1 完成。

---

## 階段 2：裝 skillful-mcp + notebooklm-mcp

這兩個工具的 Mac 安裝命令已經寫成兩段獨立訊息，Angel 直接貼給你即可。

跟 Angel 說：

> 「下一步要裝兩個工具：**skillful-mcp**（搜尋武器庫的中介層）跟 **notebooklm-mcp**（NotebookLM 接口）。
>
> 我準備了兩段訊息，請依序開下面兩個連結，把整段內容（從『嗨 Claude...』那行開始）複製貼給我，我會自動處理：
>
> 1. **skillful-mcp**: https://github.com/falcon75423-ui/fal-skills-for-angel/blob/main/docs/Angel-貼給Claude-skillful-mcp.md
> 2. **notebooklm-mcp**: https://github.com/falcon75423-ui/fal-skills-for-angel/blob/main/docs/Angel-貼給Claude-notebooklm-mcp.md
>
> 第一段我跑完會說『✅ 裝好了』再請妳貼第二段。第二段中間有一步妳要在瀏覽器登 Google 帳號（給 NotebookLM 用），到那一步我會告訴妳怎麼做。」

兩段都跑完，最後驗證：

```bash
which skillful-mcp
which notebooklm-mcp
```

兩個都印出路徑 = ✅ 階段 2 完成。

---

## 階段 3：申請 API keys + 設定 MCP 設定檔

### 3.1 引導 Angel 申請 Exa key

跟 Angel 說：

> 「請開瀏覽器到 **https://dashboard.exa.ai/**，用 Google 帳號註冊（免費）。註冊完進 Dashboard → API Keys，建一個新的 key 複製出來貼給我。」

### 3.2 引導 Angel 申請 Tavily key

> 「請開瀏覽器到 **https://app.tavily.com/**，用 Google 帳號註冊（免費 1,000 次/月）。註冊完進 Dashboard → API Keys，複製貼給我。」

### 3.3 把 keys 寫到 ~/.zshrc

拿到兩個 key 後，幫她寫進環境變數（**用 Edit/Write 工具直接幫她改 ~/.zshrc**，不要叫她手動編）：

加到 ~/.zshrc 末尾：

```bash
export EXA_API_KEY="她貼給你的 Exa key"
export TAVILY_API_KEY="她貼給你的 Tavily key"
```

然後跑：

```bash
source ~/.zshrc
```

### 3.4 下載 mcp.json template

```bash
mkdir -p ~/.skillful-mcp
curl -L "https://raw.githubusercontent.com/falcon75423-ui/fal-skills-for-angel/main/docs/mcp-template-mac.json" \
     -o ~/.skillful-mcp/mcp.json
```

### 3.5 把 notebooklm 接到 skillful-mcp 上面

template 裡 notebooklm 是 placeholder（key 叫 `_notebooklm_TODO`，因為當初不確定 Angel 會不會用）。階段 2 已經裝好 notebooklm-mcp，現在你用 Edit 工具直接改 `~/.skillful-mcp/mcp.json`：

把這段（包含整個 `_notebooklm_TODO` 物件）：

```json
"_notebooklm_TODO": {
  "_note": "Lester 用的是 https://github.com/jacob-bd/notebooklm-mcp-cli。等 Lester 給你具體安裝命令跟 binary 路徑後，把這段的 key 從 _notebooklm_TODO 改成 notebooklm，把 command 改成正確路徑（譬如 ~/.local/bin/notebooklm-mcp 或 uv 跑的命令）。",
  "command": "TBD-請等-Lester-給命令",
  "args": [],
  "description": "NotebookLM 本地工具 — 建 notebook、加 source、跑 deep research、產出 audio/video/podcast/infographic/slides。"
}
```

整段換成：

```json
"notebooklm": {
  "command": "notebooklm-mcp",
  "description": "NotebookLM 本地工具 — 建 notebook、加 source、跑 deep research、產出 audio/video/podcast/infographic/slides。"
}
```

> 注意點：
> - key 從 `_notebooklm_TODO` 改成 `notebooklm`（少了底線跟 _TODO）
> - 如果階段 2 跑 `which notebooklm-mcp` 印出來的不是純 `notebooklm-mcp` 而是某個完整路徑（譬如 `/Users/angel/.local/bin/notebooklm-mcp`），把 `command` 改成那個完整路徑

### 3.6 把 skillful-mcp 註冊進 Claude Code

```bash
claude mcp add skillful --scope user -- ~/.local/bin/skillful-mcp --config ~/.skillful-mcp/mcp.json
```

> 注意：如果 Lester 給的 binary 不在 `~/.local/bin/skillful-mcp`，這條命令的路徑要改成正確位置。

驗證：

```bash
claude mcp list
```

應該看到 `skillful: ... ✓ Connected`。

✅ 階段 3 完成。

---

## 階段 4：裝 fal-pack plugin（在 IDE 對話框跑斜線命令）

跟 Angel 說：

> 「現在裝 plugin 本體。我要妳在我們現在的對話框裡逐條輸入這些斜線命令（每條按 Enter 送出）：」

```
/plugin marketplace add falcon75423-ui/fal-skills-for-angel
```

```
/plugin install fal-pack@fal-skills
```

```
/reload-plugins
```

```
/plugin
```

最後一條會列出已裝 plugin，看到 `fal-pack` 就成功。

✅ 階段 4 完成。

---

## 階段 5：patch 顧問團 + 測試

### 5.1 patch 顧問團

Angel 之前裝過「顧問團 skill」，需要補一段協議讓它能跟「偵察兵」協作。

**你直接用 Edit 工具改檔案**：`~/.claude/skills/顧問團/SKILL.md`

完整 patch 內容看這裡：
**https://raw.githubusercontent.com/falcon75423-ui/fal-skills-for-angel/main/docs/顧問團連接協議.md**

照那份的「步驟 3」找到「## 互動指令」段，在表格末尾加兩行；如果沒有「## 生態系接口」段，照「步驟 2」整段加進去（在「## 互動指令」之前）。

改完跑：

```
/reload-plugins
```

### 5.2 重啟 Claude Code IDE

跟 Angel 說：

> 「最後一步：請完整關掉 Claude Code IDE 然後重開（不是只關對話框，要整個 app 退出），這樣 MCP 設定才會被讀進去。重開後告訴我『重開好了』。」

### 5.3 跑煙霧測試

她重開後，幫她在新對話試這幾個：

1. 「召喚法眼」—— 看法眼是否自我介紹
2. 「召喚偵察兵，偵察今天 AI 圈有什麼新工具」—— 偵察兵應該開始規劃路線
3. 「請呼叫 skillful 的 list_skills 看可用工具」—— 應該列出 Exa / Tavily / Chrome DevTools / Playwright

每個都正常 = 安裝成功。哪個壞跟她一起 debug。

---

## 你的行為守則

- **白話講話**——Angel 是電腦小白，禁用「frontmatter」「namespace」「OAuth」「SHA」這些術語，必要時用比喻
- **每跑一條 bash 命令前都先簡短說「我要做 X，原因是 Y」**——讓她跟得上你在做什麼
- **你能自己用 Bash 跑的就跑**，不要叫她貼到終端機（除非命令需要她的密碼）
- **必須她做的事（瀏覽器點按鈕、申請 key、輸密碼）**寫清楚後暫停，說「做完跟我說『好了』」
- **遇到任何錯誤先試自己 debug**，三次試不出再叫她截圖傳給 Lester
- **每階段結束跟她講「✅ 第 X 階段完成，目前進度 X/5」**——讓她知道進度

---

## 卡關時聯絡方式

任何卡 5 分鐘以上的問題，請 Angel：
1. 把對話最後 10 句截圖
2. 貼進跟 Lester 的訊息

Lester 會直接看你卡在哪。
