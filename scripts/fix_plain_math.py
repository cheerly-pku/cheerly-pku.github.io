#!/usr/bin/env python3
"""
Fix remaining inline math:
1. ∀X / ∃X followed by adjacent $...$ → merge into one math block
2. ∀X ∈Y (all plain text, no $ on line) → wrap in $...$
"""

import re

PATH = 'tensor-ch9-content.txt'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Protect display math
display_map = {}
def save_display(m):
    key = f'⟪D{len(display_map)}⟫'
    display_map[key] = m.group(0)
    return key
content = re.sub(r'\$\$[\s\S]*?\$\$', save_display, content)

# Protect existing inline math
inline_map = {}
def save_inline(m):
    key = f'⟪I{len(inline_map)}⟫'
    inline_map[key] = m.group(0)
    return key
content = re.sub(r'(?<!\$)\$([^$\n]+?)\$(?!\$)', save_inline, content)

changes = []

# ── Merge: "∀X ⟪I⟫" → single inline block ──
# X = math content between ∀/∃ and the inline block
# This handles: ∀b ⟪I⟫, ∀f ⟪I⟫, ∀a = (a<sup>1</sup>,...)⟪I⟫ etc.

def merge_quant(m, qcmd):
    prefix = m.group(1).strip()  # text between quantifier and inline
    ikey = m.group(2)
    inner = inline_map.get(ikey, '')
    im = re.match(r'\$([^$]+)\$', inner)
    if not im:
        return m.group(0)
    inner_text = im.group(1).strip()
    # Clean prefix: convert HTML sup/sub, Unicode math
    prefix = re.sub(r'<sup>(\d+)</sup>', r'^{\1}', prefix)
    prefix = re.sub(r'<sub>(\d+)</sub>', r'_{\1}', prefix)
    for u, l in [('∈', r'\in'), ('·', r'\cdot'), ('…', r'\cdots'), ('×', r'\times'),
                 ('≠', r'\neq'), ('∗', '*'), ('ε', r'\varepsilon')]:
        prefix = prefix.replace(u, l)
    combined = f'$\\{qcmd} {prefix} {inner_text}$'
    inline_map[ikey] = combined
    changes.append(f'  Merged {qcmd} "{prefix[:50]}" + inline')
    return ikey

# ∀X ⟪I⟫
content = re.sub(
    r'∀\s+([^⟪]{1,80}?)\s*(⟪I\d+⟫)',
    lambda m: merge_quant(m, 'forall'),
    content
)
# ∃X ⟪I⟫
content = re.sub(
    r'∃\s+([^⟪]{1,80}?)\s*(⟪I\d+⟫)',
    lambda m: merge_quant(m, 'exists'),
    content
)


# ── Wrap: "∀X ∈Y" (no $ on line) → "$\forall X \in Y$" ──
# Only on lines without inline placeholders

def wrap_line(line):
    """Wrap plain-text math expressions that use Unicode math symbols."""
    if '⟪D' in line or '⟪I' in line:
        return line
    if re.match(r'^\s*(#|>|\||\- |\* |\d+\.)', line):
        return line

    orig = line

    # Pattern A: ∀X ∈Y or ∃X ∈Y
    # X and Y are short alphanumeric/symbol sequences
    # End before: Chinese character, Chinese punctuation, or line end
    line = re.sub(
        r'([∀∃])\s+'
        r'([a-zA-ZεζηικλμνξπρστυφχψωΔΛΣΩΓΘ0-9,\s·…\+\-\.\(\)\[\]\*<>\^_/|]+?)'
        r'\s*∈\s*'
        r'([a-zA-ZεζηικλμνξπρστυφχψωΔΛΣΩΓΘ0-9\s\+\-\.\(\)\[\]\{\}\*<>\^_/|]+?)'
        r'(?=[，。；：、一-鿿]|$)',
        _wrap_qm, line
    )

    # Pattern B: Simple X ∈Y (one/two variables)
    # Only match single-letter vars to avoid false positives
    line = re.sub(
        r'(?<=[\s,;]|^)'
        r'([a-zA-Z])\s*∈\s*'
        r'([a-zA-ZεζηικλμνξπρστυφχψωΔΛΣΩΓΘ0-9\s\+\-\.\(\)\[\]\{\}\*]+?)'
        r'(?=[，。；：、一-鿿]|$)',
        _wrap_m, line
    )

    if line != orig:
        changes.append(f'  Wrapped: {orig[:80]}...')
    return line


def _wrap_qm(m):
    """Wrap ∀/∃ X ∈ Y → $\forall X \in Y$"""
    q = '\\forall' if m.group(1) == '∀' else '\\exists'
    x = m.group(2).strip()
    y = m.group(3).strip()
    # Clean HTML tags
    x = re.sub(r'<sup>(\d+)</sup>', r'^{\1}', x)
    x = re.sub(r'<sub>(\d+)</sub>', r'_{\1}', x)
    y = re.sub(r'<sup>(\d+)</sup>', r'^{\1}', y)
    y = re.sub(r'<sub>(\d+)</sub>', r'_{\1}', y)
    # Clean Unicode
    for u, l in [('·', r'\cdot'), ('…', r'\cdots'), ('×', r'\times'),
                 ('≠', r'\neq'), ('∗', '*'), ('ε', r'\varepsilon'),
                 ('∈', r'\in'), ('→', r'\to')]:
        x = x.replace(u, l)
        y = y.replace(u, l)
    return f'${q} {x} \\in {y}$'

def _wrap_m(m):
    """Wrap X ∈ Y → $X \in Y$"""
    x = m.group(1).strip()
    y = m.group(2).strip()
    y = re.sub(r'<sup>(\d+)</sup>', r'^{\1}', y)
    y = re.sub(r'<sub>(\d+)</sub>', r'_{\1}', y)
    for u, l in [('·', r'\cdot'), ('…', r'\cdots'), ('×', r'\times'),
                 ('≠', r'\neq'), ('∗', '*')]:
        y = y.replace(u, l)
    return f'${x} \\in {y}$'


# Apply line-by-line
lines = content.split('\n')
new_lines = []
for line in lines:
    new_lines.append(wrap_line(line))
content = '\n'.join(new_lines)


# ── Restore inline math ──
for key, value in inline_map.items():
    content = content.replace(key, value)

# ── Restore display math ──
for key, value in display_map.items():
    content = content.replace(key, value)

# ── Cleanup ──
# Remove doubled commands
content = re.sub(r'\\in\s+\\in', r'\\in', content)
content = re.sub(r'\\forall\s+\\forall', r'\\forall', content)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done. {len(changes)} changes.')
for c in changes:
    print(c)
