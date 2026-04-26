# 平台情蒐工法手冊

> 跨 Skill 共用的外部平台搜尋工法。每條工法都經過實戰驗證。
> 最後驗證：2026-04-08
> 適用場景：任何需要搜尋外部平台內容的 Skill 或一般對話

---

## 工具總覽

| 工具 | 強項 | 弱項 |
|------|------|------|
| **Exa** | 語意搜尋、`includeDomains` 精準限定、freshness 過濾 | X/Twitter 覆蓋差、`site:` 對 Reddit 無效 |
| **WebSearch** | 廣度大、即時性好、中文搜尋有效 | 結果雜訊多、無 includeDomains |
| **WebFetch** | 讀取特定 URL 全文 | 付費牆/認證頁面會失敗、底層會摘要非逐字 |
| **NotebookLM** | YouTube 逐字稿提取、語義分析、報告生成 | 只吃有自動字幕的 YouTube、批次送報告會塞車 |
| **Bash (curl)** | Reddit .json 免費取留言 | 需設 User-Agent、有 rate limit |

---

## YouTube

### 發現（找影片）

```
Exa(
  query="頻道名A OR 頻道名B new video [主題]",
  includeDomains=["youtube.com"],
  freshness="week",
  numResults=5
)
```

**已驗證**：能準確撈到特定頻道的最新影片，含 views、likes、發布日期。
**踩坑**：WebSearch 搜 YouTube 太雜，Exa + includeDomains 效果好很多。

### 深挖（看內容）

```
1. source_add(notebook_id, source_type="url", url=YouTube_URL, wait=true)
   → NotebookLM / Gemini 自動提取逐字稿，約 30 秒

2. notebook_query(notebook_id, query="用 300 字做 executive briefing：
   核心論點？3 個最驚訝的宣言？真正新穎 vs 老生常談？",
   source_ids=[該來源 ID])
   → 回傳結構化摘要 + 精確引文
```

**已驗證**：一小時影片的逐字稿約 70-80KB，notebook_query 能做語義分析。
**踩坑**：自動字幕專有名詞會出錯（「Claude Code」→「clot code」），引用時需校正。

---

## Reddit

### 發現（找帖子）

```
WebSearch("reddit r/[subreddit] best posts this week [主題] [日期]")
```

**已驗證**：WebSearch 對 Reddit 的覆蓋穩定。
**踩坑**：Exa 的 `site:reddit.com` 語法無效（2026-04-08 驗證），回傳 0 結果。**不要用 Exa 搜 Reddit**。

### 深挖（看留言）

```
curl -s -H "User-Agent: [名稱]/1.0" \
  "https://www.reddit.com/r/{sub}/comments/{id}/.json" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
post = data[0]['data']['children'][0]['data']
print(f'Score: {post[\"score\"]}')
print(f'Comments: {post[\"num_comments\"]}')
comments = data[1]['data']['children']
for i, c in enumerate(comments[:5]):
    if c['kind'] != 't1': continue
    cd = c['data']
    body = cd.get('body','')[:200]
    print(f'--- #{i+1} ({cd.get(\"score\",0)} ups) u/{cd.get(\"author\",\"?\")}')
    print(body)
"
```

**已驗證**：免費、無需 API key、能拿到 score + upvote_ratio + top comments。
**踩坑**：必須設 User-Agent header，否則 429。單次最多深挖 3-5 個帖子（rate limit）。

---

## Hacker News

### 發現（找討論）

```
Exa(
  query="site:news.ycombinator.com [主題] discussion",
  freshness="week",
  numResults=5
)
```

**已驗證**：Exa 的 `site:` 對 HN 有效（跟 Reddit 不同）。
**踩坑**：無。穩定。

### 深挖（看討論串）

```
WebFetch(url="https://news.ycombinator.com/item?id=[ID]",
         prompt="提取前 10 則最高分留言的核心觀點")
```

---

## X / Twitter

### 發現（找推文串）

```
# 主力：WebSearch
WebSearch("[人名A] OR [人名B] AI tweet thread [日期]")

# 補充：Exa（不限 domain）
Exa(
  query="[人名] latest tweet thread AI observation",
  freshness="week",
  numResults=5
)
```

**已驗證**：WebSearch 能找到關於特定人物推文的報導和討論。Exa 不限 domain 時能撈到 Threads 和轉載。
**踩坑**：Exa `includeDomains=["x.com", "twitter.com"]` 效果差（2026-04-08 驗證）——回傳 Threads 和文章，不是推文本身。**X 搜尋不要用 Exa includeDomains**。

---

## Podcast

### 發現（找新集）

```
Exa(
  query="[節目名A] podcast OR [節目名B] podcast new episode",
  freshness="week",
  numResults=5
)
```

**已驗證**：能撈到 YouTube 上的 podcast 影片版（含 views、likes）+ Apple Podcasts 連結。
**踩坑**：主題搜尋幾乎撈不到 podcast 集數——必須用節目名搜。

### 深挖（聽內容）

多數 podcast 同步上 YouTube → 轉入 YouTube 深挖流程（NotebookLM）。
純音頻無 YouTube 版 → 用 WebFetch 找 show notes / transcript 做評估。

---

## 中文來源

### 發現

```
# 特定網域
Exa(
  query="[作者名] AI OR [網域] AI 最新文章",
  freshness="week",
  numResults=5
)

# 廣度搜尋
WebSearch("AI 人工智慧 [主題] 台灣 [日期] 深度分析")
```

**已驗證**：Exa 能找到特定中文 blog（Wilson Huang 等），WebSearch 中文關鍵字能找到 iThome、TechOrange、天下等台灣媒體。
**踩坑**：英文搜尋永遠不會撈到中文內容。**中文來源必須用中文關鍵字獨立搜尋**。

---

## NotebookLM 操作工法

### 報告批次生成

- 🔴 **一次最多 3-4 份**，不要同時送超過 5 份——佇列塞車，部分報告永遠卡 `in_progress`
- 分批策略：每批 3-4 份，`studio_status` 確認全部 `completed` 後再送下一批
- 等待時間：每批 60-90 秒

### 驗證時清理

`studio_status` 時必掃：
- 殭屍報告（`in_progress` > 3 分鐘且同來源已有 completed）→ `studio_delete` 刪除
- 重複報告（同 source_id 多份 completed）→ 保留最新，刪舊
- 無標題殭屍（標題 = 筆記本名稱而非來源標題）→ 確認有正常報告後刪除

### 來源標題格式

```
文章：[YYYY-MM-DD] [類別] 文章標題
影片：[YYYY-MM-DD] [影片] 頻道名 — 影片標題
Reddit：[YYYY-MM-DD] [Reddit] r/subreddit — 帖子標題
```

---

## 工具選擇決策樹

```
要搜什麼？
├─ YouTube 影片 → Exa + includeDomains=youtube.com
├─ Reddit 帖子 → WebSearch（Exa 對 Reddit 無效）
├─ Hacker News → Exa + site:news.ycombinator.com
├─ X/Twitter 推文 → WebSearch 主力 + Exa 補充（不限 domain）
├─ Podcast 新集 → Exa + 節目名
├─ 中文內容 → Exa 搜特定網域 + WebSearch 中文關鍵字
├─ 一般文章/Blog → Exa + WebSearch 雙引擎
└─ 特定 URL 全文 → WebFetch（注意付費牆限制）

要深挖內容？
├─ YouTube/Podcast 影片 → NotebookLM source_add + notebook_query
├─ Reddit 留言 → curl .json endpoint
├─ HN 討論串 → WebFetch
└─ 付費牆文章 → 標記 🔒，讓使用者決定
```
