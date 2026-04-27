# 貼給 Claude（階段 2A）：裝 skillful-mcp

> Angel：到階段 2 時，從下方分隔線開始整段複製貼進 Claude Code IDE 對話框，按 Enter 送出就好。
>
> 中間如果問妳問題就照畫面回答，全部跑完 Claude 會跟妳說「✅ skillful-mcp 裝好了」。

---

嗨 Claude，我是 Lester。請幫 Angel 裝 **skillful-mcp**——Go 寫的 MCP 中介層，會把多個下游 MCP servers 包成一個給 Claude Code 用，是 fal-pack 的必要前置工具。

整個過程約 3-5 分鐘，**全部你自己用 Bash 跑**，不需要 Angel 動手（這些命令也不需要她的 Mac 密碼）。依序執行，每條跑完看 output 確認成功再跑下一條。

## 步驟 1：偵測 Mac 架構

```bash
uname -m
```

- 結果 `arm64` → Apple Silicon（M1/M2/M3/M4），跑步驟 2A
- 結果 `x86_64` → Intel Mac，跑步驟 2B

## 步驟 2A：下載 binary（Apple Silicon）

```bash
mkdir -p ~/.local/bin
curl -L "https://github.com/kurtisvg/skillful-mcp/releases/download/v0.1.0/skillful-mcp_0.1.0_darwin_arm64" -o ~/.local/bin/skillful-mcp
chmod +x ~/.local/bin/skillful-mcp
```

## 步驟 2B：下載 binary（Intel）

```bash
mkdir -p ~/.local/bin
curl -L "https://github.com/kurtisvg/skillful-mcp/releases/download/v0.1.0/skillful-mcp_0.1.0_darwin_amd64" -o ~/.local/bin/skillful-mcp
chmod +x ~/.local/bin/skillful-mcp
```

## 步驟 3：把 ~/.local/bin 加到 PATH（如果還沒）

```bash
grep -q '.local/bin' ~/.zshrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 步驟 4：驗證

```bash
which skillful-mcp
skillful-mcp --version
```

預期 output：
- `which` 印出類似 `/Users/angel/.local/bin/skillful-mcp`
- `--version` 印出 `v0.1.0` 或類似版本字串

兩條都正常 → 跟 Angel 說：

> 「✅ skillful-mcp 裝好了。接下來請貼第二段訊息（裝 notebooklm-mcp）給我。」

## 卡住怎麼辦

任何一步失敗 → 把完整錯誤訊息（連同你跑的命令）貼給 Angel，請她截圖傳給 Lester。**不要自己亂猜**，這個工具版本敏感，Lester 比較知道哪裡出問題。
