---
name: "Q1 2026 業務分析報告"
description: "商業文件 - 季度業務數據分析與策略建議"

colors:
  primary: "#1A2B3F"
  secondary: "#4A5C72"
  accent: "#0F7AA8"
  body: "#2A2A2A"
  caption: "#6F6F6F"
  table_header_bg: "#E8EEF4"
  table_border: "#C5D0DD"
  background: "#FBFBFA"
  positive: "#2D7D32"
  warning: "#E65100"

typography:
  heading_1:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 18
    fontWeight: 700
    lineSpacing: 1.3
    spaceBefore: 24
    spaceAfter: 12

  heading_2:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 14
    fontWeight: 700
    lineSpacing: 1.4
    spaceBefore: 18
    spaceAfter: 6

  heading_3:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 12
    fontWeight: 700
    lineSpacing: 1.5
    spaceBefore: 12
    spaceAfter: 6

  body:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 11
    fontWeight: 400
    lineSpacing: 1.5
    spaceBefore: 0
    spaceAfter: 6

  body_emphasis:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 11
    fontWeight: 700
    lineSpacing: 1.5

  caption:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 9
    fontWeight: 400
    lineSpacing: 1.4

  metric_large:
    fontFamily: "Helvetica"
    fontFamilyCJK: "思源黑體"
    fontSize: 24
    fontWeight: 300
    lineSpacing: 1.0

spacing:
  unit: 6
  margin_top: "2.54cm"
  margin_bottom: "2.54cm"
  margin_left: "2.5cm"
  margin_right: "2.5cm"
  paragraph_indent: "0"
  list_indent: "0.74cm"
  quote_indent: "1cm"

cjk:
  pangu_spacing: true
  kinsoku: true
  overflow_punct: true
  auto_space_de: true
  auto_space_dn: true
  punct_width: "fullwidth"

numbering:
  heading_style: "1.1.1"
  list_marker: "•"
  toc_depth: 3
  figure_prefix: "圖"
  table_prefix: "表"

sections:
  page_size: "A4"
  orientation: "portrait"
  different_first_page: true
  even_odd_headers: false
  page_number_start: 2
  page_number_position: "footer_right"
  cover_page: true

components:
  body_paragraph:
    typography: "{typography.body}"
    indent: "{spacing.paragraph_indent}"
  heading_1_style:
    typography: "{typography.heading_1}"
    color: "{colors.primary}"
  heading_2_style:
    typography: "{typography.heading_2}"
    color: "{colors.primary}"
  heading_3_style:
    typography: "{typography.heading_3}"
    color: "{colors.secondary}"
  table_header:
    backgroundColor: "{colors.table_header_bg}"
    typography: "{typography.body_emphasis}"
  metric_callout:
    typography: "{typography.metric_large}"
    color: "{colors.accent}"
  link:
    typography: "{typography.body}"
    color: "{colors.accent}"
---

# Design System: Q1 2026 業務分析報告

## 1. Overview

**創意北極星：「會議室白板上的數據敘事」**

這是給高階主管 15 分鐘掃描的季度報告。讀者不是逐頁閱讀，是先看封面摘要、再翻關鍵數據、最後讀建議行動。設計要服務這個閱讀路徑——大數據要醒目、結論要短、視覺層次要立刻分得出輕重緩急。

**核心特徵**：
- 主色深藍黑表達穩重專業
- 強調色靛藍用於關鍵數據與行動項
- 大量數字採用 Light 字重 + 大字級的反差設計（24pt Light vs 11pt Regular）

**這份文件 NOT**：
- 不是學術論文的密集長文
- 不是行銷簡報的視覺豪華
- 不是公文的字面僵硬

## 2. Colors

主色靠近深海軍藍，傳達穩重與專業。強調色是飽和靛藍（用量 ≤ 5%），只用在關鍵數據、連結、行動按鈕。另增 positive/warning 兩色服務數據視覺化。

### 主色 Primary
- **深海軍** (#1A2B3F)：H1 H2 標題、頁碼、關鍵分隔線。

### 次色 Secondary
- **石板灰藍** (#4A5C72)：H3 副標題、表格表頭文字。

### 強調色 Accent
- **電光靛** (#0F7AA8)：關鍵數據（指標卡 metric_callout）、超連結。全文用量 ≤ 5%。

### 中性色 Neutral
- **碳灰** (#2A2A2A)：內文（避免純黑）
- **石灰** (#6F6F6F)：圖說、腳註
- **辦公白** (#FBFBFA)：背景

### 數據語意色
- **正向綠** (#2D7D32)：正成長指標
- **警示橘** (#E65100)：負成長 / 風險訊號

### 命名規則
**靛色稀有規則**：強調色用量上限 5%。每頁靛色出現 ≤ 4 處。

## 3. Typography

**內文字型 Body**：Helvetica（CJK：思源黑體）
**展示字型 Metric**：Helvetica Light 24pt

**個性**：純粹的無襯線現代感。Helvetica 的中性氣質讓數據自己說話，不被字型風格搶戲。

### 階層

- **Heading 1** (700 18pt, 行距 1.3 倍, 段前 24pt / 段後 12pt)：章節標題
- **Heading 2** (700 14pt, 行距 1.4 倍, 段前 18pt / 段後 6pt)：節
- **Heading 3** (700 12pt, 行距 1.5 倍)：小節
- **Body** (400 11pt, 行距 1.5 倍, 中文每行約 35 字)：內文
- **Body Emphasis** (700 11pt, 行距 1.5 倍)：粗體強調
- **Caption** (400 9pt, 行距 1.4 倍)：圖說、腳註
- **Metric Large** (300 24pt, 行距 1.0)：指標卡的大數字

### 中文特化規則

- 行距：1.5 倍（商業文件標準）
- 中英間距：pangu 自動處理
- 避頭尾：啟用
- 段落呼吸：段距 6pt，首行不縮排

### 命名規則
**Light 反差規則**：Metric 大數字用 Light 300 + Heading Bold 700，反差製造視覺對比。Light 字重不用於小於 18pt 的場景。

## 4. Sections

兩分節：封面（無頁碼）+ 內文（頁碼從 2 起算）。內文不分章首頁，連續排版以便快速翻閱。

### 紙張規格
- 大小：A4
- 方向：直向
- 邊距：上下 2.54cm / 左右 2.5cm
- 排版區寬度：16cm

### 分節策略
- 首頁不同：Yes（封面無頁碼）
- 奇偶頁不同：No
- 頁碼起算：第 2 頁
- 頁碼位置：頁尾右側
- 頁首：左側書名「Q1 2026 業務分析」/ 右側日期

## 5. Components

### 內文段落
- 字型：引用 `{typography.body}`
- 段距：6pt（不縮排，現代商業文件習慣）
- 引用塊縮排 1cm

### 標題 Headings
- 編號：1.1.1（自動三級編號）
- H1 H2 用 `{colors.primary}`，H3 用 `{colors.secondary}`
- H1 不分頁（連續排版便於快速翻閱）

### 指標卡 Metric Callout
- 大數字用 `{typography.metric_large}` (Light 24pt)
- 單位用 `{typography.body}` (11pt)
- 數字顏色 `{colors.accent}`，單位 `{colors.body}`
- 上下留 12pt 空間

### 表格 Tables
- 表頭背景 `{colors.table_header_bg}`，字重 700
- 數字欄右對齊，正向用 `{colors.positive}`，負向用 `{colors.warning}`
- 邊框 0.5pt，顏色 `{colors.table_border}`
- 隔行底色 #F7F8FA（疏密區分）

### 圖表 Figures
- 圖片寬度 100% 排版區
- 圖說 `{typography.caption}`，置中於圖片下方
- 圖框：無

## 6. Do's and Don'ts

### Do
- **Do** 大數字用 Light 300 + 大字級（≥18pt），製造視覺對比
- **Do** 使用 Bold 標題與 Regular 內文的清楚字重對比
- **Do** 表格數字右對齊，文字左對齊
- **Do** 強調色用於連結與關鍵數據，總用量 ≤ 5%

### Don't
- **Don't** 同一頁出現超過 4 處強調色 accent
- **Don't** 用紅綠對比表示正負（色弱讀者看不到 → 改用綠/橘）
- **Don't** 使用斜體強調（中文斜體不美觀，改用粗體）
- **Don't** 在標題加底線（90 年代簡報風格）
- **Don't** 內文中放純黑文字（換 #2A2A2A 較柔和）
