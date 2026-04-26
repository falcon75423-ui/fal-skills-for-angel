# 法眼 — 已知地雷 💣

> 踩過的雷，不踩第二次。每次踩新雷 → 追記 → 下次自動免疫。

---

## 🔴 鎖死齒輪（絕對不可違反）

### 單源單報告
- NotebookLM 報告生成：一個來源 → 一份報告，例外零容忍
- 多個來源混合生成報告 = 內容混雜 = 品質崩塌
- 即使兩篇文章主題相關，也必須各自獨立生成報告
- 🔴 **跨輪次保護**（2026-04-11 事故升級）：「單源單報告」不只管本輪，也管**跨輪次**。生成報告前必須先跑 `notebook_get` + `studio_status` 檢查是否已有舊報告。若命中 → 跳過不再生成，避免製造「第 2 份/第 3 份」重複
- 歷史事故：2026-04-11 一次出刊上架 10 篇精選，其中 Gemma 4 Lambert 和 Raschka Coding Agent 兩篇之前已有舊報告。幸好第一次 `studio_status` 掃描時發現，臨時改為跳過+後續清理。根因是**source_add 前沒查既有 sources**——已升級為記憶層的啟動載入閘門

### 來源標題格式
- 新增來源時標題必須包含日期和類別：`[YYYY-MM-DD] [類別] 文章標題`
- 不加日期 = 日後無法追溯時間軸
- 不加類別 = 日後無法按類別篩選

### 分類篩選不可扁平化
- 精選階段必須先按類別分組，每類各選最多 3 篇
- 不可做扁平 Top N 排名——會導致某些類別的優質內容被整個吃掉
- 類別可動態調整，但「分類再選」的機制不可省略

### 記憶層鎖死齒輪（2026-04-11 新增）
- 🔴 **啟動時必須載入 `memory/picks-index.md`**——不載入就開工 = 失憶主編 = 保證騙版位
- 🔴 **粗篩第 0 條四題問答不可省**——任一題答不出即燒。Q1（多知道什麼）/ Q2（連接語怎麼寫）/ Q3（擠掉誰）
- 🔴 **通過 Q2 的候選，連接語必須寫進點評的第一或第二句**——這是閘門的強制動作，不是建議
- 🔴 **出刊末段必須有「🗑️ 記憶層審計」區塊**——每次被燒掉的候選都要顯性列出攔截理由 + 觸發的舊精選 + 使用者覆蓋指令。記憶層不能是黑盒子
- 詳細規範見 `references/記憶層規範.md`
- 歷史背景：2026-04-11 之前法眼無記憶，導致 W15 筆記本累積 4 組重複（Gemma 4 × 3、Enterprise Playbook × 2、Claude Dispatch × 2、Raschka Coding Agent × 2）。這不是單次失誤，是結構性失憶——所以升級為閘門而非記憶

---

## 報告生成地雷

### 批次報告生成會塞車
- 🔴 **一次最多送 3-4 份報告**，不要同時送 10 份——NotebookLM 佇列會塞車，部分報告永遠卡在 `in_progress`
- 分批策略：每批 3-4 份，等 `studio_status` 確認該批全部 `completed` 後再送下一批
- 等待時間：每批約 60-90 秒

### 驗證時自動清理殭屍與重複報告
- 🔴 **`studio_status` 驗證時必做清理**：掃描所有報告，發現以下情況**立即用 `studio_delete` 刪除**，不需要問使用者：
  - **殭屍報告**：`in_progress` 超過 3 分鐘且同來源已有 `completed` 報告 → 刪除殭屍
  - **重複報告**：同一個 `source_id` 有多份 `completed` 報告 → 保留最新的，刪除舊的
  - **無標題殭屍**：標題為筆記本名稱（如「法眼精選 — 2026-WXX」）而非來源標題 → 大概率是塞車產物，確認有正常報告後刪除
- 清理後向使用者報告刪了幾份、為什麼

### 單筆記本 report 配額（NotebookLM 隱性限制 ≈ 10 份）
- 🔴 **單筆記本 reports 上限約 10 份**——超過後 `studio_create(report)` 持續回「Could not create report」，等 90s/180s 都不解。這不是短期 rate limit，是配額硬牆
- **mind_map 不計入 report quota**（W17 驗證：10 reports + 1 mind map 同時存在無問題）
- **預檢策略（建檔前必跑）**：盤點 source 數量。**> 10 source 時必須拆筆記本**：
  - 主筆記本「法眼精選 — YYYY-WXX」只放最高優先級（必讀 🔥 + 值得看 ✓），最多 10 個 source
  - 次要的（法眼特選 / 商業實戰 / 也值得一讀補充）丟「法眼精選 — YYYY-WXX 補檔」筆記本
  - 拆分時同主題不可分離（例如 Zvi 三部曲必須同筆記本，因為心智圖要跨三篇整合）
- **判定方式**：`source_describe` 能正常生成 summary = source 健全；4 次以上 `studio_create(report)` 重試仍失敗（含等 90s/180s）= 配額硬牆，不是 source 問題
- 實測案例：12 source 的筆記本，前 10 個 report 全成功，第 11、12 個連 4 次重試皆失敗。`source_describe` 顯示 summary 完整 → 源頭健康 → 判定為 NotebookLM 端隱性 quota。當下選擇接受 10/12 結果，未生成 report 的 source 仍可被搜尋

---

## 工具地雷

### NotebookLM 認證

**驗證方法（啟動時用）**：
- 呼叫 `notebook_list`（max_results=1）做輕量探測
- 能回傳 = 認證有效，不需要任何動作
- 🔴 **不要主動跑 `nlm login`**——這會開瀏覽器、產生錯誤訊息、打斷流程。只有認證確認失敗時才請 使用者自己跑

**修復方法（認證失敗時用）**：
- 提醒 使用者在終端跑 `nlm login`，不要靜默失敗，也不要自己代跑
- 🔴 **版本要求：0.5.22+**（≤0.5.5 在 Chrome 已開啟時無法正確抓 cookie，會靜默失敗）

**認證過期是結構性必然**：
- Google session cookies 有壽命（約 2-3 週），不存在「一次登入永久有效」
- 過期時症狀：MCP 工具回傳 auth error，`nlm login --check` 顯示 expired
- 修復：使用者跑 `nlm login`（0.5.22 版可在 Chrome 開啟狀態下直接抓既有 session 的 cookie）

**歷史**：
- 2026-03-24：nlm 版本衝突修復，舊版 `notebooklm-cli`（v0.1.12）已移除
- 2026-04-13：v0.5.5→v0.5.22 升級。根因：舊版在 Chrome 已開啟時 CDP 連不上，cookie 靜默抓取失敗。新版可直接連上既有 Chrome 實例

### 搜尋工具限制
- Tavily 免費額度已用完（2026-03-26），不再作為必要工具。Exa + WebSearch 雙引擎完全替代
- Exa API key 已設定（MCP Connector），語意搜尋主力
- WebSearch 使用 Claude token，廣度搜尋主力
- WebFetch 對需要認證的頁面會失敗（Facebook、付費牆）
- 🔴 **WebFetch 不適合精確全文提取**：WebFetch 底層會摘要，即使 prompt 要求逐字回傳，實際取回率約 80%。需要 100% 吃透外部 repo（吸收精髓、安裝前評估、深審）時，必須先 `git clone` 到本地再用 Read 逐檔讀。WebFetch 只適合快速偵察，不適合深審級閱讀（2026-04-05 踩雷確認）

---

## 內容地雷

### 付費牆
- 很多高品質來源（SemiAnalysis、Stratechery）有付費牆
- 策略：能讀到的部分做評估，標記「🔒 付費內容」讓 使用者自己決定是否訂閱

### Facebook / Threads 內容
- 封閉花園，無法自動擷取。使用者丟連結可嘗試 WebFetch 但不保證成功
- 不要把 Facebook/Threads 列為自動化來源
- 🔴 **Threads API 深度偵察結論（2026-03-26）**：官方 API 有 Keyword Search 功能，但搜尋「別人的」公開貼文需要 App Review + 商家驗證（2-4 週），rate limit 500次/7天。Apify 爬蟲方案有合規風險（Meta vs Bright Data 判例）。MCP Server 存在（`baguskto/threads-mcp`）但底層仍受同樣 API 限制。**決定暫緩**，聽風功能先以 X 為主力

### YouTube 影片評估
- 🔴 **法眼無法直接讀取影片內容**——Exa / WebSearch 只回傳標題和摘要，不夠做五維評估
- **解法**：透過 NotebookLM 導入 YouTube URL → Gemini 自動提取逐字稿 → notebook_query 做語義摘要 → 法眼根據摘要評估
- NotebookLM 處理 YouTube 時只提取逐字稿（自動字幕），不是 multimodal 看影片（2026-04-07 測試確認）
- 自動字幕專有名詞常出錯（如「Claude Code」→「clot code」），引用時需校正
- 完整流程 → 見 `references/深挖工法.md`

### Reddit 留言深挖
- Reddit 帖子 URL 後加 `.json` 可免費取得帖子 + 留言 JSON（無需 API key）
- 🔴 **必須設 User-Agent header**，否則 Reddit 直接擋（429）
- Rate limit 存在：單次巡稿最多深挖 3-5 個帖子，不要批量
- 高讚留言往往比帖子本身更有洞察——這是 Reddit 最有價值的部分
- 完整流程 → 見 `references/深挖工法.md`

---

## 品味地雷

### 大佬光環
- 不因為作者是大佬就自動高評分。大佬也會交敷衍的東西
- 判斷標準永遠是文章本身，不是作者履歷

### 同溫層陷阱
- 連續多天推同一類型文章時，主動檢查是否掉入同溫層
- 「意外值」維度是對策

### 翻譯品質
- 中文摘要需確保不失真。技術概念翻譯要附原文術語
- 不確定的翻譯寧可保留原文
