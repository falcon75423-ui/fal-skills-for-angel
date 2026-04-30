# 已知地雷

> 🔴 每次執行前強制載入。這是表哥的免疫系統——每踩一次雷就自動免疫。

---

## 1. 相容性地雷（工程不對 → 檔案壞 / Google Sheets 不相容）

> 「會不會壞」「能不能跨平台」「會不會靜默損壞」這類問題。
> 4 個子段是表哥從 2025-2026 累積的工程踩雷史。

### openpyxl 地雷

❌ 直接修改 `cell.font.bold = True`
✅ 建立新 Font 物件：`cell.font = Font(bold=True, name=old.name, size=old.size, ...)`

❌ 複製格式用 `target.font = source.font`（共享參照，改一個影響兩個）
✅ 用 `from copy import copy; target.font = copy(source.font)`

❌ 邊框只設需要的邊（`Border(left=thin)`），其他邊變 None
✅ 四邊都明確設定：`Border(left=thin, right=thin, top=thin, bottom=thin)`

❌ 先寫邊框再寫資料（後續操作可能覆蓋邊框）
✅ 所有資料和格式寫完後，最後做一輪獨立的邊框 pass

❌ 合併儲存格只對左上角設邊框（其他 cell 的邊框消失）
✅ 合併區域四邊界每個 cell 都要設邊框

❌ 用 `insert_rows()` 插入行後期待格式跟上（不會複製格式）
✅ 用 placeholder 替換模式，或手動從模板行 `copy_cell_style()`

❌ `data_only=True` 開啟後存檔（永久摧毀所有公式）
✅ 讀公式用 `data_only=False`，讀快取值用 `data_only=True` 但**絕不存檔**

❌ 對 .xlsm 檔案用 openpyxl 開啟+存檔（VBA 被剝離）
✅ 用 win32com COM 自動化操作 .xlsm

❌ 含圖片/形狀的檔案用 openpyxl roundtrip（圖片靜默消失）
✅ 用 win32com，或只讀不寫

---

### 格式地雷

❌ 年份用數字格式（`2026` 顯示為 `2,026`）
✅ 年份用文字格式（`@`）或直接寫成字串

❌ 使用 Theme Color（Google Sheets 會變黑色）
✅ 一律使用 RGB hex 色碼

❌ 使用 Named Style（Google Sheets 完全忽略）
✅ 使用 inline/direct style

❌ 使用 Gradient Fill（Google Sheets 只取第一色）
✅ 使用 PatternFill(fill_type='solid')

❌ 使用 Calibri 字型（Google Sheets 沒有，欄寬會炸）
✅ 英文用 Arial，繁中用 Noto Sans TC

❌ CJK 內容的欄寬用英文字元數估算（中文字寬是英文 2 倍）
✅ 用 `unicodedata.east_asian_width()` 計算，CJK 算 2 倍寬

❌ 依賴 Excel 的「自動調整欄寬」（openpyxl 產出的檔案不會自動調整）
✅ 必須明確用程式計算並設定每一欄的 width

---

### 公式地雷

❌ 可算的值寫死數字（`cell.value = 1234`）
✅ 寫公式（`cell.value = '=SUM(B2:B9)'`）

❌ 使用 FILTER/SORT/UNIQUE/SEQUENCE（Google Sheets 語法不同）
✅ 用 INDEX-MATCH、手動篩選、輔助欄

❌ 使用 INDIRECT/OFFSET（揮發性函數，效能殺手）
✅ 用 INDEX-MATCH 替代

❌ 寫完公式不驗算
✅ Python 端獨立計算一次比對結果

---

### 環境地雷

❌ 用預設的 `python`（3.14，缺少必要套件）
✅ 用 `<Python 3.13 路徑>`

❌ Excel COM 操作時不關閉 DisplayAlerts（彈出對話框卡住）
✅ `excel.DisplayAlerts = False`

❌ Excel COM 操作後不 Quit（留下殭屍程序）
✅ 用 try/finally 確保 `excel.Quit()` 執行

❌ 用相對路徑開啟 Excel COM（路徑解析錯誤）
✅ 一律用 `os.path.abspath()` 轉絕對路徑

---

## 2. 腳本地雷（2026-03-31 升級事故）

> 表哥動生成腳本（.py）時誤殺資料 / 設計常數重複定義 / 結構偏移。

❌ 修改生成腳本時用舊版本作為底稿重寫（資料列表、累積更新、結構擴展全部遺失）
✅ 先讀磁碟上的現行版本，只做外科手術式修改。「改字型」= 只改字型定義，不碰其他

❌ 生成腳本有本地設計系統常數（字型/顏色/填充），跟 design_system.py 重複定義
✅ 所有格式定義只在 design_system.py 一處。生成腳本 import 使用，不重複定義

❌ 資料結構用裸 tuple + magic index（如 `g[7]`），插入新欄位時所有後續索引偏移
✅ 用 `GameRecord` namedtuple，欄位存取用 `g.confidence` 不用 `g[7]`

❌ 只改了 design_system.py 的值，沒確認生成腳本是否 import 了它（以為改就生效）
✅ 改完 design_system.py 後，grep 所有 import 它的腳本確認引用關係

---

## 3. 設計品味地雷（看起來不對 → 讀者體驗差 / 違反設計原則）

> F-018 借鑑 impeccable v3.0.5（pbakaus/impeccable）E20「絕對禁令清單」精神（match-and-refuse rewrite）。
> 「相容性地雷」管「會不會壞」、本段管「好不好看」。看到就拒絕重寫，不等客戶抱怨。
> 8 條皆有 `scripts/verify_design.py` 自動檢查（驗證管線 Layer 1.5）。

❌ 紅綠對比表示正向/負向（色弱讀者完全看不到差異，全球約 8% 男性色弱）
✅ 用綠（#2D7D32）/ 橘（#E65100）對比，或綠/紅但加形狀差異（▲/▼）

❌ 標題列跟資料列字級相同（hierarchy 糊掉）
✅ 標題列字級 ≥ 資料列 × 1.25 + 字重加粗（多維 hierarchy）

❌ 一份 .xlsx 用超過 3 套字型（含 Latin + CJK 各算一套）
✅ Latin（Arial）+ CJK（Noto Sans TC）+ 等寬數字（Roboto Mono）= 3 套，到此為止

❌ 列高用 7 / 11 / 13 / 17 pt 等非 6pt 整數倍（視覺節奏破碎）
✅ 列高用 6pt 整數倍（12/18/24/30/36），跟 F-017 文本參謀長對齊基礎單位
   例外：Excel 預設 15pt（=2.5×6 非整倍）為合法例外，verify_design.py 降為 WARNING 不 hard fail

❌ 合併儲存格貼邊不留 padding（視覺擠壓）
✅ 合併區四邊界留 ≥ 2pt padding，搭配 `border_merged_range`

❌ 隔行底色灰度差 > 8%（如 #FFFFFF 跟 #E0E0E0）= 底色搶 hierarchy
✅ 灰度差 ≤ 4%（如 #FFFFFF 跟 #F8F8F8 = 約 3% 差距）

❌ 同一欄數字混用左右對齊（視覺安定感失敗）
✅ 數字一律右對齊 + 千分位 / 百分比一律右對齊 + 1 位小數 / 文字一律左對齊

❌ #000 純黑文字 + #FFF 純白背景（傷視疲勞 + 紙頁缺溫度）
✅ 文字用 #2A2A2A 之類淡墨，背景用 #FAFAF8 之類暖白
