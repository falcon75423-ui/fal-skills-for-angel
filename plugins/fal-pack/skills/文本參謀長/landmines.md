# 已知地雷集

> 🔴 每次執行前強制載入。這是表弟的免疫系統——每踩一次雷就自動免疫。
> 格式：❌ 地雷 → ✅ 正確做法

---

## python-docx

❌ CJK 字型只設 `font.name`，中文字用了錯誤字型
✅ 同時設 `font.name`（Latin）+ `rFonts.set(qn('w:eastAsia'), '微軟正黑體')`

❌ 直接修改 Style 物件的屬性（`style.font.size = Pt(14)`）
✅ 永遠 copy() 後新建，或操作 run 層級而非 style 層級

❌ 設 `WD_ORIENT.LANDSCAPE` 但沒交換 page_width 和 page_height
✅ 方向 + 尺寸一起設：width=29.7cm, height=21.0cm

❌ 新增分節後直接寫頁首內容（繼承了前一節的頁首）
✅ 先設 `is_linked_to_previous = False`，再寫入內容

❌ 用 python-docx 開啟含 VBA/SmartArt 的複雜文件再存檔（roundtrip 損壞）
✅ 先跑 assess_risk.py，UNSAFE → 切 Word COM

❌ 合併儲存格後只設左上角邊框（其他 cell 邊框被清空）
✅ 對合併範圍的每個 cell 逐一設定邊框

---

## OOXML

❌ Track Changes 的 `<w:ins>` / `<w:del>` 缺少 w:id / w:author / w:date
✅ 三者缺一不可，w:id 全文件唯一

❌ 刪除的文字用 `<w:t>` 而非 `<w:delText>`
✅ 被 `<w:del>` 包裹的文字必須用 `<w:delText>`

❌ `<w:t>` 中有前後空格但沒設 `xml:space="preserve"`
✅ 只要有空格就加 `xml:space="preserve"`

❌ 編輯 XML fragment 時缺少 namespace 宣告
✅ 所有用到的 namespace 都要在 fragment 中宣告

---

## Word COM

❌ 操作中途出錯，word.Quit() 沒被呼叫，Word process 殘留
✅ 永遠用 try/finally 包裹，finally 中 word.Quit()

❌ PDF 用 SaveAs 匯出（品質較差）
✅ 用 ExportAsFixedFormat（最高品質 + 書籤）

❌ 路徑用正斜線（Word COM 不認）
✅ 用反斜線或 raw string：`r'C:\path\to\file.docx'`

---

## 格式轉換

❌ Pandoc MD→DOCX 不帶 `--reference-doc`（輸出用預設醜樣式）
✅ 永遠帶 `--reference-doc=template.docx`

❌ 對掃描型 PDF 直接跑 pdf2docx（輸出空白或亂碼）
✅ 先 OCR（Tesseract），再轉換

---

*每次遇到新地雷，立即追加到此表。格式保持 `❌ → ✅` 一對。*
