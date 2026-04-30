"""
load_design.py — DESIGN.md → DESIGN_SYSTEM dict 自動同步
F-017 / 文本參謀長

職責：
1. 解析 DESIGN.md 開頭的 YAML frontmatter
2. 對映成 Python dict，含 docx 型別轉換（RGBColor / Cm / Pt）
3. 漂移驗證閘門：YAML 跟 markdown body 描述明顯不一致時警告
4. 提供 load_design(path) -> dict API 給其他腳本用

設計限制（subagent 驗收 W2 文件化）：
- token reference 僅支援單層解析（components 引用 primitives）
- typography role 內部含的 token reference 不會自動 resolve
- 循環引用會被偵測並 raise ValueError

使用：
    from load_design import load_design
    DESIGN_SYSTEM = load_design('path/to/DESIGN.md')
    # DESIGN_SYSTEM['typography']['body']['fontSize']  -> Pt(11)
    # DESIGN_SYSTEM['colors']['primary']               -> RGBColor(0x1A, 0x1A, 0x2E)

CLI 模式：
    python load_design.py path/to/DESIGN.md --validate
    python load_design.py path/to/DESIGN.md --print

來源：F-017 由火神鍛造工頭 + 文本參謀長跨客戶協作鍛造（2026-04-30）。
"""

from __future__ import annotations
import re
import sys
import json
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write("ERROR: PyYAML 未安裝。執行: pip install pyyaml\n")
    sys.exit(1)

# python-docx 為 optional dependency（純解析/驗證模式不需要）
try:
    from docx.shared import Pt, Cm, RGBColor
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    # Fallback 型別：tuple 形式，方便測試與序列化
    def Pt(x):  # type: ignore
        return ('Pt', x)

    def Cm(x):  # type: ignore
        return ('Cm', x)

    def RGBColor(r, g, b):  # type: ignore
        return ('RGBColor', r, g, b)


# ============================================================
#                    YAML frontmatter 解析
# ============================================================

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)


def extract_frontmatter(text: str) -> tuple[dict, str]:
    """從 markdown 開頭抽出 YAML frontmatter，回傳 (frontmatter_dict, body)"""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("DESIGN.md 開頭未找到 YAML frontmatter（--- 包夾的區塊）")
    yaml_text = match.group(1)
    body = text[match.end():]
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML frontmatter 解析失敗：{e}")
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter 必須是 mapping（dict），不是 list 或 scalar")
    return data, body


# ============================================================
#                    型別轉換
# ============================================================

def parse_pt(value: Any) -> Any:
    """解析 Pt 值。支援 int/float (假設 pt 單位) 或字串 '12pt' / '12'"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return Pt(float(value))
    if isinstance(value, str):
        v = value.strip().lower().replace('pt', '').strip()
        try:
            return Pt(float(v))
        except ValueError:
            raise ValueError(f"無法解析 Pt: {value!r}")
    raise ValueError(f"無法解析 Pt: {value!r}")


def parse_cm(value: Any) -> Any:
    """解析 Cm 值。支援字串 '2.54cm' / '2.54' / '1inch' / '1\"' 或數字（假設 cm）"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return Cm(float(value))
    if isinstance(value, str):
        v = value.strip().lower()
        if v.endswith('cm'):
            return Cm(float(v[:-2].strip()))
        if v.endswith('mm'):
            return Cm(float(v[:-2].strip()) / 10.0)
        if v.endswith('inch') or v.endswith('"') or v.endswith('in'):
            v_clean = v.rstrip('"').replace('inch', '').replace('in', '').strip()
            return Cm(float(v_clean) * 2.54)
        # 純數字字串假設 cm
        try:
            return Cm(float(v))
        except ValueError:
            raise ValueError(f"無法解析 Cm: {value!r}")
    raise ValueError(f"無法解析 Cm: {value!r}")


HEX_COLOR_RE = re.compile(r'^#?([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$')


def parse_color(value: Any) -> Any:
    """解析顏色。支援 '#1A1A2E' / '#1a1a2e' / '#ABC' / '1A1A2E'"""
    if not isinstance(value, str):
        raise ValueError(f"顏色必須是字串: {value!r}")
    v = value.strip().lstrip('#')
    if len(v) == 6 and HEX_COLOR_RE.match(value.strip()):
        r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
        return RGBColor(r, g, b)
    if len(v) == 3 and HEX_COLOR_RE.match(value.strip()):
        r = int(v[0] * 2, 16)
        g = int(v[1] * 2, 16)
        b = int(v[2] * 2, 16)
        return RGBColor(r, g, b)
    raise ValueError(f"無法解析顏色: {value!r}（需要 #RRGGBB 或 #RGB 格式）")


# ============================================================
#                    區塊轉換邏輯
# ============================================================

def transform_typography_role(role: dict) -> dict:
    """轉換 typography 單一 role（display / heading_1 / body / ...）"""
    if not isinstance(role, dict):
        raise ValueError(f"typography role 必須是 dict: {role!r}")
    out: dict = {}
    for key, val in role.items():
        if key in ('fontFamily', 'fontFamilyCJK'):
            out[key] = str(val) if val is not None else None
        elif key == 'fontSize':
            out[key] = parse_pt(val)
        elif key == 'fontWeight':
            out[key] = int(val) if val is not None else None
        elif key == 'lineSpacing':
            out[key] = float(val) if val is not None else None
        elif key in ('spaceBefore', 'spaceAfter'):
            out[key] = parse_pt(val)
        elif key == 'letterSpacing':
            out[key] = parse_pt(val)
        else:
            out[key] = val  # 未知欄位保留原值
    return out


def transform_spacing(spacing: dict) -> dict:
    if not isinstance(spacing, dict):
        return {}
    out: dict = {}
    for key, val in spacing.items():
        if key == 'unit':
            out[key] = parse_pt(val)
        elif key.startswith('margin_') or key in ('list_indent', 'quote_indent'):
            out[key] = parse_cm(val)
        elif key == 'paragraph_indent':
            # paragraph_indent 可能是 '0' / '0.74cm' / '2em'（em 留原值給上層處理）
            if isinstance(val, str) and val.strip().endswith('em'):
                out[key] = val
            elif val == '0' or val == 0:
                out[key] = Cm(0)
            else:
                try:
                    out[key] = parse_cm(val)
                except ValueError:
                    print(
                        f"WARN: paragraph_indent 無法解析 {val!r}，fallback 為 Cm(0)",
                        file=sys.stderr,
                    )
                    out[key] = Cm(0)
        else:
            out[key] = val
    return out


def transform_colors(colors: dict) -> dict:
    if not isinstance(colors, dict):
        return {}
    return {key: parse_color(val) for key, val in colors.items()}


TOKEN_REF_RE = re.compile(r'^\{([\w\.]+)\}$')


def resolve_token_ref(ref: str, design: dict, _visited: set | None = None) -> Any:
    """解析 token reference 如 '{typography.body}' 或 '{colors.primary}'。

    僅支援單層解析（components 引用 primitives）。
    多級嵌套（typography role 內部再含 token ref）不自動展開——這是設計選擇。
    循環引用會被偵測並 raise ValueError。
    """
    if _visited is None:
        _visited = set()
    match = TOKEN_REF_RE.match(ref)
    if not match:
        return ref
    if ref in _visited:
        raise ValueError(f"Token reference '{ref}' 循環引用偵測——拒絕解析")
    _visited.add(ref)
    path = match.group(1).split('.')
    v: Any = design
    for p in path:
        if isinstance(v, dict) and p in v:
            v = v[p]
        else:
            raise ValueError(f"Token reference '{ref}' 找不到（在 path '{p}' 處中斷）")
    return v


def transform_components(components: dict, resolved: dict) -> dict:
    """解析 components 內的 token refs（{path.to.token}）"""
    if not isinstance(components, dict):
        return {}
    out: dict = {}
    for name, comp in components.items():
        if not isinstance(comp, dict):
            out[name] = comp
            continue
        out_comp: dict = {}
        for prop, val in comp.items():
            if isinstance(val, str) and TOKEN_REF_RE.match(val):
                out_comp[prop] = resolve_token_ref(val, resolved)
            else:
                out_comp[prop] = val
        out[name] = out_comp
    return out


# ============================================================
#                    對外 API
# ============================================================

def load_design(path: str | Path) -> dict[str, Any]:
    """
    讀取 DESIGN.md 並回傳 DESIGN_SYSTEM dict。

    Args:
        path: DESIGN.md 檔案路徑

    Returns:
        dict 含以下 keys（缺的 key 為 {}）:
            name, description, colors, typography, spacing, cjk,
            numbering, sections, components

    Raises:
        FileNotFoundError: 檔案不存在
        ValueError: YAML frontmatter 解析錯誤 / token reference 找不到
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"DESIGN.md not found: {p}")

    text = p.read_text(encoding='utf-8')
    frontmatter, _body = extract_frontmatter(text)

    # 順序重要：先解析 primitives（colors / typography / spacing），
    # 再解析 components（components 會引用 primitives）
    design: dict[str, Any] = {
        'name': frontmatter.get('name', ''),
        'description': frontmatter.get('description', ''),
        'colors': transform_colors(frontmatter.get('colors') or {}),
        'typography': {
            role: transform_typography_role(spec)
            for role, spec in (frontmatter.get('typography') or {}).items()
        },
        'spacing': transform_spacing(frontmatter.get('spacing') or {}),
        'cjk': frontmatter.get('cjk') or {},
        'numbering': frontmatter.get('numbering') or {},
        'sections': frontmatter.get('sections') or {},
    }

    # components 在最後，因為要引用 primitives
    if frontmatter.get('components'):
        design['components'] = transform_components(
            frontmatter['components'],
            design,
        )
    else:
        design['components'] = {}

    return design


# ============================================================
#                    漂移驗證閘門
# ============================================================

REQUIRED_SECTIONS = [
    '1. Overview',
    '2. Colors',
    '3. Typography',
    '4. Sections',
    '5. Components',
    "6. Do",  # "Do's and Don'ts" 開頭可變
]


def validate_design(path: str | Path) -> tuple[bool, list[str]]:
    """
    驗證 DESIGN.md 的 YAML frontmatter 跟 markdown body 是否漂移。

    Returns:
        (passed, warnings):
        - passed: True 如果無嚴重漂移
        - warnings: 漂移警告清單（給人類看）

    驗證項目：
    1. 必要 markdown 段落是否齊全（6 段）
    2. YAML colors 是否在 markdown body 出現過至少一次
    3. YAML typography role 是否在 markdown body 提到過
    """
    p = Path(path)
    if not p.exists():
        return False, [f"檔案不存在: {p}"]

    text = p.read_text(encoding='utf-8')

    try:
        frontmatter, body = extract_frontmatter(text)
    except ValueError as e:
        return False, [f"YAML 解析失敗: {e}"]

    warnings: list[str] = []

    # Check 1: 必要段落
    for section in REQUIRED_SECTIONS:
        # 容許「## 1. Overview」或「## 1. Overview: The XXX」
        if not re.search(rf'^##\s+{re.escape(section)}', body, re.MULTILINE):
            warnings.append(f"Markdown body 缺少必要段落 '## {section}'")

    # Check 2: YAML colors 在 markdown body 出現（hex 直寫 OR {colors.NAME} token 引用）
    body_upper = body.upper()
    for color_name, color_value in (frontmatter.get('colors') or {}).items():
        if not isinstance(color_value, str):
            continue
        # 條件 A: hex 值直接出現在 body
        if color_value.upper() in body_upper:
            continue
        # 條件 B: 以 token reference 形式出現（如 {colors.primary}）
        if f'{{colors.{color_name}}}' in body:
            continue
        warnings.append(
            f"colors.{color_name} ({color_value}) 在 YAML 定義但 markdown body 沒提到（hex 或 {{colors.{color_name}}}）——可能漂移"
        )

    # Check 3: YAML typography role 在 markdown body 提到（role 名 OR {typography.NAME} token 引用）
    body_lower = body.lower()
    for role in (frontmatter.get('typography') or {}).keys():
        # 容許 'heading_1' 或 'heading 1' 或 'Heading 1' 形式
        role_variants = {
            role.lower(),
            role.replace('_', ' ').lower(),
            role.replace('_', '').lower(),
        }
        if any(v in body_lower for v in role_variants):
            continue
        # 條件 B: 以 token reference 形式出現（如 {typography.body}）
        if f'{{typography.{role}}}' in body:
            continue
        warnings.append(
            f"typography.{role} 在 YAML 定義但 markdown body 沒提到（role 名或 {{typography.{role}}}）——可能漂移"
        )

    return (len(warnings) == 0), warnings


# ============================================================
#                    序列化（CLI --print 用）
# ============================================================

def _serialize_for_json(obj: Any) -> Any:
    """把 docx 型別 (Pt/Cm/RGBColor) 轉成 JSON-serializable"""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _serialize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        # tuple 形式（fallback 模式）保留 type marker
        if len(obj) >= 2 and isinstance(obj[0], str) and obj[0] in ('Pt', 'Cm', 'RGBColor'):
            return list(obj)
        return [_serialize_for_json(x) for x in obj]
    # 真的 docx 型別（HAS_DOCX=True 時）
    if HAS_DOCX:
        try:
            from docx.shared import Length
            if isinstance(obj, Length):
                return f"{obj.pt}pt"
        except Exception:
            pass
        try:
            from docx.shared import RGBColor as _RGB
            if isinstance(obj, _RGB):
                return f"#{obj}"
        except Exception:
            pass
    return str(obj)


# ============================================================
#                    CLI 入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='DESIGN.md 解析與漂移驗證工具（F-017 / 文本參謀長）',
    )
    parser.add_argument('path', help='DESIGN.md 檔案路徑')
    parser.add_argument(
        '--validate', action='store_true',
        help='執行漂移驗證閘門（YAML vs markdown body）',
    )
    parser.add_argument(
        '--print', dest='do_print', action='store_true',
        help='列印解析後的 DESIGN_SYSTEM dict（JSON 格式）',
    )
    args = parser.parse_args()

    if args.validate:
        passed, warnings = validate_design(args.path)
        if passed:
            print(f"[OK] {args.path} 無漂移")
        else:
            print(f"[WARN] {args.path} 有 {len(warnings)} 條漂移警告:")
            for w in warnings:
                print(f"  - {w}")
            sys.exit(1)

    if args.do_print:
        try:
            design = load_design(args.path)
        except (FileNotFoundError, ValueError) as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(2)
        out = _serialize_for_json(design)
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
