"""既有 Excel 檔案風險偵測。

用法：
    python assess_risk.py <filepath>

回傳 JSON：
    {"level": "SAFE|RISKY|UNSAFE", "risks": {"SAFE": [...], "RISKY": [...], "UNSAFE": [...]}}

UNSAFE = 不能用 openpyxl roundtrip，必須用 win32com
RISKY = 可以用 openpyxl 但要小心，建議先備份
SAFE = 可以安心用 openpyxl
"""

import json
import sys
import zipfile
import os


def assess_risk(filepath):
    risks = {'SAFE': [], 'RISKY': [], 'UNSAFE': []}

    if not os.path.exists(filepath):
        return 'UNSAFE', {'UNSAFE': [f'檔案不存在: {filepath}'], 'RISKY': [], 'SAFE': []}

    # 副檔名
    if filepath.lower().endswith('.xlsm'):
        risks['UNSAFE'].append('致命：.xlsm 檔案的 VBA 會被 openpyxl 剝離')

    # ZIP 層級
    try:
        with zipfile.ZipFile(filepath) as z:
            names = z.namelist()

            if 'xl/vbaProject.bin' in names:
                risks['UNSAFE'].append('致命：含 VBA macro')
            if any('activeX' in n for n in names):
                risks['UNSAFE'].append('致命：含 ActiveX 控件')
            if 'xl/connections.xml' in names:
                risks['UNSAFE'].append('致命：含外部資料連線')
            if any('oleObject' in n.lower() for n in names):
                risks['UNSAFE'].append('致命：含 OLE 物件')

            for name in names:
                if name.startswith('xl/worksheets/sheet'):
                    content = z.read(name).decode('utf-8', errors='ignore')
                    if 'sparklineGroup' in content:
                        risks['UNSAFE'].append('致命：含 Sparklines')
                        break

            # 圖片檢查
            if any(n.startswith('xl/media/') for n in names):
                risks['UNSAFE'].append('致命：含圖片/媒體（roundtrip 會丟失）')

            # 圖表檢查
            if any(n.startswith('xl/charts/') for n in names):
                risks['RISKY'].append('注意：含圖表（格式可能重設）')

    except zipfile.BadZipFile:
        risks['UNSAFE'].append('致命：檔案不是有效的 ZIP/XLSX')
        return 'UNSAFE', risks

    # openpyxl 層級
    try:
        from openpyxl import load_workbook
        wb = load_workbook(filepath, read_only=True, data_only=False)

        defined_names = list(wb.defined_names.definedName) if wb.defined_names else []
        if defined_names:
            risks['RISKY'].append(f'注意：含 {len(defined_names)} 個命名範圍（可能損壞）')

        for ws in wb.worksheets:
            if ws.conditional_formatting:
                cf_count = sum(1 for _ in ws.conditional_formatting)
                risks['RISKY'].append(f'注意：{ws.title} 含 {cf_count} 條件格式規則（複雜規則可能損壞）')

            if ws.data_validations and ws.data_validations.dataValidation:
                dv_count = len(ws.data_validations.dataValidation)
                risks['RISKY'].append(f'注意：{ws.title} 含 {dv_count} 資料驗證規則（可能被丟棄）')

        wb.close()
    except Exception as e:
        risks['RISKY'].append(f'注意：openpyxl 讀取時發生錯誤: {str(e)}')

    # 判定
    if risks['UNSAFE']:
        level = 'UNSAFE'
    elif risks['RISKY']:
        level = 'RISKY'
    else:
        level = 'SAFE'
        risks['SAFE'].append('檔案結構簡單，可安全使用 openpyxl')

    return level, risks


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python assess_risk.py <filepath>')
        sys.exit(1)

    level, risks = assess_risk(sys.argv[1])
    print(json.dumps({'level': level, 'risks': risks}, ensure_ascii=False, indent=2))
