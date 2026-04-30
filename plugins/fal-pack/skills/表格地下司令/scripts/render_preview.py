"""Excel 視覺品檢管線：xlsx → PDF → PNG。

用法：
    python render_preview.py <xlsx_path> [output_dir]

依賴：
    - Excel（win32com）
    - PyMuPDF（fitz）
    - 必須用 Python 3.13：C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe

回傳：產出的 PNG 檔案路徑清單（JSON）
"""

import json
import os
import sys


def render_xlsx_to_png(xlsx_path, output_dir=None):
    """Excel COM → PDF → PyMuPDF → PNG。回傳 PNG 路徑清單。"""
    import win32com.client
    import fitz

    xlsx_path = os.path.abspath(xlsx_path)
    if output_dir is None:
        output_dir = os.path.dirname(xlsx_path)

    base_name = os.path.splitext(os.path.basename(xlsx_path))[0]
    pdf_path = os.path.join(output_dir, base_name + '_preview.pdf')

    # Step 1: xlsx → PDF via Excel COM
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    try:
        workbook = excel.Workbooks.Open(xlsx_path)
        workbook.ExportAsFixedFormat(0, pdf_path)  # 0 = xlTypePDF
        workbook.Close(False)
    finally:
        excel.Quit()

    # Step 2: PDF → PNG via PyMuPDF
    png_paths = []
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        mat = fitz.Matrix(2, 2)  # 2x zoom for readability
        pix = page.get_pixmap(matrix=mat)
        png_path = os.path.join(output_dir, f"{base_name}_preview_p{i}.png")
        pix.save(png_path)
        png_paths.append(png_path)
    doc.close()

    # 清理中間 PDF
    try:
        os.remove(pdf_path)
    except OSError:
        pass

    return png_paths


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python render_preview.py <xlsx_path> [output_dir]')
        sys.exit(1)

    xlsx_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    png_paths = render_xlsx_to_png(xlsx_path, output_dir)
    print(json.dumps(png_paths, ensure_ascii=False))
