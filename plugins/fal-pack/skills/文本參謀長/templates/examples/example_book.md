---
name: "明清江南商業變遷"
description: "學術書籍 - 探討明清時期江南地區商業活動的歷史變遷"

colors:
  primary: "#2C2520"
  secondary: "#5C4D40"
  accent: "#8B4513"
  body: "#2E2826"
  caption: "#6B635A"
  table_header_bg: "#F5EFE6"
  table_border: "#D4C4A8"
  background: "#FAF6EC"

typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontFamilyCJK: "思源宋體"
    fontSize: 32
    fontWeight: 600
    lineSpacing: 1.2
    spaceBefore: 60
    spaceAfter: 24

  heading_1:
    fontFamily: "Cormorant Garamond"
    fontFamilyCJK: "思源宋體"
    fontSize: 20
    fontWeight: 700
    lineSpacing: 1.3
    spaceBefore: 36
    spaceAfter: 18

  heading_2:
    fontFamily: "Cormorant Garamond"
    fontFamilyCJK: "思源宋體"
    fontSize: 15
    fontWeight: 700
    lineSpacing: 1.4
    spaceBefore: 24
    spaceAfter: 12

  body:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 11
    fontWeight: 400
    lineSpacing: 1.75
    spaceBefore: 0
    spaceAfter: 0

  body_emphasis:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 11
    fontWeight: 700
    lineSpacing: 1.75

  caption:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 9
    fontWeight: 400
    lineSpacing: 1.4

  quote:
    fontFamily: "Cormorant Garamond"
    fontFamilyCJK: "思源宋體"
    fontSize: 11
    fontWeight: 400
    lineSpacing: 1.6

spacing:
  unit: 6
  margin_top: "3.5cm"
  margin_bottom: "3cm"
  margin_left: "3.5cm"
  margin_right: "3cm"
  paragraph_indent: "0.74cm"
  list_indent: "0.74cm"
  quote_indent: "1.5cm"

cjk:
  pangu_spacing: true
  kinsoku: true
  overflow_punct: true
  auto_space_de: true
  auto_space_dn: true
  punct_width: "fullwidth"

numbering:
  heading_style: "壹貳參"
  list_marker: "•"
  toc_depth: 3
  figure_prefix: "圖"
  table_prefix: "表"

sections:
  page_size: "B5"
  orientation: "portrait"
  different_first_page: true
  even_odd_headers: true
  page_number_start: 1
  page_number_position: "footer_center"
  cover_page: true

components:
  body_paragraph:
    typography: "{typography.body}"
    indent: "{spacing.paragraph_indent}"
  heading_1_style:
    typography: "{typography.heading_1}"
    color: "{colors.primary}"
  table_header:
    backgroundColor: "{colors.table_header_bg}"
    typography: "{typography.body_emphasis}"
  quote_block:
    typography: "{typography.quote}"
    color: "{colors.caption}"
    indent: "{spacing.quote_indent}"
---

# Design System: 明清江南商業變遷

## 1. Overview

**創意北極星：「藏書樓裡的學者書桌」**

這本書是學術研究的成熟結晶——傳遞的是經過十年考據的歷史敘事，氣質沉靜、紙頁有重量。讀者是研究生與專業學者，他們會在書桌前帶著筆記本緩慢閱讀，在邊緣寫批註。

**核心特徵**：
- 飽和暖白紙背景，主色用古書墨色
- 大量留白，每頁文字密度約 60%
- 圖表與正文同一暖色系，不靠彩色製造焦點

**這份文件 NOT**：
- 不是商業簡報的鮮豔色塊
- 不是 SaaS 紫色漸層
- 不是大字疏排的入門讀物

## 2. Colors

整本書只用三個主要色系，主色是古書墨色，次色是舊紙泛黃的暖灰，強調色克制使用於章節分隔符。

### 主色 Primary
- **沉默墨色** (#2C2520)：所有 H1 標題、章節分隔符、頁碼。表達文件的權威感與重量。

### 次色 Secondary
- **舊紙暖灰** (#5C4D40)：副標題、表格表頭文字。

### 強調色 Accent
- **典籍褐** (#8B4513)：章節分隔符的單色裝飾、引文起頭。全書總用量 ≤ 3%。

### 中性色 Neutral
- **淡墨** (#2E2826)：內文（避免純黑 #000，保留紙頁溫度）
- **霧灰** (#6B635A)：圖說、腳註
- **典籍白** (#FAF6EC)：背景紙色，模仿舊書頁

### 命名規則
**One Voice 規則**：強調色用量 ≤ 3%。它的稀有性就是它的力量。

## 3. Typography

**展示字型 Display**：Cormorant Garamond（fallback：Georgia, serif）
**內文字型 Body**：Times New Roman（CJK：思源宋體）

**個性**：兩套都是襯線體，氣質統一。Cormorant 更有古典展示感，Times 更內斂適合長文閱讀。

### 階層

- **Display** (600 32pt, 行距 1.2 倍)：封面標題
- **Heading 1** (700 20pt, 行距 1.3 倍, 段前 36pt / 段後 18pt)：章
- **Heading 2** (700 15pt, 行距 1.4 倍, 段前 24pt / 段後 12pt)：節
- **Body** (400 11pt, 行距 1.75 倍, 中文每行約 32 字)：正文
- **Body Emphasis** (700 11pt)：粗體強調（用 `{typography.body_emphasis}`）
- **Caption** (400 9pt, 行距 1.4 倍)：圖說、腳註

### 中文特化規則

- 行距：1.75 倍（書籍長文場景）
- 中英間距：pangu 自動處理
- 避頭尾：啟用
- 段落呼吸：首行縮排 2 字（0.74cm），段距 0（書籍傳統）

### 命名規則
**字級不雜規則**：全書最多 4 個字級（不算 caption）。

## 4. Sections

全書四分節：封面（無頁碼/無頁首）、目錄（羅馬數字頁碼）、正文（阿拉伯數字頁碼從 1 起算）、附錄（接續正文頁碼）。雙面印書奇偶頁不同頁首：偶數頁顯示書名，奇數頁顯示章名。

### 紙張規格
- 大小：B5（17.6 × 25cm，書籍標準）
- 方向：直向
- 邊距：上 3.5cm / 下 3cm / 左 3.5cm / 右 3cm
- 裝訂邊：左側多留 0.5cm

### 分節策略
- 首頁不同：Yes（封面、各章首頁）
- 奇偶頁不同：Yes
- 頁碼起算：第 5 頁（正文第一頁）
- 頁碼位置：頁尾置中

## 5. Components

### 內文段落 Body Paragraph
- 字型：引用 `{typography.body}`
- 段落策略：首行縮排 0.74cm（約 2 字）
- 首段不縮排（章節首段保留視覺起點感）

### 標題 Headings
- 編號：「第一章」「第一節」（壹貳參格式）
- H1 用 `{colors.primary}`，H2 用 `{colors.secondary}`
- 每章 H1 從新頁開始

### 引用塊 Quotes
- 縮排 1.5cm
- 字型 Cormorant Garamond + 思源宋體
- 顏色 `{colors.caption}`（淡化）

### 表格 Tables
- 表頭背景 `{colors.table_header_bg}`，字重 700
- 邊框 0.5pt，顏色 `{colors.table_border}`
- 跨頁時表頭重複

## 6. Do's and Don'ts

### Do
- **Do** 保持暖白背景與墨色文字的高對比，但避免純黑純白
- **Do** 中文行距 1.75 倍，給予閱讀呼吸
- **Do** 章首頁強制空 1/3 頁面再開內文
- **Do** 圖說字級小於正文（9pt vs 11pt）

### Don't
- **Don't** 用霓虹色或飽和度 > 70% 的彩色（與古書氣質衝突）
- **Don't** 章節間隔處放裝飾線條（克制裝飾，保留紙面留白）
- **Don't** 在內文中使用粗體強調超過每頁 3 處（會破壞閱讀節奏）
- **Don't** 使用兩套以上的 CJK 字型混排
