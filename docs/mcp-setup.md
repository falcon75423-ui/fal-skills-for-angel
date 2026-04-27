# MCP 工具設定（Mac 完整版）

`fal-pack` 的搜尋武器庫透過 **`skillful-mcp`** 中介層調用底層工具
（Exa、Tavily、Chrome DevTools、Playwright；NotebookLM 之後另外加）。

要讓 skill 可以正常工作，這層 MCP 必須先設好。整個流程約 20 分鐘。

> 💡 **如果你正在用 IDE 裡的 Claude 接管安裝**，Claude 會幫你跑下面大部分命令，
> 你只要在被要求時提供 API key 跟 Mac 密碼即可。

---

## 第一步：裝 skillful-mcp 本體

skillful-mcp 是「中介層」——它把多個下游 MCP servers 包成一個給 Claude Code 用。

Mac 兩種裝法（**選一個**）：

### 方法 A：下載官方 binary（最快，1 分鐘）

```bash
# Apple Silicon Mac (M1/M2/M3/M4)：
mkdir -p ~/.local/bin
curl -L "https://github.com/kurtisvg/skillful-mcp/releases/download/v0.1.0/skillful-mcp_0.1.0_darwin_arm64" -o ~/.local/bin/skillful-mcp
chmod +x ~/.local/bin/skillful-mcp

# Intel Mac：
mkdir -p ~/.local/bin
curl -L "https://github.com/kurtisvg/skillful-mcp/releases/download/v0.1.0/skillful-mcp_0.1.0_darwin_amd64" -o ~/.local/bin/skillful-mcp
chmod +x ~/.local/bin/skillful-mcp
```

> 不確定你是 Apple Silicon 還是 Intel？跑 `uname -m`。`arm64` = Apple Silicon，`x86_64` = Intel。

把 `~/.local/bin` 加到 PATH（如果還沒在）：

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

驗證：

```bash
which skillful-mcp
skillful-mcp --version
```

### 方法 B：從 source 裝（要 Go 1.25+）

```bash
brew install go
go install github.com/kurtisvg/skillful-mcp@latest
```

驗證：

```bash
which skillful-mcp
```

---

## 第二步：申請 API keys

需要兩家服務的 key（都有免費額度）：

| 服務 | 用途 | 申請網址 | 免費額度 |
|------|------|----------|---------|
| **Exa** | 語意搜尋（深度研究、法眼必用）| https://dashboard.exa.ai/ | 有免費 tier |
| **Tavily** | 廣度搜尋 + 網站爬蟲 | https://app.tavily.com/ | 1,000 次/月 |

操作：

1. 開兩個網站，分別**用 Google 帳號**或 email 註冊
2. 進 Dashboard → API keys 區
3. 各複製一個 key 出來，**待會要設成環境變數**

---

## 第三步：把 API keys 設成環境變數

打開 `~/.zshrc`：

```bash
open -e ~/.zshrc
```

加進這兩行（把 `xxxxx` 換成剛申請到的 key）：

```bash
export EXA_API_KEY="xxxxx-你的-Exa-key"
export TAVILY_API_KEY="xxxxx-你的-Tavily-key"
```

存檔，回終端機跑：

```bash
source ~/.zshrc
```

驗證：

```bash
echo $EXA_API_KEY  # 應該印出你的 key
echo $TAVILY_API_KEY
```

---

## 第四步：建 skillful-mcp 設定檔

```bash
mkdir -p ~/.skillful-mcp
```

從 repo 下載 template：

```bash
curl -L "https://raw.githubusercontent.com/falcon75423-ui/fal-skills-for-angel/main/docs/mcp-template-mac.json" \
     -o ~/.skillful-mcp/mcp.json
```

> 這個 template 已經設好 Exa + Tavily + Chrome DevTools + Playwright 四個 server，API key 透過環境變數讀取。

---

## 第五步：把 skillful-mcp 註冊進 Claude Code

```bash
claude mcp add skillful --scope user -- ~/.local/bin/skillful-mcp --config ~/.skillful-mcp/mcp.json
```

驗證：

```bash
claude mcp list
```

應該看到：

```
skillful: ~/.local/bin/skillful-mcp --config ~/.skillful-mcp/mcp.json - ✓ Connected
```

---

## 第六步：重啟 Claude Code IDE

關閉 IDE 重開，讓它讀新的 MCP 設定。

---

## 第七步：驗證（在 Claude Code 對話框跑）

問 Claude：

```
請呼叫 skillful 的 list_skills 看可用工具
```

如果看到 `tavily` / `exa` / `chrome-devtools` / `playwright` 出現在列表，就成功了。

---

## NotebookLM（之後加）

分享者用的是 https://github.com/jacob-bd/notebooklm-mcp-cli（Python 寫的，用 uv 安裝）。

請跟分享者拿具體 Mac 安裝命令（會涉及 Google 帳號登入流程）。

裝完後編輯 `~/.skillful-mcp/mcp.json`，把 `_notebooklm_TODO` 區塊改名成 `notebooklm`，填入正確的 command/args（分享者會告訴你完整內容）。

---

## 故障排除

| 症狀 | 解法 |
|------|------|
| `claude mcp list` 看不到 skillful | 確認 `which skillful-mcp` 有結果；如果沒 PATH 加好就重跑第一步 |
| `skillful: ✗` connection failed | 跑 `~/.local/bin/skillful-mcp --config ~/.skillful-mcp/mcp.json` 看錯誤訊息 |
| Exa / Tavily 報 401 | API key 沒生效；跑 `echo $EXA_API_KEY` 確認；沒值就重新 `source ~/.zshrc` |
| 顯示 connected 但 LLM 說「找不到工具」 | 重啟 Claude Code IDE（不是只關對話框，是整個 app 退出再開） |

---

## 下一步

回 [README.md](../README.md) 第 3 步「安裝 plugin」。
