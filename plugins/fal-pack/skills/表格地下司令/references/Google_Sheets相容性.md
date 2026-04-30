# Google Sheets 相容性

> 讀取時機：Google Sheets 安全模式啟用時（預設開啟）。

---

## 安全格式規範

Google Sheets 安全模式下，所有產出必須遵守：

### 字型

| 語系 | 安全字型 | 禁用 |
|------|---------|------|
| 英文 | Arial, Roboto, Courier New | Calibri（Google Sheets 沒有，會 fallback 導致欄寬炸裂）|
| 繁體中文 | Noto Sans TC | 新細明體、標楷體（非 Google Fonts）|
| 簡體中文 | Noto Sans SC | 宋體、黑體 |
| 日文 | Noto Sans JP | MS Gothic |

### 顏色

- 🔴 **一律使用 RGB hex**：`Font(color="FF0000")`, `PatternFill(fgColor="E2EFDA")`
- 🔴 **禁用 Theme Color**：Google Sheets 不支援，會變黑色或預設色
- 🔴 **禁用 Gradient Fill**：Google Sheets 只取第一色渲染為 solid

### 邊框

安全子集：`thin`, `medium`, `thick`, `dashed`, `dotted`
不安全：`double`（部分版本渲染不一致）、`hair`（太細可能不顯示）

### 條件格式

安全子集：`CellIsRule`, `FormulaRule`, `ColorScale`（簡單形式）
不安全：`IconSet`（渲染完全不同）、`DataBar`（部分支援）、複雜多規則

### 公式

禁用清單（Google Sheets 不支援或語法不同）：
- `FILTER`, `SORT`, `UNIQUE`, `SEQUENCE`（動態陣列——語法不同）
- `LET`（部分支援但行為差異）
- `LAMBDA`（部分支援）
- `CUBE*` 系列（完全不支援）
- 條件式數值格式碼（`[Red][>100]#,##0`）

安全替代：
- XLOOKUP → INDEX-MATCH
- FILTER → 手動篩選或輔助欄
- SEQUENCE → 手動序號

### 欄寬

Excel 用「字元數」，Google Sheets 用像素。轉換會有 1-2 字元的偏差。
**防禦**：設定欄寬時寧可寬 10% 也不要窄。CJK 內容額外加 2 字元 buffer。

### 列印設定

Google Sheets **完全忽略** .xlsx 中的列印設定（紙張大小、邊距、頁首頁尾、分頁符號、重複標題列）。
無法防禦，但需在交付時告知使用者：「列印設定需在 Google Sheets 中重新設定。」

---

## 地雷嚴重度清單

| 功能 | 嚴重度 | Google Sheets 行為 |
|------|--------|-------------------|
| Theme Color | 致命 | 變黑色或預設色 |
| VBA Macro | 致命 | 完全剝離 |
| Sparklines | 致命 | 完全消失 |
| ActiveX / Form 控件 | 致命 | 完全消失 |
| OLE 物件 | 致命 | 完全消失 |
| Power Query | 致命 | 完全消失 |
| Gradient Fill | 高 | 只取第一色 |
| 合併儲存格邊框 | 高 | 內部邊框常遺失 |
| 字型 fallback | 高 | 替換為 Google 字型，欄寬變 |
| 欄寬單位 | 高 | 偏差 1-2 字元 |
| 條件格式 DataBar | 中 | 樣式不同 |
| 條件格式 IconSet | 中 | 渲染不同 |
| 圖表進階設定 | 中 | 3D 效果、副軸可能丟失 |
| Named Style | 中 | 完全忽略，只讀 inline style |
| 動態陣列公式 | 高 | 語法不同，結果錯誤 |
| 數值格式碼 | 低 | 大部分支援 |
| 資料驗證 | 低 | 基本下拉 OK，公式型可能壞 |
| 凍結窗格 | 無 | 正常 |
| Auto-filter | 無 | 正常 |
| 超連結 | 無 | 正常 |
| 圖片 | 無 | 正常 |
| 註解 | 無 | 正常 |

---

## zip 層級檢測

openpyxl 看不到的東西（因為它不支援），必須直接檢查 .xlsx 的 ZIP 結構：

```python
import zipfile

def zip_level_check(filepath):
    """檢查 openpyxl API 看不到的 Google Sheets 不相容功能。"""
    warnings = []
    with zipfile.ZipFile(filepath) as z:
        names = z.namelist()

        if 'xl/vbaProject.bin' in names:
            warnings.append("致命：VBA macro 會被 Google Sheets 剝離")

        if any('activeX' in n for n in names):
            warnings.append("致命：ActiveX 控件會消失")

        if 'xl/connections.xml' in names:
            warnings.append("致命：外部資料連線會消失")

        if any('oleObject' in n.lower() for n in names):
            warnings.append("致命：OLE 物件會消失")

        if any('diagrams/' in n for n in names):
            warnings.append("高：SmartArt 會被柵格化或消失")

        for name in names:
            if name.startswith('xl/worksheets/sheet'):
                content = z.read(name).decode('utf-8', errors='ignore')
                if 'sparklineGroup' in content:
                    warnings.append("致命：Sparklines 會消失")
                    break

    return warnings
```

---

## 檔案限制

| 限制 | 上限 |
|------|------|
| 檔案大小 | 100 MB |
| 儲存格數 | 10,000,000 |
| 欄數 | 18,278 (ZZZ) |
| 工作表數 | 200 |

超過任何限制 = 上傳失敗。在產出時檢查。
