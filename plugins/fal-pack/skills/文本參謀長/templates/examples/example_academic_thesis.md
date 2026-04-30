---
name: "博士論文 - 比較研究方法論"
description: "學術論文 - 三萬字博士論文，依 APA 7th 規範"

colors:
  primary: "#1A1A1A"
  secondary: "#3D3D3D"
  accent: "#5A4FCF"
  body: "#1F1F1F"
  caption: "#5C5C5C"
  table_header_bg: "#F0F0F0"
  table_border: "#B8B8B8"
  background: "#FCFCFA"

typography:
  display:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 18
    fontWeight: 700
    lineSpacing: 1.5
    spaceBefore: 0
    spaceAfter: 24

  heading_1:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 16
    fontWeight: 700
    lineSpacing: 1.5
    spaceBefore: 24
    spaceAfter: 12

  heading_2:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 14
    fontWeight: 700
    lineSpacing: 1.5
    spaceBefore: 18
    spaceAfter: 6

  heading_3:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 12
    fontWeight: 700
    lineSpacing: 1.5
    spaceBefore: 12
    spaceAfter: 6

  body:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 12
    fontWeight: 400
    lineSpacing: 1.75
    spaceBefore: 0
    spaceAfter: 0

  body_emphasis:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 12
    fontWeight: 700
    lineSpacing: 1.75

  caption:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 10
    fontWeight: 400
    lineSpacing: 1.5

  quote:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 11
    fontWeight: 400
    lineSpacing: 1.5

  footnote:
    fontFamily: "Times New Roman"
    fontFamilyCJK: "思源宋體"
    fontSize: 10
    fontWeight: 400
    lineSpacing: 1.3

spacing:
  unit: 6
  margin_top: "2.54cm"
  margin_bottom: "2.54cm"
  margin_left: "3.5cm"
  margin_right: "2.54cm"
  paragraph_indent: "0.84cm"
  list_indent: "0.84cm"
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
  heading_2_style:
    typography: "{typography.heading_2}"
    color: "{colors.primary}"
  heading_3_style:
    typography: "{typography.heading_3}"
    color: "{colors.secondary}"
  table_header:
    backgroundColor: "{colors.table_header_bg}"
    typography: "{typography.body_emphasis}"
  quote_block:
    typography: "{typography.quote}"
    color: "{colors.body}"
    indent: "{spacing.quote_indent}"
  footnote_text:
    typography: "{typography.footnote}"
    color: "{colors.body}"
  caption_text:
    typography: "{typography.caption}"
    color: "{colors.caption}"
---

# Design System: 博士論文 - 比較研究方法論

## 1. Overview

**創意北極星：「圖書館特藏室的研究稿」**

學位論文是給三位口試委員 + 未來研究者讀的。讀者會精讀、追腳註、查文獻清單。設計必須服從學術慣例（APA 7th + 校方規範），不靠視覺巧思取勝——靠的是嚴謹的結構與不出錯的格式細節。

**核心特徵**：
- 全文襯線體，學術正統
- 行距 1.75 倍（適合密集邏輯文字 + 給口試委員批註空間）
- 左側裝訂邊加大到 3.5cm（裝訂後仍可閱讀）
- 首行縮排 0.84cm（中文 2 字寬）

**這份文件 NOT**：
- 不是商業簡報的視覺豪華
- 不是雜誌編輯的字型遊戲
- 不是部落格的疏排輕快

## 2. Colors

學術論文幾乎不用色——黑墨字、白紙背景，是傳統。本設計加入極克制的紫色當引文/連結強調。

### 主色 Primary
- **論文墨黑** (#1A1A1A)：所有標題（避免純黑 #000，保留紙頁溫度）

### 次色 Secondary
- **次標灰** (#3D3D3D)：H3 副標題

### 強調色 Accent
- **學術紫** (#5A4FCF)：超連結、DOI、URL。全文用量極少（< 1%）。

### 中性色 Neutral
- **內文墨** (#1F1F1F)：正文
- **腳註灰** (#5C5C5C)：腳註、圖說
- **論文白** (#FCFCFA)：背景紙

### 命名規則
**色彩克制規則**：除了超連結，全文不出現任何彩色。圖表也用灰階 + 紋理區分（色弱讀者友善 + 黑白印刷不失真）。

## 3. Typography

**內文字型 Body**：Times New Roman（CJK：思源宋體）

**個性**：學術正統的襯線體，氣質統一。Times New Roman 是 APA 規範的標準選擇，思源宋體與其搭配在 CJK 場景中最和諧。

### 階層

- **Display** (700 18pt, 行距 1.5 倍)：論文標題（封面）
- **Heading 1** (700 16pt, 行距 1.5 倍, 段前 24pt / 段後 12pt)：章
- **Heading 2** (700 14pt, 行距 1.5 倍, 段前 18pt / 段後 6pt)：節
- **Heading 3** (700 12pt, 行距 1.5 倍, 段前 12pt / 段後 6pt)：小節
- **Body** (400 12pt, 行距 1.75 倍, 中文每行約 30 字)：正文
- **Body Emphasis** (700 12pt)：內文粗體強調（用 `{typography.body_emphasis}`）
- **Quote** (400 11pt, 行距 1.5 倍)：四行以上的引文（縮排成獨立段）
- **Footnote** (400 10pt, 行距 1.3 倍)：腳註
- **Caption** (400 10pt, 行距 1.5 倍)：圖說、表說

### 中文特化規則

- 行距：1.75 倍（學術論文標準）
- 中英間距：pangu 自動處理
- 避頭尾：啟用
- 段落呼吸：首行縮排 0.84cm（約中文 2 字），段距 0
- 數學公式中英留空：保留

### 命名規則
**APA 7th 守則**：所有引用格式遵循 APA 7th。中文文獻照「APA 7th 中文化版」處理。

## 4. Sections

四分節：封面、目次（羅馬數字頁碼）、正文（阿拉伯數字頁碼從 1 起算）、參考文獻 + 附錄。

### 紙張規格
- 大小：A4
- 方向：直向
- 邊距：上 2.54cm / 下 2.54cm / 左 3.5cm（裝訂邊）/ 右 2.54cm

### 分節策略
- 首頁不同：Yes
- 奇偶頁不同：No（單面印交付）
- 頁碼起算：正文第 1 頁
- 頁碼位置：頁尾置中

### 頁首頁尾
- 頁首：無（保持簡潔）
- 頁尾：頁碼置中

## 5. Components

### 內文段落
- 首行縮排 0.84cm（中文 2 字）
- 段距 0
- 章節首段不縮排
- 內文絕不使用斜體（中文斜體不美），用粗體強調

### 標題 Headings
- 編號：1.1.1（西式三級）
- 中文章節別名：「第一章」「第一節」可選用作 H1 H2
- H1 從新頁開始
- H1 H2 用 `{colors.primary}`，H3 用 `{colors.secondary}`

### 引用塊 Quotes
- 四行以下：直接放在段落中，加引號 `「」`
- 四行以上：獨立段、縮排 1cm、字級降為 11pt（典型學術慣例）
- 不加左側裝飾線

### 腳註 Footnotes
- 腳註位於頁面底部
- 字級 10pt，行距 1.3 倍
- 腳註編號連續整章編號（章內 1, 2, 3...）

### 表格 Tables
- 表頭背景 `{colors.table_header_bg}`，字重 700
- 邊框：APA 7th 慣例只有上中下三條橫線（線色 `{colors.table_border}`）
- 表說明位於表格上方（APA 7th）

### 圖表 Figures
- 圖說位於圖片下方
- 編號：圖 1、圖 2...（連續整章）
- APA 7th 慣例：圖的標題粗體，描述非粗體

### 參考文獻 References
- 懸掛縮排 0.84cm
- 字級 12pt，行距 1.5 倍
- 條目間段距 6pt

## 6. Do's and Don'ts

### Do
- **Do** 嚴格遵守 APA 7th 引用格式
- **Do** 中文行距 1.75 倍，給口試委員批註空間
- **Do** 圖表用灰階 + 紋理（色弱友善 + 黑白印刷不失真）
- **Do** 首行縮排 0.84cm，段距 0
- **Do** 表格用三線格式（上中下三條橫線）

### Don't
- **Don't** 內文使用斜體強調（中文斜體不美觀，改用粗體）
- **Don't** 用任何彩色（除了超連結 accent，全文 < 1%）
- **Don't** 在標題加裝飾或圖示（學術論文純文字）
- **Don't** 表格用全格邊框（不符 APA 7th）
- **Don't** 同段落內混用太多字型字級（保持一致性）
- **Don't** 章首頁出現頁首裝飾
