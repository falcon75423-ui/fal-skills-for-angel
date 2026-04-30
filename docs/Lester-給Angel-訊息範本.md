# Lester 傳給 Angel 的訊息範本

> 這是一份「給 Lester 拿來傳給 Angel」的訊息範本。Lester 看完整段，挑想用的版本（短版或長版），複製內容傳到 LINE / iMessage / Email 給 Angel。
>
> 可以照原樣傳，也可以改成自己語氣。

---

## 短版（推薦，3 段傳）

### 第 1 段：開場 + 工具介紹

```
嗨 Angel 👋

幫妳裝的工具套組「fal-skills」做好了，今天可以開始裝。

裡面有 9 個 skill 會大幅升級妳的 Claude 助手：

🔭 深度研究（偵察兵）— 幫妳上網挖資料、做主題研究
👁️ 法眼 — 幫妳看文章/影片/podcast 篩選有價值的內容
⚒️ 火神鍛造 — 幫妳客製打造新的 skill
⚒️ 淬鍊師 — 把零散經驗淬煉成可重用的工具
🔥 淬煉團 — 5 個角色互相辯論幫妳想清楚問題
🔪 剃刀（impeccable）— 對 AI slop 過敏的前端設計總監，做網頁/UI 用
📊 表哥（表格地下司令）— Excel 精密工程 ⚠️ Windows-only
📄 表弟（文本參謀長）— Word 文件工程 ⚠️ Windows-only
🌐 playwright-cli — 自動操作瀏覽器（截圖、填表單）

⚠️ 表哥/表弟在 Mac 進階功能（PDF/校對/Track Changes）跑不起來，但生成新檔的基本功能仍 OK；一起裝著也沒成本，未來換 Windows 或跟 Windows 同事合作就能完整跑。

整個安裝大概 40-60 分鐘，妳什麼都不用懂技術，Claude 會一步一步帶妳走。
```

### 第 2 段：怎麼開始

```
【怎麼開始】

1. 打開妳的 Claude Code IDE，新開一個對話
2. 把下面這段話完整貼進去，按 Enter 送出：

---貼這段給 Claude---

嗨 Claude，請幫我裝 fal-skills 工具套組。完整指示在這裡：

https://raw.githubusercontent.com/falcon75423-ui/fal-skills-for-angel/main/docs/嗨-Angel-請貼給Claude.md

請先讀這份指引，然後照裡面的「進場第一件事」開始引導我。

---貼到這裡為止---

3. Claude 會跟妳打招呼確認，妳說「準備好了」它就開始
4. 中間它會問妳幾個問題（例如要不要裝某工具、要不要申請 API key），照畫面回答就好
```

### 第 3 段：先準備 + 卡關時

```
【先準備這幾樣，安裝中會用到】

- 妳的 Mac 開機密碼（裝 Homebrew 那一步會用一次）
- 妳的 Google 帳號（申請 2 個免費 API key + 之後登入 NotebookLM）

【卡關時找我】

任何卡 5 分鐘以上的問題：
1. 把 Claude 對話最後 10 句截圖
2. 傳給我

我直接看你卡哪。

加油，妳沒問題的 💪
```

---

## 長版（一次傳，不分段）

```
嗨 Angel 👋

幫妳裝的工具套組「fal-skills」做好了，今天可以開始裝。

裡面有 9 個 skill 會大幅升級妳的 Claude 助手：

🔭 深度研究（偵察兵）— 上網挖資料、做主題研究
👁️ 法眼 — 篩選有價值的文章/影片/podcast
⚒️ 火神鍛造 — 客製打造新的 skill
⚒️ 淬鍊師 — 把零散經驗淬煉成可重用工具
🔥 淬煉團 — 5 個角色辯論幫妳想清楚
🔪 剃刀（impeccable）— 對 AI slop 過敏的前端設計總監
📊 表哥（表格地下司令）— Excel 精密工程 ⚠️ Windows-only
📄 表弟（文本參謀長）— Word 文件工程 ⚠️ Windows-only
🌐 playwright-cli — 自動操作瀏覽器

⚠️ 表哥/表弟 Mac 上進階功能（PDF/校對）跑不起來，基本生成仍 OK，先裝著未來換機可用。

整個安裝大概 40-60 分鐘，妳什麼都不用懂技術，Claude 會一步一步帶妳走。

【怎麼開始】

1. 打開 Claude Code IDE，新開一個對話
2. 把下面這段完整貼進去按 Enter：

——貼這段給 Claude——
嗨 Claude，請幫我裝 fal-skills 工具套組。完整指示在這裡：
https://raw.githubusercontent.com/falcon75423-ui/fal-skills-for-angel/main/docs/嗨-Angel-請貼給Claude.md
請先讀這份指引，然後照「進場第一件事」開始引導我。
——貼到這裡為止——

3. Claude 會跟妳打招呼，妳說「準備好了」它就開始
4. 中間照畫面回答就好

【先準備】
- Mac 開機密碼（裝 Homebrew 那步用一次）
- Google 帳號（申請 2 個免費 API key + 登入 NotebookLM）

【卡關時】
卡 5 分鐘以上 → 截圖 Claude 對話最後 10 句傳給我，我直接看妳卡哪。

加油，妳沒問題的 💪
```

---

## 備援方案：如果 Claude 說「我無法存取網址」

少數情況 Claude Code IDE 可能沒有開放網址抓取權限。如果 Angel 試了第一段她貼的訊息後 Claude 回「無法 fetch」之類，請她改成這樣做：

```
備援方案 ——

1. 開瀏覽器到：
   https://github.com/falcon75423-ui/fal-skills-for-angel/blob/main/docs/嗨-Angel-請貼給Claude.md

2. 點頁面上方檔案內容右上角的「複製原始檔」按鈕
   （長得像兩個重疊的方塊，hover 顯示「Copy raw file」）

3. 切回 Claude Code IDE 對話框
4. 按 Cmd+V 貼上整份內容
5. 按 Enter 送出

這樣等於把整份指引塞給 Claude，它會接管。
```

---

## Lester 自己的 checklist

傳出前確認：

- [ ] Angel 的 Claude Code IDE 是最新版（plugin 系統 + MCP 都要支援）
- [ ] Angel 已經裝好 顧問團 skill（階段 5 會 patch 它，沒裝的話得先補裝）
- [ ] Angel 知道她的 Mac 開機密碼（裝 Homebrew 必須）
- [ ] Angel 有可用的 Google 帳號（申請 Exa / Tavily / NotebookLM 登入）
- [ ] Angel 大致知道 40-60 分鐘的時間預期（避免她做一半中斷後忘記怎麼接回去）

如果 Angel 上面任何一條缺，先補齊再傳安裝訊息。
