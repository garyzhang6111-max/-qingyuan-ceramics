#!/usr/bin/env python3
"""全站品牌名 QINGYUAN → 清原(QINGYUAN) 批量替换。"""
import os, glob, re

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'

# 替换规则（从长到短，避免误伤）
RULES = [
    ('清原', '清原'),            # logo 中文
    ('清原', '清原'),            # copyright 中文
    ('清原', '清原'),
    ('QINGYUAN', 'QINGYUAN'),             # 英文品牌名
    ('qingyuan-ceramics.com', 'qingyuan-ceramics.com'),
    ('hello@qingyuan.example', 'hello@qingyuan.example'),
    ('@qingyuan', '@qingyuan'),
]

# 处理 HTML 和 Python 文件
html_files = glob.glob(os.path.join(SITE, 'site/**/*.html'), recursive=True)
py_files = glob.glob(os.path.join(SITE, '*.py'))
files = html_files + py_files

total = 0
changed_files = []
for f in files:
    try:
        s = open(f, encoding='utf-8').read()
    except Exception:
        continue
    orig = s
    n = 0
    for a, b in RULES:
        s, c = re.subn(re.escape(a), b, s)
        n += c
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)
        total += n
        changed_files.append(os.path.relpath(f, SITE))

print(f'替换 {total} 处，{len(changed_files)} 个文件')
for f in changed_files[:20]:
    print(' ', f)
if len(changed_files) > 20:
    print(f'  ... 共 {len(changed_files)} 个文件')
