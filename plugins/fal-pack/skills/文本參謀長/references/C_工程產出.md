# C圈：工程產出

> 讀取時機：進入「付印」思考姿態時載入。

---

## 三引擎架構

### 引擎一：python-docx + docxtpl（新建/模板）

**適用場景**：從零新建、模板填充、簡單結構文件。

**python-docx 核心 API**：
```python
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

doc = Document()

# 段落 + 樣式
p = doc.add_paragraph('內容', style='Normal')
run = p.add_run('粗體片段')
run.bold = True

# CJK 字型雙設定（🔴 必經齒輪）
run.font.name = 'Times New Roman'  # Latin
run._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')  # CJK

# 標題
doc.add_heading('標題文字', level=1)

# 表格
table = doc.add_table(rows=3, cols=4, style='Table Grid')
table.rows[0].cells[0].text = '表頭'

# 圖片
doc.add_picture('image.png', width=Cm(15))

# 分節（混合頁面方向）
section = doc.add_section(WD_ORIENT.LANDSCAPE)
section.page_width = Cm(29.7)
section.page_height = Cm(21.0)
# 🔴 橫向時必須手動交換 width/height

# 頁首頁尾
header = doc.sections[0].header
header.paragraphs[0].text = '頁首文字'
doc.sections[0].different_first_page_header_footer = True
# 首頁不同頁首
first_header = doc.sections[0].first_page_header

# 頁邊距
section = doc.sections[0]
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(3.17)
section.right_margin = Cm(3.17)
```

**docxtpl 模板填充**：
```python
from docxtpl import DocxTemplate

doc = DocxTemplate('template.docx')
context = {
    'title': '報告標題',
    'author': '作者名',
    'sections': [
        {'heading': '第一節', 'content': '內容...'},
        {'heading': '第二節', 'content': '內容...'},
    ]
}
doc.render(context)
doc.save('output.docx')
```

模板中使用 Jinja2 語法：
- `{{ title }}` — 簡單替換
- `{% for s in sections %}...{% endfor %}` — 迴圈
- `{% if condition %}...{% endif %}` — 條件
- `{{ content | RichText }}` — 富文本（保留格式）

### 引擎二：OOXML 直接編輯（精確修改）

**適用場景**：修改既有文件的特定部分，不想碰到其他格式。

**三步驟**���
1. **解壓**：.docx 是 ZIP，解壓到暫存目錄
2. **編輯 XML**：直接操作 `word/document.xml`
3. **重打包**：驗證 → 壓回 ZIP

```python
import zipfile, shutil, os
from defusedxml.minidom import parseString

# 解壓
with zipfile.ZipFile('input.docx', 'r') as z:
    z.extractall('temp_dir')

# 讀取並編輯 document.xml
with open('temp_dir/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用 Edit 工具做字串替換（Anthropic 模式）
# 或使用 Document class 做程式化編輯（claude-office-skills 模式）

# 重打包
with zipfile.ZipFile('output.docx', 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk('temp_dir'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, 'temp_dir')
            z.write(file_path, arcname)
```

**Track Changes XML 模式**：
```xml
<!-- 插入文字 -->
<w:ins w:id="1" w:author="文本參謀長" w:date="2026-04-05T12:00:00Z">
  <w:r>
    <w:rPr><!-- 格式 --></w:rPr>
    <w:t>新增的文字</w:t>
  </w:r>
</w:ins>

<!-- 刪除文字 -->
<w:del w:id="2" w:author="文本參謀長" w:date="2026-04-05T12:00:00Z">
  <w:r>
    <w:rPr><!-- 格式 --></w:rPr>
    <w:delText>被刪除的文字</w:delText>
  </w:r>
</w:del>
```

🔴 **OOXML 編輯必須**：
- 每個 `<w:ins>` / `<w:del>` 必須有唯一 `w:id`
- `w:author` 統一設為 `"文本參���長"`
- `w:date` 使用 ISO 8601 UTC 格式
- 刪除的文字用 `<w:delText>` 不是 `<w:t>`
- 操作完後驗證：提取文字比對，確認沒有繞過 Track Changes 偷改

### 引擎三：win32com / Word COM（重型操作）

**適用場景**：TOC、Track Changes 接受/拒絕、PDF 輸出、拼字檢查、field 更新。

```python
import win32com.client

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

doc = word.Documents.Open(r'C:\path\to\file.docx')

# TOC 更新
doc.TablesOfContents(1).Update()

# 所有 field 更新（頁碼、交叉引用等）
doc.Fields.Update()

# 接受所有修訂
doc.Revisions.AcceptAll()

# PDF ��出
doc.ExportAsFixedFormat(
    OutputFileName=r'C:\path\to\output.pdf',
    ExportFormat=17,  # wdExportFormatPDF
    OptimizeFor=0,    # wdExportOptimizeForPrint
    CreateBookmarks=1 # wdExportCreateHeadingBookmarks
)

# 拼字檢查
doc.Content.LanguageID = 1028  # zh-TW
errors = doc.SpellingErrors
for error in errors:
    print(f"拼字問題: {error.Text}")

# 樣式管理
for style in doc.Styles:
    if style.InUse:
        print(f"{style.NameLocal}: {style.Font.Name}, {style.Font.Size}pt")

doc.Close(SaveChanges=False)
word.Quit()
```

🔴 **Word COM 使用規範**：
- 永遠在 `try/finally` 中確保 `word.Quit()` 被呼叫
- `word.Visible = False` 避免彈出視窗
- 操作前先 `doc.Save()` 備份
- PDF 輸出用 `ExportAsFixedFormat`，不用 `SaveAs`（後者品質較差）

---

## 樣式系統（Design System）

所有格式決定集中定義在一個 dict 中，腳本全檔引用同一來源。

```python
DESIGN_SYSTEM = {
    # 字型
    'font_latin': 'Times New Roman',
    'font_cjk': '微軟正黑體',
    'font_mono': 'Consolas',
    
    # 字級（pt）
    'size_h1': 18,
    'size_h2': 15,
    'size_h3': 13,
    'size_body': 11,
    'size_caption': 9,
    
    # 行距（倍數或 pt）
    'line_spacing_body': 1.5,     # 正文
    'line_spacing_heading': 1.2,  # 標題
    
    # 段落間距（pt）
    'space_after_h1': 12,
    'space_after_h2': 8,
    'space_after_body': 6,
    'space_before_h1': 24,
    'space_before_h2': 18,
    
    # 顏色（RGB）
    'color_primary': RGBColor(0x1A, 0x1A, 0x2E),    # 深藍黑
    'color_secondary': RGBColor(0x4A, 0x4A, 0x6A),   # 灰藍
    'color_accent': RGBColor(0x2E, 0x86, 0xC1),      # 藍
    'color_body': RGBColor(0x33, 0x33, 0x33),         # 深��
    'color_caption': RGBColor(0x66, 0x66, 0x66),      # 中灰
    
    # 頁面
    'page_width': Cm(21.0),       # A4
    'page_height': Cm(29.7),
    'margin_top': Cm(2.54),
    'margin_bottom': Cm(2.54),
    'margin_left': Cm(3.17),
    'margin_right': Cm(3.17),
    
    # 表格
    'table_header_bg': RGBColor(0xE8, 0xEA, 0xED),
    'table_border_color': RGBColor(0xCC, 0xCC, 0xCC),
    'table_border_width': Pt(0.5),
}
```

🔴 **Design System 規則**：
- 每個新建文件必須先定義 DESIGN_SYSTEM
- 所有格式引用必須從此 dict 取值，禁止 magic number
- 被委託時：委託方可在 Brief 中指定 Design System 覆蓋值
- 公版化時：Design System 連同模板一起結晶

---

## CJK 排版規則

### 字型設定

每個 run 都要同時設定 Latin 和 CJK 字型：
```python
def set_run_font(run, ds=DESIGN_SYSTEM):
    """設定 run 的中英雙字型（🔴 必經齒輪）"""
    run.font.name = ds['font_latin']
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), ds['font_cjk'])
```

### 中英混排間距

使用 pangu 自動處理：
```python
import pangu

text = pangu.spacing_text('中文content混排test')
# 結果: '中文 content 混排 test'
```

文件層級設定（OOXML）：
```xml
<w:autoSpaceDE w:val="true"/>  <!-- CJK 與英數字間自動空格 -->
<w:autoSpaceDN w:val="true"/>  <!-- CJK 與數字間自動空格 -->
```

### 避頭尾（Kinsoku）

Word 預設已啟用 CJK 避���尾規則。確認方式：
```xml
<w:kinsoku w:val="true"/>
```

行首禁止字元：`）、。，！？」』】〉》）；：`
行��禁止字元：`（「『【〈《（`

### 標點壓縮

```xml
<w:overflowPunct w:val="true"/>  <!-- 標點溢出 -->
<w:autoSpaceDE w:val="true"/>    <!-- 自動間距 -->
```

---

## 分節控制

同一份文件內切換頁面方向、不同頁首頁尾：

```python
from docx.enum.section import WD_ORIENT

# 新增橫向分節
new_section = doc.add_section(WD_ORIENT.LANDSCAPE)
new_section.page_width = Cm(29.7)   # 🔴 橫向要交換
new_section.page_height = Cm(21.0)

# 回到直向
back_section = doc.add_section(WD_ORIENT.PORTRAIT)
back_section.page_width = Cm(21.0)
back_section.page_height = Cm(29.7)

# 不同分節的頁首頁尾獨立
new_section.header.is_linked_to_previous = False
```

🔴 **分節陷阱**：
- `WD_ORIENT.LANDSCAPE` 只設方向屬性，**不會自動交換 width/height**，必須手動設
- `is_linked_to_previous = False` 必須在寫入頁首內容**之前**設定
- 頁碼重新起算需要操作 XML field code，python-docx 無直接 API

---

## 頁首頁尾進階

```python
# 不同首頁
section.different_first_page_header_footer = True
first_header = section.first_page_header
first_header.paragraphs[0].text = ''  # 封面無頁首

# 奇偶頁不同
doc.settings.element.set(qn('w:evenAndOddHeaders'), 'true')
even_header = section.even_page_header

# 頁首插入圖片（logo）
from docx.shared import Cm
header = section.header
paragraph = header.paragraphs[0]
run = paragraph.add_run()
run.add_picture('logo.png', height=Cm(1.2))
```

---

## TOC 生成

python-docx 無法直接生成 TOC，需要兩步：

**Step 1：插入 TOC field code（python-docx）**
```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

paragraph = doc.add_paragraph()
run = paragraph.add_run()
fldChar1 = OxmlElement('w:fldChar')
fldChar1.set(qn('w:fldCharType'), 'begin')
run._element.append(fldChar1)

instrText = OxmlElement('w:instrText')
instrText.set(qn('xml:space'), 'preserve')
instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
run2 = paragraph.add_run()
run2._element.append(instrText)

fldChar2 = OxmlElement('w:fldChar')
fldChar2.set(qn('w:fldCharType'), 'end')
run3 = paragraph.add_run()
run3._element.append(fldChar2)
```

**Step 2：用 Word COM 更新 field**
```python
doc = word.Documents.Open(path)
doc.TablesOfContents(1).Update()
doc.Save()
```

---

## 格式轉換

### Markdown → Word
```bash
pandoc -f markdown -t docx --reference-doc=template.docx -o output.docx input.md
```
`--reference-doc` 讓輸出繼承模板的樣式定義。

### PDF → Word
```python
from pdf2docx import Converter

cv = Converter('input.pdf')
cv.convert('output.docx')
cv.close()
```
⚠️ 僅適用文字型 PDF。掃描型需先 OCR（Tesseract）。

### Word → PDF
```python
# 最高品質：Word COM
doc.ExportAsFixedFormat(output_path, 17)

# 替代：docx2pdf（底層也是 Word COM）
from docx2pdf import convert
convert('input.docx', 'output.pdf')
```

### HTML → Word
```bash
pandoc -f html -t docx --reference-doc=template.docx -o output.docx input.html
```

---

## Metadata 管理

```python
from docx import Document
from datetime import datetime

doc = Document()
props = doc.core_properties
props.author = '作者名'
props.title = '文件標題'
props.subject = '主題'
props.keywords = '關鍵字1, ���鍵字2'
props.language = 'zh-TW'
props.created = datetime.now()
props.modified = datetime.now()
props.category = '報告'
```

🔴 **Metadata 是底線品質**：每份交付物必須設定 author、title、language、created。缺任何一項 = 驗證不通過。
