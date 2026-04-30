# B圈：品質系統

> 讀取時機：進入「編輯」思考姿態時載入。

---

## 四重校對閘門

> 態度是零容忍，機制是四重閘門。如果四層都過了還漏字，那是閘門要修的 bug，不是「可接受的誤差」。

### 第一層：fal 語意校對（CJK 最強項）

fal 自身的語言能力在 CJK 校對上比任何規則引擎都強。聚焦：

- **同音異字**：「在」vs「再」、「的」vs「得」vs「地」、「做」vs「作」
- **語意層面錯字**：規則引擎抓不到但人能看出來的
- **贅字/漏字**：多了一個「的」、少了一個「不」
- **句子完整性**：主詞-動詞-受詞是否齊全
- **標點正確性**：中文全形、英文半形、混用檢查

**執行方式**：逐段朗讀式掃描。不是掃一眼，是讀出聲來（心中）。

### 第二層：LanguageTool（歐語文法）

```python
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')  # 或 'zh-TW', 'ja'
matches = tool.check(text)
for match in matches:
    print(f"位置 {match.offset}: {match.message}")
    print(f"  建議: {match.replacements[:3]}")
    print(f"  規則: {match.ruleId}")
```

**多語言策略**：
- 偵測文件主要語言 → 載入對應規則集
- 混合語言文件 → 逐段偵測語言 → 分別校對
- 中文：LanguageTool 有基礎文法規則，但不做拼寫檢查（第一層已覆蓋）
- 英文：文法 + 拼寫 + 風格（被動語態、冗餘表達等）

### 第三層：Word COM 校對引擎

```python
# 利用 Word 內建校對
doc = word.Documents.Open(path)

# 設定語言
for paragraph in doc.Paragraphs:
    paragraph.Range.LanguageID = 1028  # zh-TW

# 取得拼字錯誤
spelling_errors = doc.SpellingErrors
for error in spelling_errors:
    print(f"拼字: {error.Text} (位置: {error.Start})")

# 取得文法錯誤
grammar_errors = doc.GrammaticalErrors
for error in grammar_errors:
    print(f"文法: {error.Text}")
```

**語言包依賴**：取決於系統已安裝的語言包。Windows + Office 繁中版預設支援中文和英文。

### 第四層：pangu 中英間距（Bonus）

```python
import pangu

# 自動在中英文之間加空格
corrected = pangu.spacing_text('中文content混排test')
# → '中文 content 混排 test'
```

**執行時機**：校對最後一步，對全文跑一次 pangu 修正間距。

### 校對流程

```
輸入文件
  ▼
第一層：fal 語意校對
  ├─ 逐段掃描
  ├─ 標記所有疑點
  └─ 產出校對筆記
  ▼
第二層：LanguageTool
  ├─ 偵測語言
  ├─ 跑文法 + 拼寫規則
  └─ 合併結果到校對筆記
  ▼
第三層：Word COM
  ├─ 開啟文件
  ��─ 跑 SpellingErrors + GrammaticalErrors
  └─ 合併結果
  ▼
第四層：pangu
  ├─ 中英間距修正
  └─ 標記修改處
  ▼
產出校對報告 / 直接修正（視使用者選擇）
```

---

## 術語一致性引擎

> 「Client」和「Customer」不能在同一份文件裡混用。

### 流程

1. **術語提取**：掃描全文，提取所有專有名詞、技術術語、人名、組織名
2. **變體偵測**：找出同一概念的不同寫法
   - 大小寫變體：`API` vs `api` vs `Api`
   - 同義詞變體：`Client` vs `Customer` vs `用戶` vs `客戶`
   - 縮寫變體：`Artificial Intelligence` vs `AI` vs `A.I.`
3. **統一建議**：對每組變體提出統一方案
4. **全文替換**：使用者確認後執行

### 術語表

長期協作的文件類型可以建立術語表：
```yaml
# templates/terminology/[project_name].yaml
terms:
  - preferred: "使用者"
    variants: ["用戶", "用家", "使用人"]
    context: "指產品的終端使用者"
  - preferred: "API"
    variants: ["api", "Api", "A.P.I."]
    context: "應用程式介面"
```

---

## 修訂追蹤（Track Changes）

### 寫入模式（審稿指令）

表弟在「審稿」模式下，所有修改以 Track Changes 呈現：

**用 OOXML 引擎**（精確控制）：
- 插入：`<w:ins>` 包裹新增的 `<w:r>`
- 刪除：`<w:del>` 包裹，`<w:t>` 改為 `<w:delText>`
- 格式修改：`<w:rPrChange>` 記錄格式變更前的狀態
- 每個修訂必須有唯一 `w:id`、`w:author="文本參謀長"`、`w:date`

**用 Word COM**（簡單情境）：
```python
doc.TrackRevisions = True
# 之後的所有修改自動記錄為修訂
range = doc.Range(start, end)
range.Text = "新文字"  # 自動產生刪除+插入修訂
doc.TrackRevisions = False
```

### 接受/拒絕模式

```python
# 接受所有
doc.Revisions.AcceptAll()

# 選擇性接受
for rev in doc.Revisions:
    if rev.Author == "文本參謀長":
        rev.Accept()
```

---

## 文件比對（Document Comparison）

兩版文件 → 自動產出包含 Track Changes 的 redline 差異檔。

```python
word = win32com.client.Dispatch('Word.Application')
word.Visible = False

try:
    # 開啟原始版
    original = word.Documents.Open(r'C:\path\to\v1.docx')
    
    # 比對
    word.CompareDocuments(
        OriginalDocument=original,
        RevisedDocument=word.Documents.Open(r'C:\path\to\v2.docx'),
        Destination=2,  # wdCompareDestinationNew（產出新文件）
        Granularity=1,  # wdGranularityWordLevel
        CompareFormatting=True,
        CompareCaseChanges=True,
        CompareWhitespace=True,
    )
    
    # 儲存比對結果
    word.ActiveDocument.SaveAs(r'C:\path\to\comparison.docx')
finally:
    word.Quit()
```

---

## 無障礙驗證

### 驗證項目

| 項目 | 標準 | 檢查方式 |
|------|------|---------|
| 圖片 alt text | 每張圖片必須有描述性 alt text | 掃描所有 `<wp:docPr>` 的 `descr` 屬性 |
| 標題層級 | 不跳級（H1→H2→H3，不可 H1→H3） | 提取所有 heading 層級，檢查序列 |
| 表格標頭 | 第一行標記為 header row | 檢查 `<w:tblHeader/>` |
| 語言標籤 | 不同語言的段落/run 要標記 | 檢查 `<w:lang>` 設定 |
| 色彩對比 | 文字/背景對比度 ≥ 4.5:1 | 計算 WCAG 2.0 對比度 |
| 閱讀順序 | XML 順序 = 視覺閱讀順序 | 檢查文件流 |

### 自動修復

- 缺 alt text → 提示使用者補充
- 標題跳級 → 自動修正（降級或升級）
- 缺語言標籤 → 根據內容自動偵測並設定

---

## 註解系統（Comments）

```python
# python-docx 1.2.0+ 支援 comments
from docx import Document
from docx.comments import Comment

doc = Document('input.docx')
paragraph = doc.paragraphs[0]

# 新增註解
comment = Comment(
    text='這裡需要更具體的數據支撐',
    author='文本參謀長',
)
paragraph.add_comment(comment, start=0, end=len(paragraph.text))
```

**OOXML 層級**（python-docx 不支援時）：
需同時操作 4 個 XML 檔案：
1. `comments.xml` — 註解文字
2. `commentsExtended.xml` — 父子關係（回覆）
3. `commentsIds.xml` — 持久 ID
4. `commentsExtensible.xml` — UTC 日期

在 `document.xml` 中標記範圍：
```xml
<w:commentRangeStart w:id="1"/>
<w:r><w:t>被註解的文字</w:t></w:r>
<w:commentRangeEnd w:id="1"/>
<w:r><w:rPr/><w:commentReference w:id="1"/></w:r>
```
